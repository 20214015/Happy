# feather_icons.py - Tiện ích để render Feather-style icons với qtawesome và màu sắc Monokai

import qtawesome as qta
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication
from typing import Dict, Optional

# Cache icons to improve performance
_icon_cache: Dict[str, QIcon] = {}

# Bảng màu đặc trưng của Monokai
MONOKAI_COLORS = {
    "foreground": "#F8F8F2",
    "green": "#A6E22E",
    "pink": "#F92672",
    "blue": "#66D9EF",
    "orange": "#FD971F",
    "purple": "#AE81FF",
    "yellow": "#E6DB74",
    "red": "#F92672"
}

# Ánh xạ tên icon sang màu sắc Monokai tương ứng
MONOKAI_COLOR_MAP = {
    # Hành động tích cực (xanh lá)
    "play": MONOKAI_COLORS["green"], "run": MONOKAI_COLORS["green"], "add": MONOKAI_COLORS["green"],
    "clone": MONOKAI_COLORS["green"], "save": MONOKAI_COLORS["green"], "plus": MONOKAI_COLORS["green"],
    "check": MONOKAI_COLORS["green"], "success": MONOKAI_COLORS["green"],
    
    # Hành động dừng/xóa (đỏ/hồng)
    "stop": MONOKAI_COLORS["pink"], "delete": MONOKAI_COLORS["pink"], "cleanup": MONOKAI_COLORS["pink"],
    "trash": MONOKAI_COLORS["pink"], "close": MONOKAI_COLORS["pink"], "remove": MONOKAI_COLORS["pink"],
    
    # Hành động làm mới/khởi động lại (xanh dương)
    "restart": MONOKAI_COLORS["blue"], "refresh": MONOKAI_COLORS["blue"], "sync": MONOKAI_COLORS["blue"],
    "reload": MONOKAI_COLORS["blue"], "update": MONOKAI_COLORS["blue"],
    
    # Chỉnh sửa/cấu hình (cam)
    "edit": MONOKAI_COLORS["orange"], "config": MONOKAI_COLORS["orange"],
    "settings": MONOKAI_COLORS["orange"], "theme": MONOKAI_COLORS["orange"],
    "tools": MONOKAI_COLORS["orange"], "gear": MONOKAI_COLORS["orange"],
    
    # Tự động hóa/script (tím)
    "automation": MONOKAI_COLORS["purple"], "script": MONOKAI_COLORS["purple"],
    "code": MONOKAI_COLORS["purple"], "terminal": MONOKAI_COLORS["purple"],
    
    # Cảnh báo (vàng)
    "warning": MONOKAI_COLORS["yellow"], "alert": MONOKAI_COLORS["yellow"],
    
    # Mặc định
    "dashboard": MONOKAI_COLORS["foreground"], "home": MONOKAI_COLORS["foreground"],
    "apps": MONOKAI_COLORS["foreground"], "folder": MONOKAI_COLORS["foreground"],
}

# Ánh xạ tên icon sang Material Design Icons (Feather-style) - Verified working icons
FEATHER_ICON_MAP = {
    # Giao diện chính
    "app_icon": "mdi.database", 
    "dashboard": "mdi.home", 
    "apps": "mdi.view-grid",
    "home": "mdi.home",
    
    # Điều khiển instance
    "play": "mdi.play", 
    "stop": "mdi.stop", 
    "pause": "mdi.pause",
    "restart": "mdi.restart",
    "run": "mdi.play",
    
    # Quản lý
    "add": "mdi.plus", 
    "clone": "mdi.content-copy", 
    "delete": "mdi.delete",
    "cleanup": "mdi.broom",
    "remove": "mdi.minus",
    "trash": "mdi.delete",
    
    # Chỉnh sửa & cấu hình  
    "edit": "mdi.pencil", 
    "config": "mdi.cog", 
    "settings": "mdi.cog",
    "theme": "mdi.palette",
    "tools": "mdi.wrench",
    "gear": "mdi.cog",
    
    # Làm mới & đồng bộ
    "refresh": "mdi.refresh", 
    "sync": "mdi.sync",
    "reload": "mdi.refresh",
    "update": "mdi.update",
    
    # File & folder
    "folder": "mdi.folder", 
    "save": "mdi.content-save",
    "file": "mdi.file",
    
    # Code & script
    "adb": "mdi.code-braces", 
    "script": "mdi.script-text", 
    "automation": "mdi.robot",
    "code": "mdi.code-tags",
    "terminal": "mdi.console",
    
    # Trạng thái
    "success": "mdi.check-circle",
    "check": "mdi.check",
    "warning": "mdi.alert",
    "alert": "mdi.alert-circle",
    "error": "mdi.alert-circle",
    "info": "mdi.information",
    
    # UI Elements
    "close": "mdi.close",
    "plus": "mdi.plus",
    "minus": "mdi.minus",
    "search": "mdi.magnify",
    "filter": "mdi.filter",
    "sort": "mdi.sort",
}

