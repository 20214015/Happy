#!/usr/bin/env python3
"""
⚙️ AI Configuration Manager
===========================

Centralized configuration management for AI optimization features:
- Dynamic configuration updates
- Feature toggles
- Performance tuning
- Advanced settings
- Configuration persistence
"""

import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class AIConfiguration:
    """Comprehensive AI configuration"""
    
    # Core AI Settings
    learning_enabled: bool = True
    prediction_enabled: bool = True
    enhanced_features_enabled: bool = True
    
    # Learning Parameters
    learning_rate: float = 0.01
    confidence_threshold: float = 0.6
    pattern_memory_size: int = 1000
    prediction_horizon: int = 300  # seconds
    
    # Optimization Levels
    optimization_level: str = "adaptive"  # basic, adaptive, aggressive
    auto_optimization_enabled: bool = True
    proactive_optimization: bool = True
    
    # Performance Settings
    prediction_interval: int = 10000  # milliseconds
    monitoring_interval: int = 2000   # milliseconds
    resource_check_interval: int = 5000  # milliseconds
    
    # Enhanced ML Features
    enhanced_ml_enabled: bool = True
    intelligent_monitoring_enabled: bool = True
    smart_resources_enabled: bool = True
    adaptive_thresholds_enabled: bool = True
    anomaly_detection_enabled: bool = True
    
    # Memory Management
    max_memory_mb: int = 1024
    cache_size_mb: int = 256
    gc_threshold: float = 0.85
    emergency_threshold: float = 0.95
    
    # CPU Optimization
    max_cpu_usage: float = 80.0
    cpu_optimization_enabled: bool = True
    dynamic_scheduling: bool = True
    
    # Advanced Features
    deep_learning_enabled: bool = True
    ensemble_predictions: bool = True
    multi_model_training: bool = True
    real_time_adaptation: bool = True
    
    # Monitoring and Alerts
    performance_alerts_enabled: bool = True
    resource_alerts_enabled: bool = True
    prediction_accuracy_alerts: bool = True
    alert_threshold: float = 0.8
    
    # Analytics and Reporting
    analytics_enabled: bool = True
    detailed_logging: bool = True
    metrics_retention_days: int = 30
    export_enabled: bool = True


