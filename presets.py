# presets.py - Stores predefined values for the settings editor.
"""
PRESETS CONFIGURATION FOR MUMU MANAGER
=====================================

This file contains predefined configurations for various device settings.
You can customize these presets to match your specific needs.

USAGE:
- These presets are used in the Settings Editor dialog
- Add new models/configurations as needed
- Follow the existing format for consistency

CATEGORIES:
1. Phone Models - Device identification presets
2. Performance Modes - CPU/GPU performance configurations  
3. Display Settings - Screen resolution and DPI presets
4. Memory Settings - RAM and storage configurations
5. Network Settings - Network simulation presets
6. Gaming Profiles - Optimized settings for gaming
7. Developer Tools - Development and testing configurations

CUSTOMIZATION GUIDE:
- To add new phone model: Add to appropriate brand in PHONE_MODELS
- To create custom profile: Add to CUSTOM_PROFILES with description
- To modify performance: Update PERFORMANCE_MODES values
- Always test new configurations before deploying
"""

# =====================================================================
# DEVICE IDENTIFICATION PRESETS
# =====================================================================

PHONE_MODELS = {
    "Samsung": {
        "flagship": [
            {"model": "SM-S918B", "name": "Galaxy S23 Ultra", "year": 2023},
            {"model": "SM-S916B", "name": "Galaxy S23+", "year": 2023},
            {"model": "SM-S911B", "name": "Galaxy S23", "year": 2023},
            {"model": "SM-F946B", "name": "Galaxy Z Fold 5", "year": 2023},
            {"model": "SM-F731B", "name": "Galaxy Z Flip 5", "year": 2023},
        ],
        "mid_range": [
            {"model": "SM-A546E", "name": "Galaxy A54", "year": 2023},
            {"model": "SM-A536E", "name": "Galaxy A53", "year": 2022},
            {"model": "SM-A346E", "name": "Galaxy A34", "year": 2023},
        ],
        "budget": [
            {"model": "SM-A146B", "name": "Galaxy A14", "year": 2023},
            {"model": "SM-A047F", "name": "Galaxy A04s", "year": 2022},
        ]
    },
    "Xiaomi": {
        "flagship": [
            {"model": "23021RAA2Y", "name": "Xiaomi 13 Pro", "year": 2023},
            {"model": "2210132G", "name": "Xiaomi 13", "year": 2023},
            {"model": "2301123G", "name": "Xiaomi 13 Ultra", "year": 2023},
        ],
        "gaming": [
            {"model": "23078PND5G", "name": "Black Shark 5 Pro", "year": 2023},
            {"model": "23021211RG", "name": "Poco F5", "year": 2023},
            {"model": "22101316G", "name": "Poco F4 GT", "year": 2022},
        ],
        "mid_range": [
            {"model": "2201116SG", "name": "Redmi Note 11 Pro", "year": 2022},
            {"model": "23021RAAEG", "name": "Redmi Note 12 Pro", "year": 2023},
        ]
    },
    "Google": {
        "pixel": [
            {"model": "GC3VE", "name": "Pixel 8 Pro", "year": 2023},
            {"model": "GKWS6", "name": "Pixel 8", "year": 2023},
            {"model": "G0DZQ", "name": "Pixel 7a", "year": 2023},
            {"model": "G9FPL", "name": "Pixel Fold", "year": 2023},
            {"model": "GF5KQ", "name": "Pixel 6", "year": 2021},
        ]
    },
    "OnePlus": {
        "flagship": [
            {"model": "CPH2581", "name": "OnePlus 11", "year": 2023},
            {"model": "NE2213", "name": "OnePlus 10 Pro", "year": 2022},
            {"model": "DE2117", "name": "OnePlus 9RT", "year": 2021},
        ]
    },
    "ASUS": {
        "gaming": [
            {"model": "AI2201_D", "name": "ROG Phone 6", "year": 2022},
            {"model": "ASUS_I007D", "name": "ROG Phone 5s", "year": 2021},
            {"model": "ASUS_I003DD", "name": "ROG Phone 3", "year": 2020},
        ]
    },
    "Apple": {
        "iphone": [
            {"model": "iPhone15,3", "name": "iPhone 14 Pro Max", "year": 2022},
            {"model": "iPhone15,2", "name": "iPhone 14 Pro", "year": 2022},
            {"model": "iPhone14,3", "name": "iPhone 13 Pro Max", "year": 2021},
        ]
    }
}

# =====================================================================
# PERFORMANCE CONFIGURATION PRESETS
# =====================================================================