def get_icon(name: str, color: str = None) -> QIcon:
    """
    Tạo một QIcon bằng Feather-style icons với qtawesome, tự động áp dụng màu Monokai.
    Uses caching to improve performance.
    :param name: Tên của icon (ví dụ: 'play', 'settings').
    :param color: (Tùy chọn) Ghi đè màu mặc định.
    :return: Một đối tượng QIcon.
    """
    # Create cache key
    cache_key = f"{name}_{color or 'auto'}"
    
    # Return cached icon if available
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    
    # Sử dụng Feather-style icons (Material Design Icons)
    icon_name = FEATHER_ICON_MAP.get(name, "mdi.help-circle")
    final_color = color
    
    if final_color is None:
        try:
            # Đọc theme hiện tại từ QSettings
            settings = QSettings()
            theme_name = settings.value("theme/name", "monokai")  # Default to monokai
            
            if theme_name == "monokai":
                final_color = MONOKAI_COLOR_MAP.get(name, MONOKAI_COLORS["foreground"])
            else:
                # Safe palette access cho các theme khác
                try:
                    final_color = QApplication.palette().color(QApplication.palette().ColorRole.WindowText).name()
                except Exception:
                    final_color = MONOKAI_COLORS["foreground"]  # Fallback to Monokai foreground
        except Exception as e:
            print(f"Warning: Settings access failed for icon '{name}': {e}")
            final_color = MONOKAI_COLORS["foreground"]  # Fallback to Monokai foreground

    try:
        icon = qta.icon(icon_name, color=final_color)
        # Cache the icon for future use
        _icon_cache[cache_key] = icon
        return icon
    except Exception as e:
        print(f"Lỗi khi tạo Feather icon '{name}' (mdi name: '{icon_name}'): {e}")
        # Fallback to Font Awesome if MDI not available
        try:
            fallback_name = name.replace('-', '_')
            fallback_icon_name = f"fa5s.{fallback_name}"
            fallback_icon = qta.icon(fallback_icon_name, color=final_color)
            _icon_cache[cache_key] = fallback_icon
            return fallback_icon
        except:
            # Create and cache a fallback empty icon
            fallback_icon = QIcon()
            _icon_cache[cache_key] = fallback_icon
            return fallback_icon

def clear_icon_cache():
    """Clear the icon cache to free memory"""
    global _icon_cache
    _icon_cache.clear()

def get_cache_stats() -> Dict[str, int]:
    """Get icon cache statistics"""
    return {
        'cached_icons': len(_icon_cache),
        'memory_estimate_kb': len(_icon_cache) * 4  # Rough estimate
    }

def get_available_icons() -> Dict[str, str]:
    """Get all available Feather-style icons with their MDI mappings"""
    return FEATHER_ICON_MAP.copy()

def get_themed_color(icon_name: str, theme: str = "monokai") -> str:
    """Get the themed color for a specific icon"""
    if theme == "monokai":
        return MONOKAI_COLOR_MAP.get(icon_name, MONOKAI_COLORS["foreground"])
    return "#000000"  # Default for other themes

def set_default_theme(theme_name: str):
    """Set default theme for icon coloring"""
    try:
        settings = QSettings()
        settings.setValue("theme/name", theme_name)
        # Clear cache to apply new theme
        clear_icon_cache()
    except Exception as e:
        print(f"Warning: Could not set theme '{theme_name}': {e}")

# Test function to verify icon availability
def test_feather_icons() -> Dict[str, bool]:
    """Test if Feather-style icons are available"""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QCoreApplication
    import sys
    
    # Ensure we have an application instance
    if not QCoreApplication.instance():
        app = QApplication(sys.argv)
    
    test_icons = ['home', 'play', 'stop', 'settings', 'edit', 'refresh']
    results = {}
    
    for icon_name in test_icons:
        try:
            icon = get_icon(icon_name)
            results[icon_name] = not icon.isNull()
        except Exception as e:
            results[icon_name] = False
            print(f"Error testing icon '{icon_name}': {e}")
    
    return results