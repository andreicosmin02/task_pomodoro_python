"""
Timer Controller Module

Handles the timer logic in a separate thread with callbacks for UI updates.
"""

import threading
import time
from typing import Callable, Optional

from .state import TimerState
from .notifications import send_notification, NotificationMessages


class TimerController:
    """
    Controls the timer logic in a background thread.
    
    This class manages the timer counting and triggers callbacks
    for UI updates and notifications.
    """
    
    def __init__(
        self,
        timer_state: TimerState,
        on_tick: Optional[Callable[[], None]] = None,
        on_complete: Optional[Callable[[], None]] = None,
        on_hour: Optional[Callable[[int], None]] = None,
    ):
        """
        Initialize the timer controller.
        
        Args:
            timer_state: The timer state object to manage
            on_tick: Callback called every second
            on_complete: Callback called when timer completes (rest mode)
            on_hour: Callback called on each hour milestone
        """
        self.timer_state = timer_state
        self.on_tick = on_tick
        self.on_complete = on_complete
        self.on_hour = on_hour
        
        self._stop_flag = threading.Event()
        self._thread: Optional[threading.Thread] = None
    
    def start_work_timer(self) -> None:
        """Start the work timer (counts up)."""
        self._stop()
        self.timer_state.start()
        self.timer_state.last_hour_notified = 0
        self._stop_flag.clear()
        
        self._thread = threading.Thread(target=self._work_loop, daemon=True)
        self._thread.start()
    
    def start_rest_timer(self) -> None:
        """Start the rest timer (counts down)."""
        self._stop()
        self.timer_state.start()
        self._stop_flag.clear()
        
        self._thread = threading.Thread(target=self._rest_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the timer."""
        self._stop()
        self.timer_state.is_running = False
        self.timer_state.is_paused = False
    
    def _stop(self) -> None:
        """Internal stop method."""
        self._stop_flag.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
    
    def _work_loop(self) -> None:
        """Main loop for work timer (counts up)."""
        while not self._stop_flag.is_set():
            if self.timer_state.is_running and not self.timer_state.is_paused:
                self.timer_state.increment_work()
                
                # Check for hourly notification
                if self.timer_state.should_notify_hour():
                    hours = self.timer_state.current_work_hour
                    title, message = NotificationMessages.hourly_update(hours)
                    send_notification(title, message)
                    
                    if self.on_hour:
                        self.on_hour(hours)
                
                if self.on_tick:
                    self.on_tick()
            
            time.sleep(1)
    
    def _rest_loop(self) -> None:
        """Main loop for rest timer (counts down)."""
        while not self._stop_flag.is_set() and self.timer_state.rest_seconds > 0:
            if self.timer_state.is_running and not self.timer_state.is_paused:
                is_complete = self.timer_state.decrement_rest()
                
                if self.on_tick:
                    self.on_tick()
                
                if is_complete:
                    title, message = NotificationMessages.rest_complete()
                    send_notification(title, message)
                    
                    if self.on_complete:
                        self.on_complete()
                    return
            
            time.sleep(1)
    
    @property
    def is_running(self) -> bool:
        """Check if timer thread is running."""
        return self._thread is not None and self._thread.is_alive()