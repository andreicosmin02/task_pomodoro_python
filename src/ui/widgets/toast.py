"""
Toast Notification Widget

A transient toast notification that appears at the bottom of the window.
"""

import tkinter as tk
import platform

from ..theme import Colors, Fonts


class Toast(tk.Toplevel):
    """
    Modern toast notification.
    
    Displays a message at the bottom of the parent window
    and auto-dismisses after a few seconds.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        message: str,
        duration: int = 2500,
    ):
        """
        Initialize and show the toast.
        
        Args:
            parent: Parent widget (usually the main window)
            message: Message to display
            duration: Display duration in milliseconds
        """
        super().__init__(parent)
        
        self._parent = parent
        
        # Window setup - handle Windows differently
        self.title("")
        self.configure(bg=Colors.SNACKBAR_BG)
        self.resizable(False, False)
        
        # Remove window decorations
        if platform.system() == "Windows":
            # On Windows, use toolwindow style for better compatibility
            self.attributes("-toolwindow", True)
            self.overrideredirect(True)
        else:
            self.overrideredirect(True)
        
        # Try to set transparency
        try:
            self.attributes("-alpha", 0.95)
        except tk.TclError:
            pass
        
        # Make sure it stays on top
        self.attributes("-topmost", True)
        
        # Create content with border for visibility
        outer_frame = tk.Frame(self, bg=Colors.BORDER, padx=1, pady=1)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(outer_frame, bg=Colors.SNACKBAR_BG, padx=20, pady=12)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(
            inner_frame,
            text=message,
            bg=Colors.SNACKBAR_BG,
            fg=Colors.TEXT_PRIMARY,
            font=(Fonts.FAMILY_PRIMARY, 11)
        )
        label.pack()
        
        # Force geometry update
        self.update_idletasks()
        
        # Position at bottom center of parent
        self._position_toast()
        
        # Ensure visibility
        self.lift()
        self.focus_force()
        
        # Auto-dismiss
        self.after(duration, self._dismiss)
    
    def _position_toast(self) -> None:
        """Position the toast at the bottom center of parent."""
        try:
            parent_x = self._parent.winfo_rootx()
            parent_y = self._parent.winfo_rooty()
            parent_width = self._parent.winfo_width()
            parent_height = self._parent.winfo_height()
            
            toast_width = self.winfo_width()
            toast_height = self.winfo_height()
            
            x = parent_x + (parent_width - toast_width) // 2
            y = parent_y + parent_height - toast_height - 60
            
            self.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass
    
    def _dismiss(self) -> None:
        """Dismiss the toast."""
        try:
            self.destroy()
        except tk.TclError:
            pass