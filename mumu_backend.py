# mumu_backend.py - Backend wrapper cho MumuManager Pro với tích hợp optimization

import os
from typing import List, Dict, Any, Union, Tuple
from backend import MumuManager

class MumuBackend:
    """Backend wrapper cho MumuManager với các chức năng cần thiết cho automation."""
    
    def __init__(self):
        """Initialize MumuBackend với đường dẫn MuMuManager.exe thực tế."""
        # Common paths where MuMuManager might be installed
        possible_paths = [
            r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuManager.exe",
            r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\MuMuManager.exe",
            r"C:\Program Files (x86)\Netease\MuMuPlayerGlobal-12.0\shell\MuMuManager.exe",
            r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\shell\MuMuManager.exe",
            r"D:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuManager.exe",
            r"D:\Program Files\Netease\MuMuPlayer-12.0\shell\MuMuManager.exe",
        ]
        
        # Find valid MuMuManager.exe path
        mumu_path = None
        for path in possible_paths:
            if os.path.exists(path):
                mumu_path = path
                break
        
        if not mumu_path:
            # Fallback to a default path if none found
            mumu_path = r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuManager.exe"
        
        self.mumu_manager = MumuManager(mumu_path)
    
    def is_valid(self) -> bool:
        """Check if MumuManager is properly configured."""
        return self.mumu_manager.is_valid()
    
    def get_instance_list(self) -> Dict[str, Any]:
        """Get all instances information."""
        success, data = self.mumu_manager.get_all_info()
        if success and isinstance(data, dict):
            return data
        return {}
    
    def get_instance_info(self, instance_index: int) -> Dict[str, Any]:
        """Get information for a specific instance."""
        success, data = self.mumu_manager.get_single_info(instance_index)
        if success and isinstance(data, dict):
            return data
        return {}
    
    def start_instance(self, instance_index: int) -> bool:
        """Start a MuMu instance."""
        success, _ = self.mumu_manager.control_instance([instance_index], "start")
        return success
    
    def stop_instance(self, instance_index: int) -> bool:
        """Stop a MuMu instance."""
        success, _ = self.mumu_manager.control_instance([instance_index], "stop")
        return success
    
    def restart_instance(self, instance_index: int) -> bool:
        """Restart a MuMu instance."""
        success, _ = self.mumu_manager.control_instance([instance_index], "restart")
        return success
    
    def start_instances(self, instance_indices: List[int]) -> bool:
        """Start multiple MuMu instances."""
        if not instance_indices:
            return False
        success, _ = self.mumu_manager.control_instance(instance_indices, "start")
        return success
    
    def stop_instances(self, instance_indices: List[int]) -> bool:
        """Stop multiple MuMu instances."""
        if not instance_indices:
            return False
        success, _ = self.mumu_manager.control_instance(instance_indices, "stop")
        return success
    
    def restart_instances(self, instance_indices: List[int]) -> bool:
        """Restart multiple MuMu instances."""
        if not instance_indices:
            return False
        success, _ = self.mumu_manager.control_instance(instance_indices, "restart")
        return success
    
    def create_instance(self, count: int = 1) -> bool:
        """Create new instances."""
        success, _ = self.mumu_manager.create_instance(count)
        return success
    
    def clone_instance(self, source_index: int, count: int = 1) -> bool:
        """Clone an instance."""
        success, _ = self.mumu_manager.clone_instance(source_index, count)
        return success
    
    def delete_instance(self, instance_indices: List[int]) -> bool:
        """Delete instances."""
        if not instance_indices:
            return False
        success, _ = self.mumu_manager.delete_instance(instance_indices)
        return success
    
    def rename_instance(self, instance_index: int, new_name: str) -> bool:
        """Rename an instance."""
        success, _ = self.mumu_manager.rename_instance(instance_index, new_name)
        return success
    
    def run_adb_command(self, instance_indices: List[int], command: str) -> Tuple[bool, str]:
        """Run ADB command on instances."""
        if not instance_indices:
            return False, "No instances selected"
        return self.mumu_manager.run_adb_command(instance_indices, command)
    
    def get_settings_info(self, instance_index: int) -> Tuple[bool, str]:
        """Get settings information for an instance."""
        return self.mumu_manager.get_settings_info(instance_index)
    
    def set_settings(self, instance_indices: List[int], settings: Dict[str, str]) -> bool:
        """Set settings for instances."""
        if not instance_indices or not settings:
            return False
        success, _ = self.mumu_manager.set_settings(instance_indices, settings)
        return success
    
    def get_version_info(self) -> Tuple[bool, str]:
        """Get MuMuManager version information."""
        return self.mumu_manager.get_version_info()

# Create global instance for easy import
mumu_backend = MumuBackend()
