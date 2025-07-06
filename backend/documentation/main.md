## **Trading Simulator**

### Overview

The **Trading Simulator** is a stateless execution engine designed to simulate the execution of trading orders against historical market data. It is exposed as a REST API and accepts structured trade instructions (orders) as input. It returns detailed execution results and performance metrics.

The simulator does **not** perform any signal generation or strategy logic — it solely focuses on **deterministic execution and evaluation** of submitted orders.

### 🚧 **Current Implementation Status**

**✅ Completed:**

- FastAPI application structure with CORS middleware
- Complete Pydantic data models for orders and responses
- Type-safe API endpoint definitions
- Comprehensive validation logic for orders
- Error handling and response models
- Development environment setup with uv package manager
- Type checking configuration with pyright
- Code formatting with ruff

**🔄 In Progress:**

- Core simulation engine implementation (placeholder currently exists)
- Historical data integration
- Order execution logic

**📋 Planned:**

- Unit tests and integration tests
- Performance optimization
- Documentation completion

### 🔧 **Recent Fixes & Improvements**

**Import Resolution Issues (Resolved):**

- ✅ Fixed pydantic import resolution by adding explicit dependency
- ✅ Configured IDE to use correct Python interpreter from uv virtual environment
- ✅ Added proper type annotations for ValidationInfo and other Pydantic types
- ✅ Resolved FastAPI import issues through proper environment configuration

**Code Quality Improvements:**

- ✅ Removed unused imports across all modules
- ✅ Fixed missing parameters in ErrorResponse calls
- ✅ Added comprehensive type annotations for validation functions
- ✅ Consolidated pyright configuration into single pyrightconfig.json file
- ✅ Updated project to target Python 3.11+ for broader compatibility

**Development Environment:**

- ✅ Configured VS Code with proper Python interpreter path
- ✅ Set up strict type checking with pyright
- ✅ Implemented code formatting standards with ruff
- ✅ Established proper virtual environment management with uv

---

## 🏗️ **Technical Architecture**

### Project Structure

```
backend/
├── src/
│   ├── api/                 # FastAPI route handlers
│   │   ├── __init__.py
│   │   └── simulation.py    # Main simulation endpoints
│   ├── models/              # Pydantic data models
│   │   ├── __init__.py
│   │   ├── enums.py        # Enums for order types, sides, etc.
│   │   ├── orders.py       # Order and request models
│   │   └── responses.py    # Response and metrics models
│   ├── core/               # Core business logic
│   │   └── __init__.py
│   ├── services/           # External service integrations
│   │   └── __init__.py
│   └── main.py            # FastAPI application entry point
├── pyproject.toml         # Project dependencies and configuration
├── pyrightconfig.json     # Type checking configuration
└── uv.lock               # Dependency lock file
```

### Technology Stack

- **Framework:** FastAPI 0.115.12+ with standard extras
- **Data Validation:** Pydantic 2.11.5+ with comprehensive validation
- **Package Management:** uv for fast dependency resolution
- **Type Checking:** Pyright with strict configuration
- **Code Formatting:** Ruff with Python 3.11+ target
- **Python Version:** 3.13+ (development), 3.11+ (target compatibility)

### API Endpoints

- `POST /api/v1/simulate` - Main simulation endpoint (placeholder implementation)
- `GET /api/v1/health` - Health check endpoint

---

### Core Use Cases

- Backtest pre-generated orders against historical OHLCV data.
- Benchmark strategies in a consistent and repeatable simulation environment
- Integrate with internal strategy labs or external users via API

---

### 🧠 Key Concepts

| Concept              | Description                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Order**            | A structured instruction to enter a trade at a specific time and price, with associated stop loss and take profit levels |
| **Execution**        | The act of simulating how the order would have been filled based on historical candle data                               |
| **Timeframe**        | Candle interval used for simulation (e.g., 15m, 1h)                                                                      |
| **Execution Window** | Time period over which the simulator will attempt to execute the orders                                                  |
| **Fill Logic**       | Deterministic rule set to simulate MKT or LMT order fills, including SL/TP triggers                                      |

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

| Order Type          | Fill Rule                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **MKT**             | Entry filled at the open price of `entry_time` bar                                                                    |
| **LMT**             | Entry fills if price touches `entry_price` during or after `entry_time`                                               |
| **TP / SL**         | Evaluated once position is open, in candle order. First touch wins (unless you model more complex intra-candle logic) |
| **Unfilled Orders** | Discarded if entry conditions are never met within the simulation window                                              |

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

## 🚀 **Development Setup**

### Prerequisites

- Python 3.13+ (recommended) or 3.11+ (minimum)
- [uv](https://docs.astral.sh/uv/) package manager

### Quick Start

```bash
# Clone and navigate to the project
cd backend

# Install dependencies
uv sync

# Run the development server
uv run fastapi dev src/main.py

# The API will be available at:
# - Main API: http://localhost:8000
# - Interactive docs: http://localhost:8000/docs
# - OpenAPI spec: http://localhost:8000/openapi.json
```

### Development Commands

```bash
# Type checking
uv run pyright

# Code formatting
uv run ruff format

# Code linting
uv run ruff check

# Run tests (when implemented)
uv run pytest
```

### IDE Configuration

The project includes configuration for:

- **VS Code**: Python interpreter path and pyright settings
- **Pyright**: Strict type checking with comprehensive error reporting
- **Ruff**: Code formatting and linting rules

### Current API Status

- ✅ **API Structure**: Fully implemented with proper routing
- ✅ **Data Models**: Complete with validation
- ✅ **Error Handling**: Comprehensive error responses
- 🔄 **Simulation Logic**: Placeholder implementation (returns mock data)

### 🔧 **Troubleshooting**

**Common Issues:**

1. **Import Resolution Errors**

   ```bash
   # Ensure you're using the correct virtual environment
   uv sync
   # Verify Python interpreter in VS Code points to: ./backend/.venv/bin/python
   ```

2. **Type Checking Issues**

   ```bash
   # Run type checking manually
   uv run pyright
   # Check pyrightconfig.json is properly configured
   ```

3. **API Server Issues**

   ```bash
   # Start development server with auto-reload
   uv run fastapi dev src/main.py
   # Check logs for import or configuration errors
   ```

4. **Dependency Issues**
   ```bash
   # Reinstall dependencies
   uv sync --reinstall
   # Update lock file
   uv lock --upgrade
   ```

---

## 🧰 Future Extensions (Post-MVP)

| Feature                 | Notes                                      |
| ----------------------- | ------------------------------------------ |
| Slippage modeling       | Random or fixed per symbol                 |
| Fees and commissions    | Per trade or per volume                    |
| Multi-symbol simulation | Requires state partitioning                |
| Bar-by-bar simulation   | For LSTM-like step-through or walk-forward |
| Tick-level simulation   | Advanced, if data available                |
| Interactive UI          | To visualize equity curve, trades on chart |
| Async / Job Queue       | For large-scale batch simulations          |

---