class AIConfigurationManager(QObject):
    """⚙️ Centralized AI configuration management"""
    
    # Signals for configuration changes
    configuration_changed = pyqtSignal(dict)
    feature_toggled = pyqtSignal(str, bool)
    optimization_level_changed = pyqtSignal(str)
    
    def __init__(self, config_file: str = "ai_config.json"):
        super().__init__()
        
        self.config_file = config_file
        self.config = AIConfiguration()
        self.default_config = AIConfiguration()
        
        # Load configuration
        self.load_configuration()
        
        # Validation rules
        self.validation_rules = {
            'learning_rate': (0.001, 0.1),
            'confidence_threshold': (0.1, 0.95),
            'prediction_interval': (1000, 60000),
            'monitoring_interval': (500, 10000),
            'max_memory_mb': (256, 8192),
            'max_cpu_usage': (20.0, 95.0)
        }
        
        print("⚙️ AI Configuration Manager initialized")
    
    def load_configuration(self) -> bool:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Update configuration with loaded data
                for key, value in config_data.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
                
                print(f"✅ Configuration loaded from {self.config_file}")
                return True
            else:
                print(f"⚠️ Configuration file not found, using defaults")
                self.save_configuration()  # Create default config file
                return True
                
        except Exception as e:
            print(f"❌ Configuration loading error: {e}")
            return False
    
    def save_configuration(self) -> bool:
        """Save configuration to file"""
        try:
            config_data = asdict(self.config)
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Configuration saving error: {e}")
            return False
    
    def update_setting(self, key: str, value: Any, emit_signal: bool = True) -> bool:
        """Update a specific configuration setting"""
        try:
            if not hasattr(self.config, key):
                print(f"❌ Unknown configuration key: {key}")
                return False
            
            # Validate value
            if not self._validate_setting(key, value):
                print(f"❌ Invalid value for {key}: {value}")
                return False
            
            # Update configuration
            old_value = getattr(self.config, key)
            setattr(self.config, key, value)
            
            # Emit signals
            if emit_signal:
                self.configuration_changed.emit({key: value})
                
                # Special handling for certain settings
                if key.endswith('_enabled'):
                    feature_name = key.replace('_enabled', '')
                    self.feature_toggled.emit(feature_name, value)
                elif key == 'optimization_level':
                    self.optimization_level_changed.emit(value)
            
            print(f"✅ Configuration updated: {key} = {value} (was {old_value})")
            return True
            
        except Exception as e:
            print(f"❌ Configuration update error: {e}")
            return False
    
    def update_multiple_settings(self, settings: Dict[str, Any]) -> Dict[str, bool]:
        """Update multiple configuration settings"""
        results = {}
        
        for key, value in settings.items():
            results[key] = self.update_setting(key, value, emit_signal=False)
        
        # Emit single configuration change signal
        successful_updates = {k: settings[k] for k, success in results.items() if success}
        if successful_updates:
            self.configuration_changed.emit(successful_updates)
        
        return results
    
    def _validate_setting(self, key: str, value: Any) -> bool:
        """Validate configuration setting value"""
        try:
            # Type validation
            current_value = getattr(self.config, key)
            if not isinstance(value, type(current_value)):
                return False
            
            # Range validation
            if key in self.validation_rules:
                min_val, max_val = self.validation_rules[key]
                if isinstance(value, (int, float)):
                    return min_val <= value <= max_val
            
            # String validation
            if key == 'optimization_level':
                return value in ['basic', 'adaptive', 'aggressive']
            
            return True
            
        except Exception as e:
            print(f"❌ Validation error for {key}: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        try:
            self.config = AIConfiguration()
            self.configuration_changed.emit(asdict(self.config))
            print("✅ Configuration reset to defaults")
            return True
            
        except Exception as e:
            print(f"❌ Reset to defaults error: {e}")
            return False
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration as dictionary"""
        return asdict(self.config)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get specific configuration setting"""
        return getattr(self.config, key, default)
    
    def toggle_feature(self, feature: str, enabled: Optional[bool] = None) -> bool:
        """Toggle or set feature enable/disable status"""
        key = f"{feature}_enabled"
        
        if enabled is None:
            # Toggle current state
            current_state = getattr(self.config, key, False)
            enabled = not current_state
        
        return self.update_setting(key, enabled)
    
    def set_optimization_level(self, level: str) -> bool:
        """Set AI optimization level"""
        if level not in ['basic', 'adaptive', 'aggressive']:
            print(f"❌ Invalid optimization level: {level}")
            return False
        
        success = self.update_setting('optimization_level', level)
        
        if success:
            # Update related settings based on optimization level
            if level == 'basic':
                self.update_multiple_settings({
                    'confidence_threshold': 0.8,
                    'prediction_interval': 15000,
                    'proactive_optimization': False,
                    'real_time_adaptation': False
                })
            elif level == 'adaptive':
                self.update_multiple_settings({
                    'confidence_threshold': 0.6,
                    'prediction_interval': 10000,
                    'proactive_optimization': True,
                    'real_time_adaptation': True
                })
            elif level == 'aggressive':
                self.update_multiple_settings({
                    'confidence_threshold': 0.4,
                    'prediction_interval': 5000,
                    'proactive_optimization': True,
                    'real_time_adaptation': True,
                    'dynamic_scheduling': True
                })
        
        return success
    
    def create_performance_profile(self, profile_name: str) -> Dict[str, Any]:
        """Create performance-optimized configuration profile"""
        profiles = {
            'power_saving': {
                'prediction_interval': 20000,
                'monitoring_interval': 5000,
                'max_cpu_usage': 60.0,
                'enhanced_features_enabled': False,
                'deep_learning_enabled': False
            },
            'balanced': {
                'prediction_interval': 10000,
                'monitoring_interval': 2000,
                'max_cpu_usage': 80.0,
                'enhanced_features_enabled': True,
                'deep_learning_enabled': True
            },
            'performance': {
                'prediction_interval': 5000,
                'monitoring_interval': 1000,
                'max_cpu_usage': 90.0,
                'enhanced_features_enabled': True,
                'deep_learning_enabled': True,
                'multi_model_training': True,
                'real_time_adaptation': True
            }
        }
        
        if profile_name in profiles:
            return profiles[profile_name]
        else:
            return {}
    
    def apply_performance_profile(self, profile_name: str) -> bool:
        """Apply a performance configuration profile"""
        profile_settings = self.create_performance_profile(profile_name)
        
        if profile_settings:
            results = self.update_multiple_settings(profile_settings)
            success_count = sum(results.values())
            total_count = len(results)
            
            print(f"✅ Applied {profile_name} profile: {success_count}/{total_count} settings updated")
            return success_count == total_count
        else:
            print(f"❌ Unknown performance profile: {profile_name}")
            return False
    
    def export_configuration(self, export_file: str) -> bool:
        """Export configuration to a specific file"""
        try:
            config_data = asdict(self.config)
            config_data['export_timestamp'] = __import__('time').time()
            config_data['export_version'] = '1.0'
            
            with open(export_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"✅ Configuration exported to {export_file}")
            return True
            
        except Exception as e:
            print(f"❌ Configuration export error: {e}")
            return False
    
    def import_configuration(self, import_file: str) -> bool:
        """Import configuration from a specific file"""
        try:
            if not os.path.exists(import_file):
                print(f"❌ Import file not found: {import_file}")
                return False
            
            with open(import_file, 'r') as f:
                config_data = json.load(f)
            
            # Remove metadata fields
            config_data.pop('export_timestamp', None)
            config_data.pop('export_version', None)
            
            # Apply imported configuration
            results = self.update_multiple_settings(config_data)
            success_count = sum(results.values())
            total_count = len(results)
            
            print(f"✅ Configuration imported: {success_count}/{total_count} settings applied")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Configuration import error: {e}")
            return False
    
    def get_feature_status(self) -> Dict[str, bool]:
        """Get status of all AI features"""
        return {
            'learning': self.config.learning_enabled,
            'prediction': self.config.prediction_enabled,
            'enhanced_features': self.config.enhanced_features_enabled,
            'enhanced_ml': self.config.enhanced_ml_enabled,
            'intelligent_monitoring': self.config.intelligent_monitoring_enabled,
            'smart_resources': self.config.smart_resources_enabled,
            'adaptive_thresholds': self.config.adaptive_thresholds_enabled,
            'anomaly_detection': self.config.anomaly_detection_enabled,
            'auto_optimization': self.config.auto_optimization_enabled,
            'deep_learning': self.config.deep_learning_enabled,
            'analytics': self.config.analytics_enabled
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance-related configuration settings"""
        return {
            'optimization_level': self.config.optimization_level,
            'learning_rate': self.config.learning_rate,
            'confidence_threshold': self.config.confidence_threshold,
            'prediction_interval': self.config.prediction_interval,
            'monitoring_interval': self.config.monitoring_interval,
            'max_memory_mb': self.config.max_memory_mb,
            'max_cpu_usage': self.config.max_cpu_usage
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration"""
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            config_dict = asdict(self.config)
            
            # Check for conflicting settings
            if not self.config.learning_enabled and self.config.prediction_enabled:
                validation_results['warnings'].append(
                    "Prediction enabled without learning - may have reduced accuracy"
                )
            
            # Check performance settings
            if self.config.prediction_interval < 5000 and self.config.monitoring_interval < 1000:
                validation_results['warnings'].append(
                    "Very aggressive monitoring intervals may impact performance"
                )
            
            # Check memory settings
            if self.config.cache_size_mb > self.config.max_memory_mb * 0.5:
                validation_results['warnings'].append(
                    "Cache size is more than 50% of max memory - consider reducing"
                )
            
            # Check feature dependencies
            if self.config.enhanced_features_enabled and not self.config.enhanced_ml_enabled:
                validation_results['recommendations'].append(
                    "Enable Enhanced ML for better performance with enhanced features"
                )
            
            # Add recommendations based on optimization level
            if self.config.optimization_level == 'basic' and self.config.enhanced_features_enabled:
                validation_results['recommendations'].append(
                    "Consider 'adaptive' optimization level for better use of enhanced features"
                )
            
        except Exception as e:
            validation_results['valid'] = False
            validation_results['errors'].append(f"Validation error: {e}")
        
        return validation_results
    
    def auto_tune_configuration(self, system_resources: Optional[Dict[str, Any]] = None) -> bool:
        """Auto-tune configuration based on system resources"""
        try:
            if system_resources is None:
                # Get basic system info
                import psutil
                system_resources = {
                    'cpu_count': psutil.cpu_count(),
                    'memory_gb': psutil.virtual_memory().total / (1024**3),
                    'cpu_freq': psutil.cpu_freq().max if psutil.cpu_freq() else 2000
                }
            
            # Auto-tune based on system capabilities
            cpu_count = system_resources.get('cpu_count', 4)
            memory_gb = system_resources.get('memory_gb', 8)
            
            tuning_updates = {}
            
            # Memory settings
            if memory_gb >= 16:
                tuning_updates.update({
                    'max_memory_mb': 2048,
                    'cache_size_mb': 512,
                    'enhanced_features_enabled': True,
                    'deep_learning_enabled': True
                })
            elif memory_gb >= 8:
                tuning_updates.update({
                    'max_memory_mb': 1024,
                    'cache_size_mb': 256,
                    'enhanced_features_enabled': True
                })
            else:
                tuning_updates.update({
                    'max_memory_mb': 512,
                    'cache_size_mb': 128,
                    'enhanced_features_enabled': False,
                    'deep_learning_enabled': False
                })
            
            # CPU settings
            if cpu_count >= 8:
                tuning_updates.update({
                    'prediction_interval': 5000,
                    'monitoring_interval': 1000,
                    'multi_model_training': True
                })
            elif cpu_count >= 4:
                tuning_updates.update({
                    'prediction_interval': 10000,
                    'monitoring_interval': 2000
                })
            else:
                tuning_updates.update({
                    'prediction_interval': 15000,
                    'monitoring_interval': 5000,
                    'multi_model_training': False
                })
            
            # Apply tuning
            results = self.update_multiple_settings(tuning_updates)
            success_count = sum(results.values())
            
            print(f"✅ Auto-tuning complete: {success_count} settings optimized for system")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Auto-tuning error: {e}")
            return False


# Global configuration manager
global_ai_config_manager = None

def get_ai_config_manager(config_file: str = "ai_config.json") -> AIConfigurationManager:
    """Get or create global AI configuration manager"""
    global global_ai_config_manager
    if global_ai_config_manager is None:
        global_ai_config_manager = AIConfigurationManager(config_file)
    return global_ai_config_manager


if __name__ == "__main__":
    # Test AI configuration manager
    print("⚙️ Testing AI Configuration Manager")
    
    # Create config manager
    config_mgr = AIConfigurationManager("test_ai_config.json")
    
    # Test basic operations
    print(f"\n📊 Current optimization level: {config_mgr.get_setting('optimization_level')}")
    
    # Test feature toggle
    config_mgr.toggle_feature('enhanced_ml')
    print(f"Enhanced ML enabled: {config_mgr.get_setting('enhanced_ml_enabled')}")
    
    # Test optimization level change
    config_mgr.set_optimization_level('aggressive')
    print(f"Optimization level changed to: {config_mgr.get_setting('optimization_level')}")
    
    # Test performance profile
    config_mgr.apply_performance_profile('performance')
    
    # Test configuration validation
    validation = config_mgr.validate_configuration()
    print(f"\n🔍 Configuration validation:")
    print(f"Valid: {validation['valid']}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    if validation['recommendations']:
        print(f"Recommendations: {validation['recommendations']}")
    
    # Test auto-tuning
    config_mgr.auto_tune_configuration()
    
    # Get feature status
    features = config_mgr.get_feature_status()
    print(f"\n🎛️ Feature status: {features}")
    
    # Save configuration
    config_mgr.save_configuration()
    
    print("\n✅ AI Configuration Manager testing complete!")