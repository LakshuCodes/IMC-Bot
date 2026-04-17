from datamodel import Order, TradingState
from typing import Dict, List
import json

# Position limits per product
POSITION_LIMITS = {
    "ASH_COATED_OSMIUM": 20,
    "INTARIAN_PEPPER_ROOT": 20,
}


class Trader:
    """
    IMC Prosperity Round 1 Trader
    - ASH_COATED_OSMIUM:     Stable ~9984. Mean-reversion market making.
    - INTARIAN_PEPPER_ROOT:  Trending UP ~1000/day. Trend-following with long bias.
    """

    def run(self, state: TradingState):
        # ── Load persisted data (price history survives across timestamps) ──
        try:
            data = json.loads(state.traderData) if state.traderData else {}
        except Exception:
            data = {}

        price_history: Dict[str, List[float]] = data.get("price_history", {})
        result: Dict[str, List[Order]] = {}

        for product, order_depth in state.order_depths.items():
            limit = POSITION_LIMITS.get(product, 20)
            position = state.position.get(product, 0)

            # ── Best bid / ask ──────────────────────────────────────────────
            best_ask = min(order_depth.sell_orders) if order_depth.sell_orders else None
            best_bid = max(order_depth.buy_orders)  if order_depth.buy_orders  else None

            # ── Track mid-price history ─────────────────────────────────────
            if product not in price_history:
                price_history[product] = []

            if best_ask is not None and best_bid is not None:
                mid = (best_ask + best_bid) / 2
                price_history[product].append(mid)
                price_history[product] = price_history[product][-100:]  # keep last 100

            history = price_history[product]
            orders: List[Order] = []

            if len(history) < 5:
                result[product] = orders
                continue

            # ── Compute moving averages ─────────────────────────────────────
            short_mean = sum(history[-5:])  / 5
            long_mean  = sum(history[-20:]) / min(20, len(history))
            trend      = short_mean - long_mean  # positive = uptrend

            # ── Strategy per product ────────────────────────────────────────
            if product == "ASH_COATED_OSMIUM":
                # Stable, mean-reverting product → market make around fair value
                fair = short_mean
                buy_price  = round(fair) - 2
                sell_price = round(fair) + 2

                # Passive orders
                buy_vol  = min(10, limit - position)
                sell_vol = min(10, limit + position)
                if buy_vol  > 0: orders.append(Order(product, buy_price,   buy_vol))
                if sell_vol > 0: orders.append(Order(product, sell_price, -sell_vol))

                # Aggressively cross the spread when mispriced
                if best_ask is not None and best_ask < round(fair) - 1:
                    take = min(abs(order_depth.sell_orders[best_ask]), limit - position)
                    if take > 0:
                        orders.append(Order(product, best_ask, take))

                if best_bid is not None and best_bid > round(fair) + 1:
                    take = min(order_depth.buy_orders[best_bid], limit + position)
                    if take > 0:
                        orders.append(Order(product, best_bid, -take))

            elif product == "INTARIAN_PEPPER_ROOT":
                # Trending UP ~1000 per day → bias long, ride the trend
                fair = short_mean

                if trend >= 0:
                    # Uptrend: buy aggressively, sell conservatively
                    buy_at   = best_bid + 1 if best_bid is not None else round(fair) - 1
                    sell_at  = best_ask - 1 if best_ask is not None else round(fair) + 4

                    buy_vol  = min(10, limit - position)   # max long
                    sell_vol = min(3,  limit + position)   # minimal short
                else:
                    # Rare downswing: tighten up, still lean long
                    buy_at   = best_bid + 1 if best_bid is not None else round(fair) - 2
                    sell_at  = best_ask - 1 if best_ask is not None else round(fair) + 2

                    buy_vol  = min(5,  limit - position)
                    sell_vol = min(5,  limit + position)

                if buy_vol  > 0: orders.append(Order(product, buy_at,   buy_vol))
                if sell_vol > 0: orders.append(Order(product, sell_at, -sell_vol))

                # Also take cheap asks immediately (trend = price going up)
                if best_ask is not None and best_ask <= round(fair) + 2:
                    take = min(abs(order_depth.sell_orders[best_ask]), limit - position)
                    if take > 0:
                        orders.append(Order(product, best_ask, take))

            result[product] = orders

        # ── Persist price history for next timestamp ────────────────────────
        trader_data = json.dumps({"price_history": price_history})

        # Return: orders dict, conversions (0), persisted data string
        return result, 0, trader_data