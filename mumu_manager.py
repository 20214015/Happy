"""
MuMu Manager - Tích hợp với MuMuManager.exe để quản lý instances hiệu quả
Thay thế cách check process cũ để giảm lag ứng dụng
"""

import json
import subprocess
import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MuMuInstance:
    """Thông tin instance MuMu từ MuMuManager.exe"""
    index: str
    name: str
    adb_host_ip: Optional[str] = None
    adb_port: Optional[int] = None
    created_timestamp: Optional[int] = None
    disk_size_bytes: Optional[int] = None
    error_code: int = 0
    headless_pid: Optional[int] = None
    hyperv_enabled: bool = False
    is_android_started: bool = False
    is_main: bool = False
    is_process_started: bool = False
    launch_err_code: int = 0
    launch_err_msg: str = ""
    main_wnd: Optional[str] = None
    pid: Optional[int] = None
    player_state: Optional[str] = None
    render_wnd: Optional[str] = None
    vt_enabled: Optional[bool] = None

class MuMuManager:
    """Quản lý MuMu instances thông qua MuMuManager.exe"""
    
    def __init__(self):
        self.manager_path = self._find_mumu_manager()
        self.instances_cache = {}
        self.last_update = 0
        
    def _find_mumu_manager(self) -> Optional[str]:
        """Tìm đường dẫn MuMuManager.exe"""
        possible_paths = [
            r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\MuMuManager.exe",
            r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuManager.exe",
            r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\shell\MuMuManager.exe",
            r"C:\Program Files (x86)\Netease\MuMuPlayerGlobal-12.0\shell\MuMuManager.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        # Tìm trong registry hoặc environment variables
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Netease\MuMuPlayer") as key:
                install_path = winreg.QueryValueEx(key, "InstallPath")[0]
                manager_path = os.path.join(install_path, "shell", "MuMuManager.exe")
                if os.path.exists(manager_path):
                    return manager_path
        except:
            pass
            
        return None
        
    def _run_command(self, args: List[str]) -> Optional[Dict]:
        """Chạy lệnh MuMuManager và trả về JSON result"""
        if not self.manager_path:
            return None
            
        try:
            cmd = [self.manager_path] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    return json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    # Nếu không phải JSON, trả về text
                    return {"output": result.stdout.strip()}
            else:
                return {"error": result.stderr or "Command failed"}
                
        except subprocess.TimeoutExpired:
            return {"error": "Command timeout"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_all_instances(self) -> List[MuMuInstance]:
        """Lấy thông tin tất cả instances"""
        result = self._run_command(["info", "-v", "all"])
        if not result or "error" in result:
            return []
            
        instances = []
        if isinstance(result, list):
            for item in result:
                instances.append(self._parse_instance(item))
        elif isinstance(result, dict) and "index" in result:
            instances.append(self._parse_instance(result))
            
        return instances
    
    def get_instance(self, index: str) -> Optional[MuMuInstance]:
        """Lấy thông tin instance cụ thể"""
        result = self._run_command(["info", "-v", index])
        if not result or "error" in result:
            return None
            
        if isinstance(result, list) and len(result) > 0:
            return self._parse_instance(result[0])
        elif isinstance(result, dict) and "index" in result:
            return self._parse_instance(result)
            
        return None
    
    def _parse_instance(self, data: Dict) -> MuMuInstance:
        """Parse JSON data thành MuMuInstance object"""
        return MuMuInstance(
            index=str(data.get("index", "")),
            name=data.get("name", ""),
            adb_host_ip=data.get("adb_host_ip"),
            adb_port=data.get("adb_port"),
            created_timestamp=data.get("created_timestamp"),
            disk_size_bytes=data.get("disk_size_bytes"),
            error_code=data.get("error_code", 0),
            headless_pid=data.get("headless_pid"),
            hyperv_enabled=data.get("hyperv_enabled", False),
            is_android_started=data.get("is_android_started", False),
            is_main=data.get("is_main", False),
            is_process_started=data.get("is_process_started", False),
            launch_err_code=data.get("launch_err_code", 0),
            launch_err_msg=data.get("launch_err_msg", ""),
            main_wnd=data.get("main_wnd"),
            pid=data.get("pid"),
            player_state=data.get("player_state"),
            render_wnd=data.get("render_wnd"),
            vt_enabled=data.get("vt_enabled")
        )
    
    def get_running_instances(self) -> List[MuMuInstance]:
        """Lấy danh sách instances đang chạy"""
        all_instances = self.get_all_instances()
        return [inst for inst in all_instances if inst.is_process_started]
    
    def get_instance_count(self) -> Dict[str, int]:
        """Đếm số lượng instances theo trạng thái"""
        instances = self.get_all_instances()
        return {
            "total": len(instances),
            "running": len([i for i in instances if i.is_process_started]),
            "android_started": len([i for i in instances if i.is_android_started]),
            "main": len([i for i in instances if i.is_main])
        }
    
    def control_instance(self, index: str, action: str) -> bool:
        """Điều khiển instance (launch, shutdown, restart)"""
        result = self._run_command(["control", "-v", index, action])
        return result is not None and "error" not in result
    
    def launch_instance(self, index: str, package: Optional[str] = None) -> bool:
        """Khởi động instance"""
        args = ["control", "-v", index, "launch"]
        if package:
            args.extend(["-pkg", package])
        result = self._run_command(args)
        return result is not None and "error" not in result
    
    def shutdown_instance(self, index: str) -> bool:
        """Tắt instance"""
        return self.control_instance(index, "shutdown")
    
    def restart_instance(self, index: str) -> bool:
        """Khởi động lại instance"""
        return self.control_instance(index, "restart")
    
    def show_instance(self, index: str) -> bool:
        """Hiển thị cửa sổ instance"""
        return self.control_instance(index, "show_window")
    
    def hide_instance(self, index: str) -> bool:
        """Ẩn cửa sổ instance"""
        return self.control_instance(index, "hide_window")
    
    def get_app_info(self, index: str, package: Optional[str] = None) -> Optional[Dict]:
        """Lấy thông tin app trong instance"""
        args = ["control", "-v", index, "app", "info"]
        if package:
            args.extend(["-pkg", package])
        else:
            args.append("-i")
        return self._run_command(args)
    
    def install_app(self, index: str, apk_path: str) -> bool:
        """Cài đặt app vào instance"""
        result = self._run_command(["control", "-v", index, "app", "install", "-apk", apk_path])
        return result is not None and "error" not in result
    
    def launch_app(self, index: str, package: str) -> bool:
        """Khởi động app trong instance"""
        result = self._run_command(["control", "-v", index, "app", "launch", "-pkg", package])
        return result is not None and "error" not in result
    
    def close_app(self, index: str, package: str) -> bool:
        """Đóng app trong instance"""
        result = self._run_command(["control", "-v", index, "app", "close", "-pkg", package])
        return result is not None and "error" not in result
    
    def get_setting(self, index: Optional[str] = None, key: Optional[str] = None) -> Optional[Dict]:
        """Lấy cấu hình instance"""
        args = ["setting"]
        if index:
            args.extend(["-v", index])
        if key:
            args.extend(["-k", key])
        else:
            args.append("-aw")  # All writable settings
        return self._run_command(args)
    
    def set_setting(self, index: str, key: str, value: str) -> bool:
        """Thiết lập cấu hình instance"""
        result = self._run_command(["setting", "-v", index, "-k", key, "-val", value])
        return result is not None and "error" not in result
    
    def adb_command(self, index: str, command: str) -> Optional[Dict]:
        """Thực hiện lệnh ADB"""
        result = self._run_command(["adb", "-v", index, "-c", command])
        return result
    
    def create_instance(self, index: Optional[str] = None) -> bool:
        """Tạo instance mới"""
        args = ["create"]
        if index:
            args.extend(["-v", index])
        result = self._run_command(args)
        return result is not None and "error" not in result
    
    def delete_instance(self, index: str) -> bool:
        """Xóa instance"""
        result = self._run_command(["delete", "-v", index])
        return result is not None and "error" not in result
    
    def clone_instance(self, index: str) -> bool:
        """Sao chép instance"""
        result = self._run_command(["clone", "-v", index])
        return result is not None and "error" not in result
    
    def rename_instance(self, index: str, name: str) -> bool:
        """Đổi tên instance"""
        result = self._run_command(["rename", "-v", index, "-n", name])
        return result is not None and "error" not in result
    
    def sort_windows(self) -> bool:
        """Sắp xếp cửa sổ instances"""
        result = self._run_command(["sort"])
        return result is not None and "error" not in result
    
    def is_available(self) -> bool:
        """Kiểm tra MuMuManager có khả dụng không"""
        return self.manager_path is not None and os.path.exists(self.manager_path)
    
    def get_quick_status(self) -> Dict[str, Any]:
        """Lấy trạng thái nhanh cho UI (thay thế process scanning cũ)"""
        if not self.is_available():
            return {"error": "MuMuManager not available", "instances": []}
        
        try:
            instances = self.get_all_instances()
            running_instances = [inst for inst in instances if inst.is_process_started]
            
            return {
                "total_instances": len(instances),
                "running_instances": len(running_instances),
                "instances": [
                    {
                        "index": inst.index,
                        "name": inst.name,
                        "is_running": inst.is_process_started,
                        "is_android_started": inst.is_android_started,
                        "pid": inst.pid,
                        "headless_pid": inst.headless_pid,
                        "adb_port": inst.adb_port,
                        "player_state": inst.player_state
                    }
                    for inst in running_instances
                ],
                "error": None
            }
        except Exception as e:
            return {"error": str(e), "instances": []}

# Singleton instance
mumu_manager = MuMuManager()

def get_mumu_instances_fast() -> Dict[str, Any]:
    """Hàm nhanh để lấy thông tin instances - thay thế cho process scanning"""
    return mumu_manager.get_quick_status()

def check_mumu_available() -> bool:
    """Kiểm tra MuMu có sẵn không"""
    return mumu_manager.is_available()
