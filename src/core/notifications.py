"""
System Notifications Module

Cross-platform notification support for Windows, macOS, and Linux.
"""

import platform
import subprocess
from typing import Optional


def send_notification(title: str, message: str) -> bool:
    """
    Send a system notification.
    
    Args:
        title: Notification title
        message: Notification message body
        
    Returns:
        True if notification was sent successfully, False otherwise
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            return _send_windows_notification(title, message)
        elif system == "Darwin":
            return _send_macos_notification(title, message)
        elif system == "Linux":
            return _send_linux_notification(title, message)
        else:
            print(f"Unsupported platform for notifications: {system}")
            return False
    except Exception as e:
        print(f"Notification error: {e}")
        return False


def _send_windows_notification(title: str, message: str) -> bool:
    """Send notification on Windows using PowerShell."""
    # Escape quotes for PowerShell
    safe_title = title.replace("'", "''").replace('"', '`"')
    safe_message = message.replace("'", "''").replace('"', '`"')
    
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    $balloon = New-Object System.Windows.Forms.NotifyIcon
    $balloon.Icon = [System.Drawing.SystemIcons]::Information
    $balloon.BalloonTipIcon = "Info"
    $balloon.BalloonTipTitle = "{safe_title}"
    $balloon.BalloonTipText = "{safe_message}"
    $balloon.Visible = $true
    $balloon.ShowBalloonTip(5000)
    Start-Sleep -Seconds 5
    $balloon.Dispose()
    '''
    
    try:
        # CREATE_NO_WINDOW flag
        creation_flags = 0x08000000
        subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", ps_script],
            creationflags=creation_flags
        )
        return True
    except FileNotFoundError:
        # PowerShell not available, try win10toast
        return _send_windows_notification_fallback(title, message)
    except Exception:
        return _send_windows_notification_fallback(title, message)


def _send_windows_notification_fallback(title: str, message: str) -> bool:
    """Fallback Windows notification using win10toast if available."""
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5, threaded=True)
        return True
    except ImportError:
        print("win10toast not installed. Install with: pip install win10toast")
        return False
    except Exception as e:
        print(f"win10toast error: {e}")
        return False


def _send_macos_notification(title: str, message: str) -> bool:
    """Send notification on macOS using osascript."""
    # Escape quotes for AppleScript
    safe_title = title.replace('"', '\\"')
    safe_message = message.replace('"', '\\"')
    
    script = f'display notification "{safe_message}" with title "{safe_title}"'
    
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("osascript not found")
        return False


def _send_linux_notification(title: str, message: str) -> bool:
    """Send notification on Linux using notify-send."""
    try:
        result = subprocess.run(
            ["notify-send", title, message],
            capture_output=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("notify-send not found. Install with: sudo apt install libnotify-bin")
        return False


# Notification message templates
class NotificationMessages:
    """Pre-defined notification messages."""
    
    @staticmethod
    def hourly_update(hours: int) -> tuple[str, str]:
        """Generate hourly work update notification."""
        hours_text = "hour" if hours == 1 else "hours"
        return (
            "TaskPomodoro - Work Update",
            f"You have been working for {hours} {hours_text}! Keep it up!"
        )
    
    @staticmethod
    def rest_complete() -> tuple[str, str]:
        """Generate rest complete notification."""
        return (
            "TaskPomodoro - Rest Complete!",
            "Your rest time is over. Time to get back to work!"
        )
    
    @staticmethod
    def work_session_complete(minutes: int) -> tuple[str, str]:
        """Generate work session complete notification."""
        return (
            "TaskPomodoro - Great Work!",
            f"You completed a {minutes} minute work session. Time for a break!"
        )