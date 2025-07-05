"""
Trading Simulator FastAPI Application.

This is the main entry point for the Trading Simulator API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import simulation_router

# Create FastAPI application with metadata
app = FastAPI(
    title="Trading Simulator API",
    description="""
    A stateless execution engine designed to simulate the execution of trading orders
    against historical market data. The simulator focuses on deterministic execution
    and evaluation of submitted orders without performing signal generation or strategy logic.

    ## Features

    * Historical OHLCV-based simulation
    * Support for daily and intraday intervals (1m to 4h)
    * Market and limit order types
    * Bracket orders with stop loss and take profit
    * Comprehensive performance metrics
    * Multiple orders per simulation request

    ## Usage

    Submit trading orders via the `/api/v1/simulate` endpoint and receive detailed
    execution results including individual trade outcomes and performance metrics.
    """,
    version="1.0.0",
    contact={
        "name": "Trading Simulator API",
        "url": "https://github.com/your-repo/trading-simulator",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(simulation_router)


@app.get("/", tags=["root"])
async def read_root() -> dict[str, str]:
    """
    Root endpoint providing basic API information.

    Returns:
        dict: Basic API information
    """
    return {
        "message": "Trading Simulator API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
