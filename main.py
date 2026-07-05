"""
Rex HVAC Checklist System - Main Entry Point
Raspberry Pi 5 with OSOYOO 4.3" touchscreen
"""

import tkinter as tk
import sys

# Import components
try:
    from checklist import JobManager
    print("checklist.py loaded successfully")
except ImportError as e:
    print(f"Error importing checklist: {e}")
    sys.exit(1)

try:
    from voice import VoiceHandler
    print("voice.py loaded successfully")
except ImportError as e:
    print(f"Error importing voice: {e}")
    sys.exit(1)

try:
    from ui import UI
    print("ui.py loaded successfully")
except ImportError as e:
    print(f"Error importing ui: {e}")
    sys.exit(1)

def main():
    """Main entry point"""
    
    # Create Tkinter root
    root = tk.Tk()
    
    # Initialize components
    job_manager = JobManager()
    voice_handler = VoiceHandler()
    
    # Launch UI
    app = UI(root, job_manager, voice_handler)
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    print("=== Rex HVAC Checklist System ===")
    main()
