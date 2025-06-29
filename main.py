"""
DexBot.py - Modular Entry Point
Entry point for the modular DexBot system

Author: RugRat79
Version: 2.1.0 (Infrastructure)
License: MIT
"""

import sys
import os

# Add the src directory to the Python path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "src")
sys.path.insert(0, src_dir)

try:
    # Import and run the modular bot system
    from src.core.main_loop import run_dexbot
    
    # Script entry point
    if __name__ == "__main__":
        run_dexbot()
        
except ImportError as e:
    print(f"[DexBot] Import error: {e}")
    print("[DexBot] Falling back to legacy DexBot.py if available...")
    # If modular import fails, could fall back to the original file
    # but for now we'll just show the error
    raise
except Exception as e:
    print(f"[DexBot] Error starting bot: {e}")
    raise
