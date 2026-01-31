import PyInstaller.__main__
import os

def build():
    print("Building executable...")
    
    # Ensure icon exists
    icon_path = "icon.png"
    if not os.path.exists(icon_path):
        print("Warning: icon.png not found. Building without icon.")
        icon_arg = []
    else:
        icon_arg = [f'--icon={icon_path}']

    PyInstaller.__main__.run([
        'main.py',
        '--name=ApplicationUsageTracker',
        '--onefile',
        '--noconsole',
        '--clean',
        '--add-data=icon.png;.',
        *icon_arg
    ])
    
    print("Build complete. Check 'dist/' folder.")

if __name__ == "__main__":
    build()
