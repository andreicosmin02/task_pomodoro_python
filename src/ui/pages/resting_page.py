"""
Resting Page

The rest timer page with controls for start, pause, stop, and skip.
"""

import tkinter as tk
from typing import Callable, Optional

from .base_page import BasePage
from ..theme import Colors, Fonts
from ..widgets import RoundedButton, CustomDialog
from ...utils.formatting import format_duration
from ...core.state import TimerState


class RestingPage(BasePage):
    """
    Resting page with the rest timer.
    
    Displays the countdown rest timer and control buttons.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        timer_state: TimerState,
        on_start: Callable[[], None],
        on_pause: Callable[[], None],
        on_stop: Callable[[], None],
        on_skip: Callable[[], None],
    ):
        """
        Initialize the resting page.
        
        Args:
            parent: Parent widget
            timer_state: Timer state object
            on_start: Callback to start rest timer
            on_pause: Callback to pause/resume timer
            on_stop: Callback to stop and reset
            on_skip: Callback to skip rest and return to work
        """
        super().__init__(parent)
        
        self.timer_state = timer_state
        self.on_start = on_start
        self.on_pause = on_pause
        self.on_stop = on_stop
        self.on_skip = on_skip
        
        # UI references
        self.timer_label: Optional[tk.Label] = None
        self.start_btn: Optional[RoundedButton] = None
        self.pause_btn: Optional[RoundedButton] = None
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create page widgets."""
        # Title
        label = tk.Label(
            self.container,
            text="Rest Timer",
            font=(Fonts.FAMILY_PRIMARY, Fonts.SIZE_TITLE, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        )
        label.pack(pady=(0, 20))
        
        # Timer display
        self.timer_label = tk.Label(
            self.container,
            text=format_duration(self.timer_state.rest_seconds),
            font=(Fonts.FAMILY_MONO, Fonts.SIZE_TIMER, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        )
        self.timer_label.pack(pady=(0, 30))
        
        # Control buttons row
        btn_frame = tk.Frame(self.container, bg=Colors.BG_PRIMARY)
        btn_frame.pack(pady=(0, 25))
        
        self.start_btn = RoundedButton(
            btn_frame,
            text="Start",
            command=self.on_start,
            bg=Colors.ACCENT_COOL,
            hover_bg=Colors.ACCENT_COOL_HOVER,
            width=90,
            height=40
        )
        self.start_btn.pack(side=tk.LEFT, padx=8)
        
        self.pause_btn = RoundedButton(
            btn_frame,
            text="Pause",
            command=self.on_pause,
            bg=Colors.BG_TERTIARY,
            hover_bg=Colors.BG_HOVER,
            width=90,
            height=40,
            disabled=True
        )
        self.pause_btn.pack(side=tk.LEFT, padx=8)
        
        stop_btn = RoundedButton(
            btn_frame,
            text="Stop",
            command=self._confirm_stop,
            bg=Colors.DANGER,
            hover_bg=Colors.DANGER_LIGHT,
            width=90,
            height=40
        )
        stop_btn.pack(side=tk.LEFT, padx=8)
        
        # Skip resting button
        skip_btn = RoundedButton(
            self.container,
            text="Skip Resting",
            long_press_command=self.on_skip,
            long_press_hint="Long press to skip resting",
            bg=Colors.BG_SECONDARY,
            hover_bg=Colors.BG_TERTIARY,
            width=140,
            height=40
        )
        skip_btn.pack()
    
    def _confirm_stop(self) -> None:
        """Show confirmation dialog before stopping."""
        CustomDialog(
            self.winfo_toplevel(),
            "Confirmation",
            "Are you sure you want to reset everything?",
            self.on_stop
        )
    
    def update_timer_display(self) -> None:
        """Update the timer display."""
        if self.timer_label:
            self.timer_label.config(
                text=format_duration(self.timer_state.rest_seconds)
            )
    
    def on_timer_started(self) -> None:
        """Handle timer started event."""
        if self.start_btn:
            self.start_btn.set_disabled(True)
        if self.pause_btn:
            self.pause_btn.set_disabled(False)
    
    def on_pause_toggled(self, is_paused: bool) -> None:
        """Handle pause state change."""
        if self.pause_btn:
            self.pause_btn.update_text("Resume" if is_paused else "Pause")