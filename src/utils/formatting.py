"""
Formatting Utility Functions

Common formatting and calculation utilities.
"""


def format_duration(seconds: int) -> str:
    """
    Format seconds as HH:MM:SS string.
    
    Args:
        seconds: Total seconds to format
        
    Returns:
        Formatted string in HH:MM:SS format
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def calculate_rest_duration(
    work_seconds: int,
    min_rest_minutes: int = 5,
    rest_ratio: int = 5,
    work_ratio: int = 25,
) -> int:
    """
    Calculate rest duration based on work duration.
    
    Uses the Pomodoro ratio: 5 minutes rest per 25 minutes work.
    
    Args:
        work_seconds: Total seconds worked
        min_rest_minutes: Minimum rest duration in minutes
        rest_ratio: Minutes of rest earned per work_ratio
        work_ratio: Minutes of work needed to earn rest_ratio
        
    Returns:
        Rest duration in seconds
    """
    work_minutes = work_seconds // 60
    
    # Calculate rest minutes based on completed work periods
    rest_minutes = (work_minutes // work_ratio) * rest_ratio
    
    # Add rest for partial work period
    if work_minutes % work_ratio > 0:
        rest_minutes += rest_ratio
    
    # Ensure minimum rest duration
    rest_minutes = max(min_rest_minutes, rest_minutes)
    
    return rest_minutes * 60


def format_hours_text(hours: int) -> str:
    """
    Format hours with proper singular/plural form.
    
    Args:
        hours: Number of hours
        
    Returns:
        Formatted string like "1 hour" or "2 hours"
    """
    if hours == 1:
        return "1 hour"
    return f"{hours} hours"