import subprocess
import re

def get_monitors_xrandr():
    """Get monitor info using xrandr (Linux only)"""
    try:
        output = subprocess.check_output(['xrandr'], text=True)
        monitors = []
        
        # Parse xrandr output for connected monitors
        pattern = r'(\S+) connected (?:primary )?(\d+)x(\d+)\+(\d+)\+(\d+)'
        
        for match in re.finditer(pattern, output):
            name, width, height, x, y = match.groups()
            monitors.append({
                'name': name,
                'width': int(width),
                'height': int(height),
                'x': int(x),
                'y': int(y),
                'is_primary': 'primary' in match.group(0)
            })
        
        return monitors
    except Exception as e:
        print(f"Error getting monitors: {e}")
        return []
