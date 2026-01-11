"""
Clock Icon Widget

A decorative clock icon drawn with canvas.
"""

import tkinter as tk

from ..theme import Colors


class ClockIcon(tk.Canvas):
    """
    A clock icon drawn with canvas.
    
    Used on the starting page as a decorative element.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        size: int = 80,
        color: str = Colors.ACCENT_WARM,
    ):
        """
        Initialize the clock icon.
        
        Args:
            parent: Parent widget
            size: Icon size in pixels
            color: Icon color
        """
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=Colors.BG_PRIMARY,
            highlightthickness=0
        )
        
        self.size = size
        self.color = color
        self._draw()
    
    def _draw(self) -> None:
        """Draw the clock icon."""
        self.delete("all")
        
        cx, cy = self.size // 2, self.size // 2
        r = self.size // 2 - 4
        
        # Draw circle outline
        self.create_oval(
            cx - r, cy - r,
            cx + r, cy + r,
            outline=self.color,
            width=3
        )
        
        # Draw hour hand (pointing to 12)
        self.create_line(
            cx, cy,
            cx, cy - r * 0.5,
            fill=self.color,
            width=3,
            capstyle=tk.ROUND
        )
        
        # Draw minute hand (pointing to 3)
        self.create_line(
            cx, cy,
            cx + r * 0.35, cy,
            fill=self.color,
            width=3,
            capstyle=tk.ROUND
        )
    
    def set_color(self, color: str) -> None:
        """Update the icon color."""
        self.color = color
        self._draw()