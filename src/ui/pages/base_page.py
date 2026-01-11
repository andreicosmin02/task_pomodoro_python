"""
Base Page Class

Abstract base class for all application pages.
"""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional

from ..theme import Colors


class BasePage(tk.Frame, ABC):
    """
    Abstract base class for application pages.
    
    Provides common functionality and structure for all pages.
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the base page.
        
        Args:
            parent: Parent widget (usually the main app window)
        """
        super().__init__(parent, bg=Colors.BG_PRIMARY)
        
        # Container for centered content
        self.container = tk.Frame(self, bg=Colors.BG_PRIMARY)
        self.container.place(relx=0.5, rely=0.5, anchor="center")
    
    @abstractmethod
    def update_timer_display(self) -> None:
        """Update the timer display. Override in timer pages."""
        pass
    
    def on_timer_started(self) -> None:
        """Called when timer starts. Override in subclasses."""
        pass
    
    def on_pause_toggled(self, is_paused: bool) -> None:
        """Called when pause state changes. Override in subclasses."""
        pass