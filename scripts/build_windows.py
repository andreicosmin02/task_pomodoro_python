#!/usr/bin/env python3
"""
Windows Build Script for TaskPomodoro

This script builds the TaskPomodoro application into a standalone
Windows executable using PyInstaller.

Usage:
    python scripts/build_windows.py [--onefile] [--console]

Options:
    --onefile   Create a single executable file (default: True)
    --console   Show console window (default: False, windowed mode)
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
import platform
import os


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def check_pyinstaller() -> bool:
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller() -> bool:
    """Install PyInstaller."""
    print("Installing PyInstaller...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pyinstaller"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def clean_build_dirs(project_root: Path) -> None:
    """Clean previous build directories."""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"Cleaning {dir_path}...")
            shutil.rmtree(dir_path)
    
    # Clean .spec files
    for spec_file in project_root.glob("*.spec"):
        print(f"Removing {spec_file}...")
        spec_file.unlink()


def create_icon_if_missing(project_root: Path) -> Path:
    """Create a placeholder icon if none exists."""
    icon_path = project_root / "assets" / "icon.ico"
    png_path = project_root / "assets" / "icon.png"

    # If .ico exists, use it
    if icon_path.exists():
        return icon_path

    # If only PNG exists, try to convert to .ico using Pillow
    if png_path.exists():
        try:
            from PIL import Image
            img = Image.open(png_path)
            # Save multiple sizes into the ICO file for compatibility
            img.save(icon_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
            print(f"Created {icon_path} from {png_path}")
            return icon_path
        except ImportError:
            print("Pillow not installed; cannot convert PNG to ICO.")
            print("Place an icon.ico in assets/ to use a custom icon.")
            return None
        except Exception as e:
            print(f"Failed to create icon.ico: {e}")
            return None

    print("Note: No icon.ico or icon.png found in assets/")
    print("The build will proceed without a custom icon.")
    return None


def build_executable(
    project_root: Path,
    onefile: bool = True,
    console: bool = False,
) -> bool:
    """
    Build the Windows executable.
    
    Args:
        project_root: Project root directory
        onefile: Create single file executable
        console: Show console window
        
    Returns:
        True if build succeeded
    """
    main_script = project_root / "src" / "main.py"
    
    if not main_script.exists():
        print(f"Error: Main script not found: {main_script}")
        return False
    
    # Build PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=TaskPomodoro",
        "--clean",
    ]
    
    # Add onefile option
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # Add windowed mode
    if not console:
        cmd.append("--windowed")
    
    # Add icon if exists (use resolved string path)
    icon_path = create_icon_if_missing(project_root)
    if icon_path:
        cmd.append(f"--icon={str(icon_path.resolve())}")

    # Ensure assets folder is bundled so runtime can access images/icons
    # PyInstaller expects path spec as SRC;DEST on Windows and SRC:DEST on POSIX
    sep = ";" if platform.system() == "Windows" else ":"
    assets_src = str((project_root / "assets").resolve())
    cmd.append(f"--add-data={assets_src}{sep}assets")
    
    # Add paths
    cmd.extend([
        f"--paths={project_root}",
        f"--paths={project_root / 'src'}",
    ])
    
    # Add hidden imports (for modules that might not be detected)
    hidden_imports = [
        "src.core",
        "src.core.app",
        "src.core.state",
        "src.core.timer",
        "src.core.notifications",
        "src.ui",
        "src.ui.theme",
        "src.ui.widgets",
        "src.ui.widgets.button",
        "src.ui.widgets.checkbox",
        "src.ui.widgets.clock_icon",
        "src.ui.widgets.toast",
        "src.ui.widgets.dialog",
        "src.ui.pages",
        "src.ui.pages.base_page",
        "src.ui.pages.starting_page",
        "src.ui.pages.working_page",
        "src.ui.pages.resting_page",
        "src.utils",
        "src.utils.formatting",
    ]
    
    for imp in hidden_imports:
        cmd.append(f"--hidden-import={imp}")
    
    # Add the main script
    cmd.append(str(main_script))
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Run PyInstaller
    result = subprocess.run(cmd, cwd=project_root)
    
    return result.returncode == 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build TaskPomodoro for Windows"
    )
    parser.add_argument(
        "--onefile",
        action="store_true",
        default=True,
        help="Create a single executable file (default)"
    )
    parser.add_argument(
        "--onedir",
        action="store_true",
        help="Create a directory with executable and dependencies"
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help="Show console window (for debugging)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build directories before building"
    )
    
    args = parser.parse_args()
    
    project_root = get_project_root()
    print(f"Project root: {project_root}")
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found.")
        if not install_pyinstaller():
            print("Failed to install PyInstaller!")
            sys.exit(1)
    
    # Clean if requested
    if args.clean:
        clean_build_dirs(project_root)
    
    # Determine onefile setting
    onefile = not args.onedir
    
    # Build
    success = build_executable(
        project_root,
        onefile=onefile,
        console=args.console
    )
    
    if success:
        print()
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        
        dist_path = project_root / "dist"
        if onefile:
            exe_path = dist_path / "TaskPomodoro.exe"
        else:
            exe_path = dist_path / "TaskPomodoro" / "TaskPomodoro.exe"
        
        print(f"Executable: {exe_path}")
        print()
        print("You can now distribute the executable!")
    else:
        print()
        print("BUILD FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()