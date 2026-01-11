"""
Modern Checkbox Widget

A styled checkbox with custom appearance matching the app theme.
"""

import tkinter as tk
from typing import Callable, Optional

from ..theme import Colors, Fonts


class ModernCheckbox(tk.Canvas):
    """
    A modern styled checkbox.
    
    Features:
        - Custom rounded checkbox appearance
        - Animated checkmark
        - Theme-consistent styling
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable[[bool], None]] = None,
        initial_state: bool = False,
    ):
        """
        Initialize the checkbox.
        
        Args:
            parent: Parent widget
            text: Label text
            command: Callback with new state when toggled
            initial_state: Initial checked state
        """
        super().__init__(
            parent,
            height=24,
            bg=Colors.BG_PRIMARY,
            highlightthickness=0
        )
        
        self.text = text
        self.command = command
        self.checked = initial_state
        self.box_size = 18
        
        self._draw()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self.config(cursor="hand2"))
        self.bind("<Leave>", lambda e: self.config(cursor=""))
    
    def _draw(self) -> None:
        """Draw the checkbox."""
        self.delete("all")
        
        # Calculate width based on text
        text_width = len(self.text) * 7 + 30
        self.config(width=max(text_width, 120))
        
        # Box position
        x1, y1 = 2, 3
        x2, y2 = x1 + self.box_size, y1 + self.box_size
        
        box_color = Colors.ACCENT_WARM if self.checked else Colors.BG_TERTIARY
        
        # Draw rounded box
        r = 4
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=box_color, outline=box_color)
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=box_color, outline=box_color)
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=box_color, outline=box_color)
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=box_color, outline=box_color)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=box_color, outline=box_color)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=box_color, outline=box_color)
        
        # Draw checkmark if checked
        if self.checked:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            self.create_line(
                cx - 4, cy,
                cx - 1, cy + 3,
                fill=Colors.TEXT_PRIMARY,
                width=2,
                capstyle=tk.ROUND
            )
            self.create_line(
                cx - 1, cy + 3,
                cx + 5, cy - 4,
                fill=Colors.TEXT_PRIMARY,
                width=2,
                capstyle=tk.ROUND
            )
        
        # Draw label text
        self.create_text(
            x2 + 8,
            (y1 + y2) // 2,
            text=self.text,
            anchor="w",
            fill=Colors.TEXT_SECONDARY,
            font=(Fonts.FAMILY_PRIMARY, 11)
        )
    
    def _on_click(self, event: tk.Event) -> None:
        """Handle click event."""
        self.checked = not self.checked
        self._draw()
        if self.command:
            self.command(self.checked)
    
    def is_checked(self) -> bool:
        """Get current checked state."""
        return self.checked
    
    def set_checked(self, checked: bool) -> None:
        """Set checked state."""
        self.checked = checked
        self._draw()