# backend.py - Xử lý tương tác với công cụ dòng lệnh MuMuManager.exe

import os
import subprocess
import json
import shlex
from typing import List, Tuple, Any, Dict

# Constants để tránh magic numbers
DEFAULT_TIMEOUT = 30
MAX_INSTANCES_CREATE = 50
MAX_INSTANCES_CLONE = 20
MAX_NAME_LENGTH = 100

def find_mumu_instance_path(instance_index: int) -> str:
    """Try to find the actual path of a MuMu instance by checking common locations."""
    # Common MuMu installation paths (updated with user's actual path)
    possible_base_paths = [
        r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\vms",  # User's actual path
        r"C:\Program Files\Netease\MuMuPlayer-12.0\vms",
        r"C:\Program Files (x86)\Netease\MuMuPlayerGlobal-12.0\vms",
        r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\vms", 
        r"C:\Users\Public\Documents\MuMu\vms",
        r"C:\ProgramData\MuMu\vms",
        r"D:\Program Files\Netease\MuMuPlayerGlobal-12.0\vms",
        r"D:\Program Files\Netease\MuMuPlayer-12.0\vms",
        r"D:\MuMu\vms"
    ]
    
    # Try different naming patterns
    possible_names = [
        f"MuMuPlayerGlobal-12.0-{instance_index}",
        f"MuMuPlayer-12.0-{instance_index}",
        f"MuMu{instance_index}",
        f"vm_{instance_index}",
        f"instance_{instance_index}",
        str(instance_index)
    ]
    
    for base_path in possible_base_paths:
        if os.path.exists(base_path):
            for name in possible_names:
                full_path = os.path.join(base_path, name)
                if os.path.exists(full_path):
                    return full_path
    
    return ""

def calculate_folder_size(folder_path: str) -> int:
    """Calculate the total size of a folder in bytes."""
    if not folder_path or not os.path.exists(folder_path):
        return 0
    
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                except (OSError, IOError):
                    # Skip files that can't be accessed
                    continue
    except (OSError, IOError):
        # Return 0 if folder can't be accessed
        return 0
    return total_size

