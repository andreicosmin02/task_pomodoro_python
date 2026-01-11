"""
Starting Page

The initial landing page with app title and start button.
"""

import tkinter as tk
from typing import Callable

from .base_page import BasePage
from ..theme import Colors, Fonts
from ..widgets import RoundedButton, ClockIcon


class StartingPage(BasePage):
    """
    Starting page of the application.
    
    Displays the app title, clock icon, and start button.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        on_start_work: Callable[[], None],
    ):
        """
        Initialize the starting page.
        
        Args:
            parent: Parent widget
            on_start_work: Callback when start button is pressed
        """
        super().__init__(parent)
        
        self.on_start_work = on_start_work
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create page widgets."""
        # Clock icon
        icon = ClockIcon(self.container, size=80, color=Colors.ACCENT_WARM)
        icon.pack(pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            self.container,
            text="TaskPomodoro",
            font=(Fonts.FAMILY_PRIMARY, Fonts.SIZE_HEADING, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        )
        title_label.pack(pady=(0, 40))
        
        # Start button
        start_btn = RoundedButton(
            self.container,
            text="Start Work",
            command=self.on_start_work,
            bg=Colors.ACCENT_WARM,
            hover_bg=Colors.ACCENT_WARM_HOVER,
            width=150,
            height=48,
            font_size=Fonts.SIZE_LARGE
        )
        start_btn.pack()
    
    def update_timer_display(self) -> None:
        """Not used on starting page."""
        pass