PERFORMANCE_MODES = {
    "low_power": {
        "name": "Tiết kiệm pin",
        "description": "Giảm hiệu suất để tiết kiệm tài nguyên",
        "cpu_cores": 2,
        "cpu_frequency": "1.2GHz",
        "gpu_mode": "low",
        "ram_limit": "2GB",
        "recommended_for": "Ứng dụng văn phòng, đọc tin tức"
    },
    "balanced": {
        "name": "Cân bằng",
        "description": "Cân bằng giữa hiệu suất và tiết kiệm tài nguyên",
        "cpu_cores": 4,
        "cpu_frequency": "2.0GHz", 
        "gpu_mode": "medium",
        "ram_limit": "4GB",
        "recommended_for": "Sử dụng hàng ngày, ứng dụng thông thường"
    },
    "high_performance": {
        "name": "Hiệu suất cao",
        "description": "Tối đa hiệu suất cho các tác vụ nặng",
        "cpu_cores": 8,
        "cpu_frequency": "3.0GHz",
        "gpu_mode": "high", 
        "ram_limit": "8GB",
        "recommended_for": "Gaming, rendering, ứng dụng đồ họa"
    },
    "gaming_optimized": {
        "name": "Tối ưu gaming",
        "description": "Cấu hình đặc biệt cho game",
        "cpu_cores": 8,
        "cpu_frequency": "3.2GHz",
        "gpu_mode": "ultra",
        "ram_limit": "12GB", 
        "frame_rate": "120fps",
        "recommended_for": "Game mobile cao cấp, streaming"
    }
}

# =====================================================================
# DISPLAY CONFIGURATION PRESETS  
# =====================================================================

DISPLAY_PRESETS = {
    "resolutions": {
        "hd": {"width": 1280, "height": 720, "dpi": 160, "name": "HD (720p)"},
        "fhd": {"width": 1920, "height": 1080, "dpi": 240, "name": "Full HD (1080p)"},
        "qhd": {"width": 2560, "height": 1440, "dpi": 320, "name": "QHD (1440p)"},
        "4k": {"width": 3840, "height": 2160, "dpi": 480, "name": "4K UHD"},
        "custom_tablet": {"width": 2048, "height": 1536, "dpi": 264, "name": "Tablet 4:3"},
    },
    "orientations": ["portrait", "landscape", "auto"],
    "refresh_rates": [60, 90, 120, 144],
}

# =====================================================================
# MEMORY CONFIGURATION PRESETS
# =====================================================================

MEMORY_PRESETS = {
    "configurations": {
        "basic": {"ram": "2GB", "storage": "32GB", "name": "Cơ bản"},
        "standard": {"ram": "4GB", "storage": "64GB", "name": "Tiêu chuẩn"},
        "premium": {"ram": "8GB", "storage": "128GB", "name": "Cao cấp"},
        "pro": {"ram": "12GB", "storage": "256GB", "name": "Chuyên nghiệp"},
        "max": {"ram": "16GB", "storage": "512GB", "name": "Tối đa"},
    },
    "swap_settings": {
        "disabled": {"size": "0MB", "priority": 0},
        "minimal": {"size": "512MB", "priority": 1},
        "moderate": {"size": "1GB", "priority": 5},
        "aggressive": {"size": "2GB", "priority": 10},
    }
}

# =====================================================================
# NETWORK SIMULATION PRESETS
# =====================================================================

NETWORK_PRESETS = {
    "connection_types": {
        "wifi_fast": {
            "name": "WiFi Nhanh",
            "download": "100Mbps",
            "upload": "50Mbps", 
            "latency": "10ms",
            "packet_loss": "0%"
        },
        "wifi_normal": {
            "name": "WiFi Thường",
            "download": "25Mbps",
            "upload": "5Mbps",
            "latency": "50ms", 
            "packet_loss": "0.1%"
        },
        "4g_good": {
            "name": "4G Tốt",
            "download": "20Mbps",
            "upload": "10Mbps",
            "latency": "100ms",
            "packet_loss": "0.5%"
        },
        "3g_slow": {
            "name": "3G Chậm",
            "download": "1Mbps",
            "upload": "500Kbps",
            "latency": "300ms",
            "packet_loss": "2%"
        }
    },
    "locations": {
        "vietnam": {"country": "VN", "timezone": "Asia/Ho_Chi_Minh"},
        "usa": {"country": "US", "timezone": "America/New_York"},
        "japan": {"country": "JP", "timezone": "Asia/Tokyo"},
        "singapore": {"country": "SG", "timezone": "Asia/Singapore"},
    }
}

# =====================================================================
# GAMING OPTIMIZATION PROFILES
# =====================================================================

GAMING_PROFILES = {
    "fps_games": {
        "name": "FPS Games",
        "description": "Tối ưu cho game bắn súng",
        "settings": {
            "frame_rate": 120,
            "graphics": "high",
            "anti_aliasing": True,
            "vsync": False,
            "input_lag": "minimal"
        },
        "recommended_games": ["PUBG Mobile", "Call of Duty Mobile", "Free Fire"]
    },
    "moba_games": {
        "name": "MOBA Games", 
        "description": "Tối ưu cho game chiến thuật",
        "settings": {
            "frame_rate": 90,
            "graphics": "medium",
            "effects": "reduced",
            "network_priority": "high"
        },
        "recommended_games": ["Liên Quân Mobile", "Mobile Legends", "Wild Rift"]
    },
    "rpg_games": {
        "name": "RPG Games",
        "description": "Tối ưu cho game nhập vai",
        "settings": {
            "frame_rate": 60,
            "graphics": "ultra",
            "effects": "full",
            "loading_speed": "fast"
        },
        "recommended_games": ["Genshin Impact", "Honkai Impact", "Epic Seven"]
    }
}

