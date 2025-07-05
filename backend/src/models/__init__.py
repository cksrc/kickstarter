"""
Trading Simulator API Models.

This module contains all Pydantic models used for request/response validation
and serialization in the Trading Simulator API.
"""

from .enums import OrderType, OrderSide, TradeResult, Timeframe
from .orders import Order, SimulationRequest
from .responses import Trade, SimulationMetrics, SimulationResponse, ErrorResponse

__all__ = [
    # Enums
    "OrderType",
    "OrderSide",
    "TradeResult",
    "Timeframe",
    # Request models
    "Order",
    "SimulationRequest",
    # Response models
    "Trade",
    "SimulationMetrics",
    "SimulationResponse",
    "ErrorResponse",
]