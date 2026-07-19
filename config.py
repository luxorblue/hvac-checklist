"""
Configuration for Rex HVAC Checklist System
Optimized for Raspberry Pi 5 with OSOYOO 4.3" 800x480 DSI touchscreen
"""

APP_VERSION = "0.1.0"
APP_NAME = "Rex HVAC Checklist"

# HVAC System Types
SYSTEM_TYPES = ["Heat Pump System", "Furnace System"]

# Common checklist items
COMMON_CHECKLIST = [
    "ODF cap",
    "Comp cap",
    "Start cap",
    "ODF amps",
    "Comp amps",
    "Press",
    "Blower cap",
    "Blower amps",
    "Evap coil condition",
    "Evap coil drain pan condition",
    "Blower wheel condition",
    "Temp split",
    "Filter",
    "Surge prot",
    "Drain condition",
]

# Furnace-specific items
FURNACE_ONLY_CHECKLIST = [
    "Inducer motor",
    "Furnace safeties",
    "CO detector",
]

# Complete checklists by system type
CHECKLISTS = {
    "Heat Pump System": COMMON_CHECKLIST.copy(),
    "Furnace System": COMMON_CHECKLIST + FURNACE_ONLY_CHECKLIST,
}

# UI Configuration for 800x480 touchscreen
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480

# Font sizes (adjusted for 4.3" touchscreen)
FONT_TITLE = ("Arial", 28, "bold")
FONT_HEADER = ("Arial", 20, "bold")
FONT_LARGE = ("Arial", 18)
FONT_NORMAL = ("Arial", 16)
FONT_SMALL = ("Arial", 12)

# Button dimensions
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2
BUTTON_FONT = ("Arial", 14, "bold")

# Colors
COLOR_BG = "#f0f0f0"
COLOR_HEADER = "#2c3e50"
COLOR_BUTTON = "#3498db"
COLOR_BUTTON_HOVER = "#2980b9"
COLOR_TEXT = "#2c3e50"
COLOR_STATUS = "#27ae60"
COLOR_WARNING = "#e74c3c"

# Data directory
DATA_DIR = "job_data"
