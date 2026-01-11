"""
Rounded Button Widget

A modern, rounded button with hover effects and long-press support.
"""

import tkinter as tk
import time
from typing import Callable, Optional

from ..theme import Colors, Fonts, Dimensions


class RoundedButton(tk.Canvas):
    """
    A modern rounded button with hover effects.
    
    Features:
        - Rounded corners
        - Hover color change
        - Long-press gesture support
        - Disabled state
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        bg: str = Colors.BG_TERTIARY,
        fg: str = Colors.TEXT_PRIMARY,
        hover_bg: str = Colors.BG_HOVER,
        width: int = Dimensions.BUTTON_WIDTH,
        height: int = Dimensions.BUTTON_HEIGHT,
        font_size: int = Fonts.SIZE_NORMAL,
        disabled: bool = False,
        long_press_command: Optional[Callable] = None,
        long_press_hint: Optional[str] = None,
        corner_radius: int = Dimensions.CORNER_RADIUS,
    ):
        """
        Initialize the rounded button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Click callback
            bg: Background color
            fg: Foreground (text) color
            hover_bg: Background color on hover
            width: Button width in pixels
            height: Button height in pixels
            font_size: Font size for text
            disabled: Whether button is disabled
            long_press_command: Callback for long press
            long_press_hint: Hint shown on short press if long_press_command set
            corner_radius: Corner radius for rounded effect
        """
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=Colors.BG_PRIMARY,
            highlightthickness=0
        )
        
        self.text = text
        self.command = command
        self.long_press_command = long_press_command
        self.long_press_hint = long_press_hint
        self.btn_width = width
        self.btn_height = height
        self.font_size = font_size
        self.corner_radius = corner_radius
        self._disabled = disabled
        
        # Colors
        self.bg_normal = bg
        self.bg_hover = hover_bg
        self.fg = fg
        self.current_bg = self.bg_normal
        
        # Long press tracking
        self.press_start_time: Optional[float] = None
        self.long_press_threshold = 0.5  # seconds
        self.long_press_timer: Optional[str] = None
        
        self._draw()
        if not disabled:
            self._bind_events()
    
    def _draw(self) -> None:
        """Draw the button."""
        self.delete("all")
        
        r = self.corner_radius
        x1, y1 = 2, 2
        x2, y2 = self.btn_width - 2, self.btn_height - 2
        
        bg = Colors.BG_HOVER if self._disabled else self.current_bg
        fg = Colors.TEXT_MUTED if self._disabled else self.fg
        
        # Draw rounded rectangle using arcs and rectangles
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=bg, outline=bg)
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=bg, outline=bg)
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=bg, outline=bg)
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=bg, outline=bg)
        
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=bg, outline=bg)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=bg, outline=bg)
        
        # Draw text
        self.create_text(
            self.btn_width // 2,
            self.btn_height // 2,
            text=self.text,
            fill=fg,
            font=(Fonts.FAMILY_PRIMARY, self.font_size)
        )
    
    def _bind_events(self) -> None:
        """Bind mouse events."""
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _unbind_events(self) -> None:
        """Unbind mouse events."""
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")
    
    def _on_enter(self, event: tk.Event) -> None:
        """Handle mouse enter."""
        if not self._disabled:
            self.current_bg = self.bg_hover
            self._draw()
            self.config(cursor="hand2")
    
    def _on_leave(self, event: tk.Event) -> None:
        """Handle mouse leave."""
        self.current_bg = self.bg_normal
        self._draw()
        self.config(cursor="")
        if self.long_press_timer:
            self.after_cancel(self.long_press_timer)
            self.long_press_timer = None
    
    def _on_press(self, event: tk.Event) -> None:
        """Handle mouse button press."""
        if self._disabled:
            return
        self.press_start_time = time.time()
        if self.long_press_command:
            self.long_press_timer = self.after(
                int(self.long_press_threshold * 1000),
                self._check_long_press
            )
    
    def _check_long_press(self) -> None:
        """Check if long press threshold reached."""
        if self.press_start_time:
            elapsed = time.time() - self.press_start_time
            if elapsed >= self.long_press_threshold and self.long_press_command:
                self.long_press_command()
                self.press_start_time = None
    
    def _on_release(self, event: tk.Event) -> None:
        """Handle mouse button release."""
        if self._disabled:
            return
        
        if self.long_press_timer:
            self.after_cancel(self.long_press_timer)
            self.long_press_timer = None
        
        if self.press_start_time:
            elapsed = time.time() - self.press_start_time
            if elapsed < self.long_press_threshold:
                if self.command:
                    self.command()
                elif self.long_press_hint:
                    # Show hint via toast
                    top = self.winfo_toplevel()
                    if hasattr(top, 'show_toast'):
                        top.show_toast(self.long_press_hint)
            self.press_start_time = None
    
    def set_disabled(self, disabled: bool) -> None:
        """Set the disabled state."""
        self._disabled = disabled
        if disabled:
            self._unbind_events()
        else:
            self._bind_events()
        self._draw()
    
    def update_text(self, text: str) -> None:
        """Update the button text."""
        self.text = text
        self._draw()
    
    def update_colors(self, bg: str, hover_bg: str) -> None:
        """Update button colors."""
        self.bg_normal = bg
        self.bg_hover = hover_bg
        self.current_bg = bg
        self._draw()