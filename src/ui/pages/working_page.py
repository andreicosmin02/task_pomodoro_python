"""
Working Page

The work timer page with controls for start, pause, stop, and rest.
"""

import tkinter as tk
from typing import Callable, Optional

from .base_page import BasePage
from ..theme import Colors, Fonts
from ..widgets import RoundedButton, CustomDialog
from ...utils.formatting import format_duration
from ...core.state import TimerState


class WorkingPage(BasePage):
    """
    Working page with the work timer.
    
    Displays the upward-counting work timer and control buttons.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        timer_state: TimerState,
        on_start: Callable[[], None],
        on_pause: Callable[[], None],
        on_stop: Callable[[], None],
        on_go_resting: Callable[[], None],
    ):
        """
        Initialize the working page.
        
        Args:
            parent: Parent widget
            timer_state: Timer state object
            on_start: Callback to start timer
            on_pause: Callback to pause/resume timer
            on_stop: Callback to stop and reset
            on_go_resting: Callback to go to rest mode
        """
        super().__init__(parent)
        
        self.timer_state = timer_state
        self.on_start = on_start
        self.on_pause = on_pause
        self.on_stop = on_stop
        self.on_go_resting = on_go_resting
        
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
            text="Work Timer",
            font=(Fonts.FAMILY_PRIMARY, Fonts.SIZE_TITLE, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        )
        label.pack(pady=(0, 20))
        
        # Timer display
        self.timer_label = tk.Label(
            self.container,
            text="00:00:00",
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
            bg=Colors.ACCENT_WARM,
            hover_bg=Colors.ACCENT_WARM_HOVER,
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
        
        # Go resting button
        rest_btn = RoundedButton(
            self.container,
            text="Go Resting",
            long_press_command=self.on_go_resting,
            long_press_hint="Long press to go resting",
            bg=Colors.BG_SECONDARY,
            hover_bg=Colors.BG_TERTIARY,
            width=140,
            height=40
        )
        rest_btn.pack()
    
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
                text=format_duration(self.timer_state.elapsed_seconds)
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