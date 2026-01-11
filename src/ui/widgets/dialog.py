"""
Custom Dialog Widget

A themed confirmation dialog that matches the app's design.
"""

import tkinter as tk
import platform
from typing import Callable

from ..theme import Colors, Fonts
from .button import RoundedButton


class CustomDialog(tk.Toplevel):
    """
    Custom confirmation dialog.
    
    A modal dialog with custom styling that matches the app theme.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        message: str,
        on_confirm: Callable[[], None],
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
    ):
        """
        Initialize the dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
            message: Dialog message
            on_confirm: Callback when confirmed
            confirm_text: Text for confirm button
            cancel_text: Text for cancel button
        """
        super().__init__(parent)
        
        self._parent = parent
        self.on_confirm = on_confirm
        
        # Window setup
        self.title("Confirmation")
        self.configure(bg=Colors.BG_SECONDARY)
        self.resizable(False, False)
        
        # Make it modal and ensure visibility on Windows
        self.transient(parent)
        
        # On Windows, don't use overrideredirect for dialogs
        # as it can cause visibility/focus issues
        if platform.system() == "Windows":
            # Remove minimize/maximize buttons, keep close button
            self.attributes("-toolwindow", True)
        else:
            self.overrideredirect(True)
        
        # Ensure it stays on top
        self.attributes("-topmost", True)
        
        # Create outer border frame for visibility
        border_frame = tk.Frame(self, bg=Colors.BORDER, padx=2, pady=2)
        border_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main frame with padding
        main_frame = tk.Frame(border_frame, bg=Colors.BG_SECONDARY, padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=title,
            font=(Fonts.FAMILY_PRIMARY, 16, "bold"),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Message
        msg_label = tk.Label(
            main_frame,
            text=message,
            font=(Fonts.FAMILY_PRIMARY, 12),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_SECONDARY,
            wraplength=300,
            justify="left"
        )
        msg_label.pack(anchor="w", pady=(0, 25))
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg=Colors.BG_SECONDARY)
        btn_frame.pack(anchor="e")
        
        cancel_btn = RoundedButton(
            btn_frame,
            text=cancel_text,
            command=self._on_cancel,
            bg=Colors.BG_TERTIARY,
            hover_bg=Colors.BG_HOVER,
            width=90,
            height=36
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        confirm_btn = RoundedButton(
            btn_frame,
            text=confirm_text,
            command=self._on_confirm,
            bg=Colors.ACCENT_WARM,
            hover_bg=Colors.ACCENT_WARM_HOVER,
            width=90,
            height=36
        )
        confirm_btn.pack(side=tk.LEFT)
        
        # Force update and center on parent
        self.update_idletasks()
        self._center_on_parent()
        
        # Make modal - grab focus
        self.grab_set()
        self.focus_force()
        
        # Handle escape key and window close
        self.bind("<Escape>", lambda e: self._on_cancel())
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        # Lift to top
        self.lift()
    
    def _center_on_parent(self) -> None:
        """Center the dialog on the parent window."""
        try:
            parent_x = self._parent.winfo_rootx()
            parent_y = self._parent.winfo_rooty()
            parent_width = self._parent.winfo_width()
            parent_height = self._parent.winfo_height()
            
            dialog_width = self.winfo_width()
            dialog_height = self.winfo_height()
            
            x = parent_x + (parent_width - dialog_width) // 2
            y = parent_y + (parent_height - dialog_height) // 2
            
            self.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass
    
    def _on_cancel(self) -> None:
        """Handle cancel action."""
        self.grab_release()
        self.destroy()
    
    def _on_confirm(self) -> None:
        """Handle confirm action."""
        self.grab_release()
        self.destroy()
        self.on_confirm()