"""
Application State Management

This module contains the state classes used throughout the application.
Using dataclasses for clean, type-safe state management.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional


class AppState(Enum):
    """Represents the current page/state of the application."""
    
    STARTING = auto()
    WORKING = auto()
    RESTING = auto()


@dataclass
class TimerState:
    """
    Holds the current state of the timer.
    
    Attributes:
        is_running: Whether the timer is actively counting
        is_paused: Whether the timer is paused
        elapsed_seconds: Total seconds elapsed during work
        rest_seconds: Remaining seconds for rest period
        last_hour_notified: Track which hour was last notified
    """
    
    is_running: bool = False
    is_paused: bool = False
    elapsed_seconds: int = 0
    rest_seconds: int = 0
    last_hour_notified: int = 0
    
    def reset(self) -> None:
        """Reset the timer state to initial values."""
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0
        self.rest_seconds = 0
        self.last_hour_notified = 0
    
    def start(self) -> None:
        """Start the timer."""
        self.is_running = True
        self.is_paused = False
    
    def pause(self) -> None:
        """Pause the timer."""
        self.is_paused = True
    
    def resume(self) -> None:
        """Resume the timer."""
        self.is_paused = False
    
    def toggle_pause(self) -> bool:
        """Toggle pause state. Returns new pause state."""
        self.is_paused = not self.is_paused
        return self.is_paused
    
    def increment_work(self) -> None:
        """Increment work timer by one second."""
        self.elapsed_seconds += 1
    
    def decrement_rest(self) -> bool:
        """Decrement rest timer by one second. Returns True if rest is complete."""
        self.rest_seconds -= 1
        return self.rest_seconds <= 0
    
    @property
    def current_work_hour(self) -> int:
        """Get the current hour of work (0-indexed)."""
        return self.elapsed_seconds // 3600
    
    def should_notify_hour(self) -> bool:
        """Check if we should send an hourly notification."""
        current_hour = self.current_work_hour
        if current_hour > self.last_hour_notified:
            self.last_hour_notified = current_hour
            return True
        return False


@dataclass
class AppConfig:
    """
    Application configuration settings.
    
    Attributes:
        always_on_top: Whether window should stay on top
        min_rest_minutes: Minimum rest duration in minutes
        rest_ratio: Rest minutes per work_ratio minutes
        work_ratio: Work minutes that earn rest_ratio rest minutes
    """
    
    always_on_top: bool = False
    min_rest_minutes: int = 5
    rest_ratio: int = 5
    work_ratio: int = 25
    
    def calculate_rest_duration(self, work_seconds: int) -> int:
        """Calculate rest duration in seconds based on work duration."""
        work_minutes = work_seconds // 60
        rest_minutes = (work_minutes // self.work_ratio) * self.rest_ratio
        if work_minutes % self.work_ratio > 0:
            rest_minutes += self.rest_ratio
        return max(self.min_rest_minutes, rest_minutes) * 60