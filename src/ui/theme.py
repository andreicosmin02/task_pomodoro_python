"""
UI Theme Configuration

Contains all colors, fonts, and styling constants used throughout the application.
Centralized theme management for easy customization.
"""


class Colors:
    """
    Application color palette.
    
    Dark grey theme inspired by Claude's interface.
    All colors are valid hex codes without alpha (tkinter compatible).
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BACKGROUNDS
    # ═══════════════════════════════════════════════════════════════════════════
    
    BG_PRIMARY = "#1a1a1a"      # Main background (darkest)
    BG_SECONDARY = "#2d2d2d"    # Secondary surfaces
    BG_TERTIARY = "#3d3d3d"     # Cards, buttons
    BG_HOVER = "#4a4a4a"        # Hover states
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ACCENT COLORS
    # ═══════════════════════════════════════════════════════════════════════════
    
    ACCENT_WARM = "#d97757"         # Primary warm accent (terracotta)
    ACCENT_WARM_HOVER = "#e08a6d"   # Warm accent hover state
    ACCENT_COOL = "#6b9fbe"         # Cool accent (blue) for rest mode
    ACCENT_COOL_HOVER = "#7db0cf"   # Cool accent hover state
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEXT COLORS
    # ═══════════════════════════════════════════════════════════════════════════
    
    TEXT_PRIMARY = "#f5f5f5"    # Primary text (almost white)
    TEXT_SECONDARY = "#a0a0a0"  # Secondary/muted text
    TEXT_MUTED = "#666666"      # Very muted/disabled text
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FUNCTIONAL COLORS
    # ═══════════════════════════════════════════════════════════════════════════
    
    SUCCESS = "#6bbd6b"         # Success states
    WARNING = "#e0a458"         # Warning states
    DANGER = "#cf6679"          # Danger/stop states
    DANGER_LIGHT = "#d98a99"    # Danger hover state
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UI ELEMENTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    BORDER = "#404040"          # Borders and dividers
    SNACKBAR_BG = "#383838"     # Toast/snackbar background


class Fonts:
    """
    Font configuration.
    
    Uses system fonts with fallbacks for cross-platform compatibility.
    """
    
    # Font families (with fallbacks)
    FAMILY_PRIMARY = "Segoe UI"      # Primary UI font
    FAMILY_MONO = "Consolas"         # Monospace for timer
    
    # Font sizes
    SIZE_SMALL = 10
    SIZE_NORMAL = 12
    SIZE_LARGE = 14
    SIZE_TITLE = 20
    SIZE_HEADING = 32
    SIZE_TIMER = 48


class Dimensions:
    """
    Common dimensions and spacing.
    """
    
    # Padding
    PADDING_SMALL = 8
    PADDING_NORMAL = 16
    PADDING_LARGE = 24
    
    # Button dimensions
    BUTTON_WIDTH = 90
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH_LARGE = 150
    BUTTON_HEIGHT_LARGE = 48
    
    # Corner radius
    CORNER_RADIUS = 12
    CORNER_RADIUS_SMALL = 4
    
    # Window
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 650
    WINDOW_MIN_WIDTH = 400
    WINDOW_MIN_HEIGHT = 500