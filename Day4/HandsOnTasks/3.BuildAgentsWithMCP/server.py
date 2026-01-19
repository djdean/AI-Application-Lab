# server.py
from mcp.server.fastmcp import FastMCP
import logging
import sys

# Configure logging to show info messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("Inventory")
logger.info("🚀 MCP Inventory Server initialized")
logger.info("📦 Available tools: get_inventory_levels, get_weekly_sales")

# Add an inventory check tool
@mcp.tool()
def get_inventory_levels() -> dict:
     """Returns current inventory for all products."""
     logger.info("📊 get_inventory_levels() called")
     return {
         "Moisturizer": 6,
         "Shampoo": 8,
         "Body Spray": 28,
         "Hair Gel": 5, 
         "Lip Balm": 12,
         "Skin Serum": 9,
         "Cleanser": 30,
         "Conditioner": 3,
         "Setting Powder": 17,
         "Dry Shampoo": 45
     }


# Add a weekly sales tool
@mcp.tool()
def get_weekly_sales() -> dict:
     """Returns number of units sold last week."""
     logger.info("📈 get_weekly_sales() called")
     return {
         "Moisturizer": 22,
         "Shampoo": 18,
         "Body Spray": 3,
         "Hair Gel": 2,
         "Lip Balm": 14,
         "Skin Serum": 19,
         "Cleanser": 4,
         "Conditioner": 1,
         "Setting Powder": 13,
         "Dry Shampoo": 17
     }


logger.info("🏃 Starting MCP server...")
mcp.run()