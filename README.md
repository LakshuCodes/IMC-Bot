# 🚀 IMC Prosperity Trading Bot

## 📌 Overview

This project contains an algorithmic trading bot developed for the **IMC Prosperity Trading Challenge**.

The bot is designed to trade efficiently in a simulated market environment by analyzing order books, detecting trends, and executing profitable trades automatically.

---

## 🧠 Strategy Used

The bot uses a **hybrid trading strategy** combining:

### 🔹 1. Mean Reversion (Stable Assets)

* Applied to assets like **ASH_COATED_OSMIUM**
* Assumes price returns to an average (fair value)
* Buys when price is low, sells when high

### 🔹 2. Trend Following (Momentum Trading)

* Applied to assets like **INTARIAN_PEPPER_ROOT**
* Detects upward/downward trends using moving averages
* Buys in uptrend, sells in downtrend

### 🔹 3. Market Making

* Places both buy and sell orders around fair value
* Profits from bid-ask spread

### 🔹 4. Aggressive Execution

* Instantly buys undervalued asks
* Instantly sells overpriced bids

---

## ⚙️ Features

* 📊 Moving Average Analysis (Short-term & Long-term)
* 🧠 Product-Specific Strategy
* 🔄 Persistent Price History (via `traderData`)
* ⚡ Spread Exploitation
* 📈 Trend Detection
* 🛡️ Position Limit Risk Management

---

## 🏗️ Tech Stack

* Python 🐍
* Custom IMC Trading Engine (`datamodel`)
* JSON for state persistence

---

## 📂 Project Structure

```
.
├── main.py          # Trading bot logic
├── datamodel.py     # (optional local testing stub)
├── README.md        # Project documentation
```

---

## ▶️ How It Works

1. Reads live market order book
2. Calculates mid-price and moving averages
3. Detects:

   * Trend (up/down)
   * Fair value
4. Executes:

   * Buy orders (if undervalued)
   * Sell orders (if overvalued)
5. Maintains position within safe limits

---

## 🧪 Testing

* Tested using IMC simulation environment
* Uses historical price patterns for tuning
* Performance evaluated based on profit generation

---

## 🎯 Goal

Maximize profit while:

* Managing risk
* Adapting to different asset behaviors
* Exploiting both trends and inefficiencies

---

## 🏆 Challenge Context

This bot is built specifically for:

👉 **IMC Prosperity Trading Challenge**

* A competitive trading simulation hosted by IMC
* Focuses on algorithmic decision-making
* Requires fast, adaptive, and strategic bots

---

## 🚀 Future Improvements

* Advanced statistical arbitrage
* Machine learning-based predictions
* Dynamic position sizing
* Better volatility handling

---

## 👨‍💻 Author

**Lakshyaa Singh**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork & improve!
