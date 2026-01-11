"""
Main Application Class

The main Tkinter application window and page management.
"""

import tkinter as tk
from typing import Optional

from .state import AppState, TimerState, AppConfig
from .timer import TimerController
from ..ui.theme import Colors
from ..ui.widgets import ModernCheckbox, Toast
from ..ui.pages import StartingPage, WorkingPage, RestingPage, BasePage
from pathlib import Path
import platform
import ctypes


class TaskPomodoroApp(tk.Tk):
    """
    Main Pomodoro Timer Application.
    
    Manages the main window, page navigation, and application state.
    """
    
    def __init__(self):
        # On Windows, set an explicit AppUserModelID before creating the Tk root.
        # This helps Windows associate the running process with the executable's
        # icon (useful when packaged with PyInstaller). Call this before
        # `super().__init__()` so the taskbar grouping picks up the AppID.
        if platform.system() == "Windows":
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.taskpomodoro.app")
            except Exception:
                pass

        super().__init__()
        
        # Window configuration
        self.title("TaskPomodoro")
        self.geometry("500x650")
        self.minsize(400, 500)
        self.configure(bg=Colors.BG_PRIMARY)
        
        # Load application icon (prefer .ico for Windows taskbar, fallback to .png)
        try:
            project_root = Path(__file__).resolve().parents[2]
            ico_path = project_root / "assets" / "icon.ico"
            png_path = project_root / "assets" / "icon.png"
            if ico_path.exists():
                self.iconbitmap(str(ico_path))
            elif png_path.exists():
                photo = tk.PhotoImage(file=str(png_path))
                self._icon_photo = photo
                self.iconphoto(True, photo)
        except Exception:
            pass
        
        # Application state
        self.app_state = AppState.STARTING
        self.timer_state = TimerState()
        self.config = AppConfig()
        
        # Timer controller
        self.timer_controller: Optional[TimerController] = None
        
        # UI references
        self.current_page: Optional[BasePage] = None
        self.on_top_checkbox: Optional[ModernCheckbox] = None
        
        # Create UI
        self._create_bottom_bar()
        self._show_starting_page()
    
    def _create_bottom_bar(self) -> None:
        """Create the bottom bar with always-on-top checkbox."""
        self.bottom_bar = tk.Frame(self, bg=Colors.BG_PRIMARY, height=40)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=10)
        
        self.on_top_checkbox = ModernCheckbox(
            self.bottom_bar,
            text="Always on top",
            command=self._toggle_always_on_top,
            initial_state=False
        )
        self.on_top_checkbox.pack(side=tk.RIGHT)
    
    def _toggle_always_on_top(self, checked: bool) -> None:
        """Toggle window always on top."""
        self.config.always_on_top = checked
        self.attributes("-topmost", checked)
        if checked:
            self.show_toast("Window will stay on top")
    
    def show_toast(self, message: str) -> None:
        """Show a toast notification in the app."""
        Toast(self, message)
    
    def _clear_page(self) -> None:
        """Clear the current page."""
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE NAVIGATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _show_starting_page(self) -> None:
        """Show the starting page."""
        self._clear_page()
        self.app_state = AppState.STARTING
        
        self.current_page = StartingPage(
            self,
            on_start_work=self._show_working_page
        )
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def _show_working_page(self) -> None:
        """Show the working page."""
        self._clear_page()
        self.app_state = AppState.WORKING
        self.timer_state.reset()
        
        # Stop any existing timer
        if self.timer_controller:
            self.timer_controller.stop()
        
        self.current_page = WorkingPage(
            self,
            timer_state=self.timer_state,
            on_start=self._start_work_timer,
            on_pause=self._toggle_pause,
            on_stop=self._stop_and_reset,
            on_go_resting=self._show_resting_page
        )
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def _show_resting_page(self) -> None:
        """Show the resting page."""
        # Stop work timer
        if self.timer_controller:
            self.timer_controller.stop()
        
        self._clear_page()
        self.app_state = AppState.RESTING
        
        # Calculate rest duration
        self.timer_state.rest_seconds = self.config.calculate_rest_duration(
            self.timer_state.elapsed_seconds
        )
        self.timer_state.is_running = False
        self.timer_state.is_paused = False
        
        self.current_page = RestingPage(
            self,
            timer_state=self.timer_state,
            on_start=self._start_rest_timer,
            on_pause=self._toggle_pause,
            on_stop=self._stop_and_reset,
            on_skip=self._skip_resting
        )
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIMER CONTROLS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _start_work_timer(self) -> None:
        """Start the work timer."""
        self.timer_controller = TimerController(
            timer_state=self.timer_state,
            on_tick=lambda: self.after(0, self._update_display),
        )
        self.timer_controller.start_work_timer()
        
        if self.current_page:
            self.current_page.on_timer_started()
    
    def _start_rest_timer(self) -> None:
        """Start the rest timer."""
        self.timer_controller = TimerController(
            timer_state=self.timer_state,
            on_tick=lambda: self.after(0, self._update_display),
            on_complete=lambda: self.after(0, self._show_working_page),
        )
        self.timer_controller.start_rest_timer()
        
        if self.current_page:
            self.current_page.on_timer_started()
    
    def _toggle_pause(self) -> None:
        """Toggle timer pause state."""
        is_paused = self.timer_state.toggle_pause()
        if self.current_page:
            self.current_page.on_pause_toggled(is_paused)
    
    def _update_display(self) -> None:
        """Update the timer display."""
        if self.current_page:
            self.current_page.update_timer_display()
    
    def _stop_and_reset(self) -> None:
        """Stop timer and return to starting page."""
        if self.timer_controller:
            self.timer_controller.stop()
        self.timer_state.reset()
        self._show_starting_page()
    
    def _skip_resting(self) -> None:
        """Skip rest and go back to working."""
        if self.timer_controller:
            self.timer_controller.stop()
        self.timer_state.reset()
        self._show_working_page()
    
    def on_closing(self) -> None:
        """Handle window close event."""
        if self.timer_controller:
            self.timer_controller.stop()
        self.destroy()