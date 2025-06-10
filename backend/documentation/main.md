
## **Trading Simulator**

### Overview

The **Trading Simulator** is a stateless execution engine designed to simulate the execution of trading orders against historical market data. It is exposed as a REST API and accepts structured trade instructions (orders) as input. It returns detailed execution results and performance metrics.

The simulator does **not** perform any signal generation or strategy logic — it solely focuses on **deterministic execution and evaluation** of submitted orders.

---

### Core Use Cases

- Backtest pre-generated orders against historical OHLCV data
    
- Benchmark strategies in a consistent and repeatable simulation environment
    
- Integrate with internal strategy labs or external users via API
    

---

### 🧠 Key Concepts

|Concept|Description|
|---|---|
|**Order**|A structured instruction to enter a trade at a specific time and price, with associated stop loss and take profit levels|
|**Execution**|The act of simulating how the order would have been filled based on historical candle data|
|**Timeframe**|Candle interval used for simulation (e.g., 15m, 1h)|
|**Execution Window**|Time period over which the simulator will attempt to execute the orders|
|**Fill Logic**|Deterministic rule set to simulate MKT or LMT order fills, including SL/TP triggers|

---

## 🛠️ Supported Features (MVP Scope)

| Feature                               |
| ------------------------------------- |
| Historical OHLCV-based simulation     |
| Daily + Intraday intervals (1m to 4h) |
| LMT and MKT orders                    |
| Bracket orders (Entry, SL, TP)        |
| Win/loss and PnL metrics              |
| Multiple orders per request           |
| Single-symbol per simulation run      |
| Simple REST API                       |
| Equity curve / trade log in output    |


---

## 📥 Order Schema (Input)

```json
{
  "symbol": "AAPL",
  "timeframe": "15m",
  "start": "2024-04-01T00:00:00Z",
  "end": "2024-07-01T00:00:00Z",
  "orders": [
    {
      "entry_time": "2024-05-10T14:00:00Z",
      "entry_type": "LMT",           // or "MKT"
      "entry_price": 185.50,         // ignored for MKT
      "side": "buy",                 // or "sell"
      "stop_loss": 182.00,
      "take_profit": 190.00
    },
    ...
  ]
}
```

---

## 📤 Simulation Output Schema

```json
{
  "symbol": "AAPL",
  "timeframe": "15m",
  "start": "2024-04-01T00:00:00Z",
  "end": "2024-07-01T00:00:00Z",
  "metrics": {
    "total_orders": 12,
    "executed_orders": 10,
    "win_rate": 0.7,
    "total_pnl": 1234.56,
    "avg_trade_return": 1.25,
    "max_drawdown": -2.15
  },
  "trades": [
    {
      "entry_time": "2024-05-10T14:00:00Z",
      "exit_time": "2024-05-11T10:15:00Z",
      "entry_price": 185.50,
      "exit_price": 190.00,
      "side": "buy",
      "result": "tp",        // "tp", "sl", or "timeout"
      "pnl": 4.5,
      "holding_minutes": 1275
    },
    ...
  ]
}
```

---

## 🔄 Fill Logic (Execution Model)

|Order Type|Fill Rule|
|---|---|
|**MKT**|Entry filled at the open price of `entry_time` bar|
|**LMT**|Entry fills if price touches `entry_price` during or after `entry_time`|
|**TP / SL**|Evaluated once position is open, in candle order. First touch wins (unless you model more complex intra-candle logic)|
|**Unfilled Orders**|Discarded if entry conditions are never met within the simulation window|

---

## 🚀 API Design

### `POST /simulate`

**Request:**

- Accepts JSON as per order schema
    

**Response:**

- Returns structured execution results (as above)
    

**Example Curl:**

```bash
curl -X POST http://localhost:8000/simulate \
     -H "Content-Type: application/json" \
     -d @orders.json
```

---

## 🧰 Future Extensions (Post-MVP)

|Feature|Notes|
|---|---|
|Slippage modeling|Random or fixed per symbol|
|Fees and commissions|Per trade or per volume|
|Multi-symbol simulation|Requires state partitioning|
|Bar-by-bar simulation|For LSTM-like step-through or walk-forward|
|Tick-level simulation|Advanced, if data available|
|Interactive UI|To visualize equity curve, trades on chart|
|Async / Job Queue|For large-scale batch simulations|

---
