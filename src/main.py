#!/usr/bin/env python3
"""
TaskPomodoro - Application Entry Point

This is the main entry point for the TaskPomodoro application.
Run with: python -m src.main
"""

import sys
from pathlib import Path

# Add src to path for proper imports when running directly
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path.parent))

from src.core.app import TaskPomodoroApp


def main():
    """Main entry point for the application."""
    app = TaskPomodoroApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()