# =====================================================================
# DEVELOPER & TESTING PRESETS
# =====================================================================

DEVELOPER_PRESETS = {
    "debug_modes": {
        "adb_enabled": True,
        "usb_debugging": True,
        "developer_options": True,
        "mock_locations": True,
    },
    "testing_environments": {
        "automation": {
            "name": "Test Automation",
            "accessibility_service": True,
            "keep_screen_on": True,
            "disable_animations": True,
        },
        "performance_testing": {
            "name": "Performance Testing",
            "gpu_profiling": True,
            "memory_profiling": True,
            "network_monitoring": True,
        }
    }
}

# =====================================================================
# CUSTOM PROFILES TEMPLATES
# =====================================================================

CUSTOM_PROFILES = {
    "social_media": {
        "name": "Social Media Optimization",
        "description": "Tối ưu cho ứng dụng mạng xã hội",
        "device_model": "SM-A546E",  # Galaxy A54
        "performance": "balanced",
        "network": "wifi_normal",
        "recommended_apps": ["Facebook", "Instagram", "TikTok", "Zalo"]
    },
    "productivity": {
        "name": "Productivity Suite",
        "description": "Tối ưu cho công việc văn phòng",
        "device_model": "CPH2581",  # OnePlus 11
        "performance": "balanced", 
        "memory": "premium",
        "recommended_apps": ["Microsoft Office", "Google Workspace", "Notion"]
    },
    "content_creation": {
        "name": "Content Creation",
        "description": "Tối ưu cho tạo nội dung",
        "device_model": "GC3VE",  # Pixel 8 Pro
        "performance": "high_performance",
        "display": "qhd",
        "recommended_apps": ["CapCut", "Lightroom", "Canva"]
    }
}

# =====================================================================
# UTILITY FUNCTIONS
# =====================================================================

def get_all_phone_models():
    """Get flattened list of all phone models"""
    models = []
    for brand, categories in PHONE_MODELS.items():
        for category, devices in categories.items():
            for device in devices:
                models.append({
                    "brand": brand,
                    "category": category,
                    "model": device["model"],
                    "name": device["name"],
                    "year": device["year"]
                })
    return models

def get_models_by_brand(brand):
    """Get all models for a specific brand"""
    if brand in PHONE_MODELS:
        return PHONE_MODELS[brand]
    return {}

def get_performance_recommendations(use_case):
    """Get performance recommendations based on use case"""
    recommendations = {
        "gaming": PERFORMANCE_MODES["gaming_optimized"],
        "work": PERFORMANCE_MODES["balanced"],
        "basic": PERFORMANCE_MODES["low_power"],
        "development": PERFORMANCE_MODES["high_performance"]
    }
    return recommendations.get(use_case, PERFORMANCE_MODES["balanced"])

def get_preset_by_name(preset_name):
    """Get custom profile by name"""
    return CUSTOM_PROFILES.get(preset_name, {})

# =====================================================================
# CONFIGURATION VALIDATION
# =====================================================================

def validate_configuration(config):
    """Validate configuration against available presets"""
    valid = True
    errors = []
    
    # Validate device model
    all_models = [device["model"] for device in get_all_phone_models()]
    if config.get("device_model") not in all_models:
        errors.append(f"Invalid device model: {config.get('device_model')}")
        valid = False
    
    # Validate performance mode
    if config.get("performance") not in PERFORMANCE_MODES:
        errors.append(f"Invalid performance mode: {config.get('performance')}")
        valid = False
    
    return valid, errors

# =====================================================================
# USAGE EXAMPLES & DOCUMENTATION
# =====================================================================

"""
USAGE EXAMPLES:
==============

1. Get all Samsung flagship models:
   models = PHONE_MODELS["Samsung"]["flagship"]

2. Get performance settings for gaming:
   gaming_config = PERFORMANCE_MODES["gaming_optimized"]

3. Get recommended display settings:
   display = DISPLAY_PRESETS["resolutions"]["fhd"]

4. Create custom profile:
   my_profile = {
       "name": "My Custom Profile",
       "device_model": "SM-S918B",  # Galaxy S23 Ultra
       "performance": "high_performance",
       "display": "qhd",
       "network": "wifi_fast"
   }

5. Validate configuration:
   valid, errors = validate_configuration(my_profile)

EXTENDING PRESETS:
=================

To add new presets:
1. Follow existing dictionary structure
2. Include name, description, and settings
3. Add validation if needed
4. Update documentation
5. Test thoroughly before deployment

BEST PRACTICES:
==============

- Always include descriptions for new presets
- Use consistent naming conventions
- Test configurations before adding
- Document recommended use cases
- Keep presets organized by category
"""