def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable string."""
    if size_bytes == 0:
        return "0MB"
    
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            if unit == 'B':
                return f"{int(size)}{unit}"
            else:
                return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}PB"

class MumuManager:
    """Lớp bao (wrapper) mạnh mẽ để tương tác với công cụ dòng lệnh MuMuManager.exe."""

    def __init__(self, executable_path: str):
        self.executable_path = executable_path
        if not os.path.exists(self.executable_path):
            print(f"Cảnh báo: Không tìm thấy MuMuManager.exe tại {self.executable_path}")

    def is_valid(self) -> bool:
        """Kiểm tra xem đường dẫn thực thi đã cấu hình có hợp lệ không."""
        return os.path.isfile(self.executable_path)
    
    def get_version_info(self) -> Tuple[bool, str]:
        """Lấy thông tin version của MuMuManager."""
        return self._run_command(['--version'])
    
    def _validate_indices(self, indices: List[int]) -> Tuple[bool, str]:
        """Validate danh sách indices."""
        if not indices:
            return False, "Không có instance nào được chọn"
        if any(idx < 0 for idx in indices):
            return False, "Index không thể âm"
        if len(indices) > 100:  # Giới hạn an toàn
            return False, "Quá nhiều instances được chọn (tối đa 100)"
        return True, ""

    def _run_command(self, args: List[str]) -> Tuple[bool, str]:
        """Thực thi một lệnh và nhận output."""
        if not self.is_valid():
            return False, f"Lỗi: Không tìm thấy '{os.path.basename(self.executable_path)}'."

        command = [self.executable_path] + args
        
        # Cấu hình startup để ẩn console window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        try:
            # Tối ưu hóa subprocess call với error handling tốt hơn
            result = subprocess.run(
                command, 
                check=False,  # Không raise exception để có control tốt hơn
                capture_output=True, 
                text=True,
                encoding='utf-8', 
                errors='replace',  # Xử lý encoding errors tốt hơn
                startupinfo=startupinfo,
                timeout=DEFAULT_TIMEOUT  # Sử dụng constant
            )
            
            # Kiểm tra return code và xây dựng error message có cấu trúc
            if result.returncode != 0:
                error_parts = [f"Lệnh thất bại (return code: {result.returncode})"]
                if result.stderr:
                    error_parts.append(f"Stderr: {result.stderr.strip()}")
                if result.stdout:
                    error_parts.append(f"Stdout: {result.stdout.strip()}")
                return False, "\n".join(error_parts)
            
            # Hợp nhất stdout và stderr một cách thông minh
            output_parts = []
            if result.stdout:
                output_parts.append(result.stdout.strip())
            if result.stderr:
                output_parts.append(result.stderr.strip())
            
            return True, "\n".join(output_parts) if output_parts else ""
            
        except subprocess.TimeoutExpired:
            return False, f"Lỗi: Lệnh bị quá thời gian chờ ({DEFAULT_TIMEOUT}s). Args={' '.join(args)}"
        except subprocess.CalledProcessError as e:
            # Note: Không bao giờ đến đây vì check=False
            error_msg = f"Lỗi thực thi lệnh:\n{e.stderr.strip() if e.stderr else 'Không có thông tin lỗi.'}"
            return False, error_msg
        except FileNotFoundError:
            return False, f"Lỗi: Không tìm thấy file thực thi '{self.executable_path}'"
        except Exception as e:
            return False, f"Lỗi không xác định: {type(e).__name__}: {e}"

    def get_all_info(self) -> Tuple[bool, Any]:
        """Lấy thông tin cho tất cả máy ảo, xử lý nhiều định dạng JSON một cách thông minh."""
        success, output = self._run_command(['info', '-v', 'all'])
        if not success:
            return False, output
        
        # Early return cho output rỗng
        if not output.strip():
            return True, {}
        
        try:
            return self._parse_json_output(output)
        except json.JSONDecodeError:
            error_details = f"Lỗi phân tích JSON. Dữ liệu nhận được không hợp lệ.\n--- Dữ liệu thô ---\n{output}\n--- Kết thúc ---"
            return False, error_details
    
    def _parse_json_output(self, output: str) -> Tuple[bool, Dict[str, Any]]:
        """Helper method để parse JSON output với nhiều format khác nhau."""
        # Thử parse multi-line JSON objects trước
        json_lines = [line.strip() for line in output.strip().split('\n') 
                     if line.strip() and line.startswith('{')]
        
        if len(json_lines) > 1:
            # Multiple JSON objects, một object per line
            json_objects = [json.loads(line) for line in json_lines]
            if all('index' in obj for obj in json_objects):
                parsed_data = {str(obj['index']): obj for obj in json_objects}
                # Add real disk usage calculation
                self._calculate_disk_usage_for_all(parsed_data)
                return True, parsed_data

        # Thử parse như single JSON object
        data = json.loads(output)
        
        # Xử lý các format khác nhau
        if isinstance(data, list):
            # Array of objects
            if all(isinstance(obj, dict) and 'index' in obj for obj in data):
                parsed_data = {str(obj['index']): obj for obj in data}
                self._calculate_disk_usage_for_all(parsed_data)
                return True, parsed_data
            # Array without index, sử dụng position
            parsed_data = {str(i): obj for i, obj in enumerate(data)}
            self._calculate_disk_usage_for_all(parsed_data)
            return True, parsed_data
        
        if isinstance(data, dict):
            # Dictionary with indexed objects
            if all(isinstance(v, dict) and 'index' in v for v in data.values()):
                self._calculate_disk_usage_for_all(data)
                return True, data
            # Single object with index
            if 'index' in data:
                parsed_data = {str(data['index']): data}
                self._calculate_disk_usage_for_all(parsed_data)
                return True, parsed_data
            # Dictionary format khác
            self._calculate_disk_usage_for_all(data)
            return True, data
                
        return False, f"Định dạng dữ liệu không được hỗ trợ:\n{output}"

    def _calculate_disk_usage_for_all(self, instances_data: Dict[str, Any]) -> None:
        """Calculate real disk usage for all instances."""
        for instance_key, instance_data in instances_data.items():
            if isinstance(instance_data, dict):
                self._calculate_disk_usage_for_instance(instance_data)
    
    def _calculate_disk_usage_for_instance(self, instance_data: Dict[str, Any]) -> None:
        """Calculate real disk usage for a single instance."""
        try:
            instance_id = instance_data.get('index', 'unknown')
            
            # First, check if MuMuManager already provided disk_size_bytes
            disk_bytes = instance_data.get('disk_size_bytes', 0)
            if disk_bytes and disk_bytes > 0:
                # Use the data from MuMuManager directly
                formatted_size = format_size(disk_bytes)
                instance_data['disk_usage'] = formatted_size
                instance_data['disk_size_bytes'] = disk_bytes
                
                # Log for debugging (first few instances only)
                if int(str(instance_id)) <= 3:
                    print(f"💾 Instance {instance_id}: Using MuMu data -> {formatted_size} ({disk_bytes} bytes)")
                return
            
            # If no disk_size_bytes from MuMu, try to calculate manually
            path = instance_data.get('path', '')
            
            # If no path provided, try to find it automatically
            if not path or path == '':
                path = find_mumu_instance_path(int(str(instance_id)))
                if path:
                    # Update the instance data with found path
                    instance_data['path'] = path
            
            # Debug: Log path info for first few instances
            if int(str(instance_id)) <= 3:
                print(f"🔍 Instance {instance_id}: path='{path}', exists={os.path.exists(path) if path else False}")
            
            if path and os.path.exists(path):
                # Calculate the actual disk usage manually
                disk_bytes = calculate_folder_size(path)
                formatted_size = format_size(disk_bytes)
                
                # Update the instance data with calculated disk usage
                instance_data['disk_usage'] = formatted_size
                instance_data['disk_size_bytes'] = disk_bytes
                
                # Log for debugging (first few instances only)
                if int(str(instance_id)) <= 3:
                    print(f"💾 Instance {instance_id}: Calculated {path} -> {formatted_size} ({disk_bytes} bytes)")
            else:
                # No valid path and no MuMu data, keep as 0MB
                if int(str(instance_id)) <= 3:
                    print(f"❌ Instance {instance_id}: No data available - keeping 0MB")
                instance_data['disk_usage'] = "0MB"
                instance_data['disk_size_bytes'] = 0
        except Exception as e:
            # If anything fails, keep original values
            instance_data['disk_usage'] = instance_data.get('disk_usage', '0MB')
            instance_data['disk_size_bytes'] = 0
            print(f"⚠️ Error calculating disk usage for instance {instance_data.get('index', 'unknown')}: {e}")

    def get_single_info(self, index: int) -> Tuple[bool, Any]:
        """Lấy thông tin cho một máy ảo duy nhất với error handling tốt hơn."""
        success, output = self._run_command(['info', '-v', str(index)])
        if not success:
            return False, f"Command failed: {output}"
        
        if not output.strip():
            return False, f"Không có dữ liệu cho máy ảo index {index}"
            
        try:
            data = json.loads(output)
            
            # Validate that data is not empty and contains expected structure
            if data is None:
                return False, f"Dữ liệu là None cho máy ảo {index}"
                
            if not isinstance(data, dict):
                return False, f"Dữ liệu không phải dict cho máy ảo {index}: {type(data)} = {data}"
            
            if len(data) == 0:
                return False, f"Dữ liệu dict rỗng cho máy ảo {index}"
            
            # Check for essential fields that should exist in VM info
            if 'index' not in data and 'name' not in data:
                return False, f"Dữ liệu thiếu thông tin cơ bản cho máy ảo {index}: {list(data.keys())}"
            
            # Ensure index field exists and matches
            if 'index' not in data:
                data['index'] = index
            
            # Calculate real disk usage for this instance
            self._calculate_disk_usage_for_instance(data)
                
            return True, data
        except json.JSONDecodeError as e:
            return False, f"Lỗi phân tích JSON cho máy ảo {index}: {e}\nDữ liệu: {output}"

    def control_instance(self, indices: List[int], action: str) -> Tuple[bool, str]:
        """Điều khiển instances với validation."""
        if not indices:
            return False, "Không có instance nào được chọn"
        if not action:
            return False, "Action không được để trống"
        return self._run_command(['control', '--vmindex', ",".join(map(str, indices)), action])

    def create_instance(self, count: int) -> Tuple[bool, str]:
        """Tạo instances mới với validation."""
        if count <= 0:
            return False, "Số lượng instance phải lớn hơn 0"
        if count > MAX_INSTANCES_CREATE:  # Sử dụng constant
            return False, f"Không thể tạo quá {MAX_INSTANCES_CREATE} instances cùng lúc"
        return self._run_command(['create', '-n', str(count)])

    def clone_instance(self, source_index: int, count: int) -> Tuple[bool, str]:
        """Clone instance với validation."""
        if count <= 0:
            return False, "Số lượng clone phải lớn hơn 0"
        if count > MAX_INSTANCES_CLONE:  # Sử dụng constant
            return False, f"Không thể clone quá {MAX_INSTANCES_CLONE} instances cùng lúc"
        return self._run_command(['clone', '-v', str(source_index), '-n', str(count)])

    def delete_instance(self, indices: List[int]) -> Tuple[bool, str]:
        """Xóa instances với validation."""
        if not indices:
            return False, "Không có instance nào được chọn để xóa"
        return self._run_command(['delete', '-v', ",".join(map(str, indices))])

    def rename_instance(self, index: int, new_name: str) -> Tuple[bool, str]:
        """Đổi tên instance với validation."""
        if not new_name or not new_name.strip():
            return False, "Tên mới không được để trống"
        if len(new_name.strip()) > MAX_NAME_LENGTH:  # Sử dụng constant
            return False, f"Tên instance quá dài (tối đa {MAX_NAME_LENGTH} ký tự)"
        return self._run_command(['rename', '-v', str(index), '-n', new_name.strip()])

    def run_adb_command(self, indices: List[int], command_str: str) -> Tuple[bool, str]:
        """Chạy ADB command với validation và security checks."""
        if not indices:
            return False, "Không có instance nào được chọn"
        if not command_str or not command_str.strip():
            return False, "Lệnh ADB không được để trống"
        
        # Basic security validation
        dangerous_commands = ['rm -rf', 'format', 'factory', 'wipe', 'delete', 'dd if=']
        command_lower = command_str.lower()
        if any(dangerous in command_lower for dangerous in dangerous_commands):
            return False, f"Lệnh có thể nguy hiểm và không được phép: {command_str}"
        
        try:
            cmd_parts = shlex.split(command_str.strip())
            if not cmd_parts:
                return False, "Lệnh ADB không hợp lệ sau khi parse"
            return self._run_command(['adb', '-v', ",".join(map(str, indices)), '-c'] + cmd_parts)
        except ValueError as e:
            return False, f"Lỗi parse command: {e}"

    def set_simulation_value(self, indices: List[int], key: str, value: str) -> Tuple[bool, str]:
        """Set simulation value với validation."""
        if not indices:
            return False, "Không có instance nào được chọn"
        if not key or not key.strip():
            return False, "Key không được để trống"
        return self._run_command(['simulation', '-v', ",".join(map(str, indices)), '-sk', key.strip(), '-sv', value])

    def get_settings_info(self, index: int) -> Tuple[bool, str]:
        """Lấy thông tin settings với error handling."""
        return self._run_command(['setting', '-v', str(index), '-i'])

    def get_writable_settings_values(self, index: int) -> Tuple[bool, str]:
        """Lấy giá trị settings có thể write với error handling."""
        return self._run_command(['setting', '-v', str(index), '-aw'])

    def set_settings(self, indices: List[int], settings: Dict[str, str]) -> Tuple[bool, str]:
        """Set multiple settings với validation và optimization."""
        if not indices:
            return False, "Không có instance nào được chọn"
        if not settings:
            return True, "Không có cài đặt nào được thay đổi."
        
        # Validate settings
        invalid_settings = []
        for key, value in settings.items():
            if not key or not key.strip():
                invalid_settings.append(f"Key rỗng với value: {value}")
        
        if invalid_settings:
            return False, f"Settings không hợp lệ: {'; '.join(invalid_settings)}"
        
        # Build command efficiently
        args = ['setting', '-v', ",".join(map(str, indices))]
        for key, value in settings.items():
            args.extend(['-k', key.strip(), '-val', str(value)])
            
        return self._run_command(args)
