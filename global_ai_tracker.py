"""
Global AI Instance Tracker
=========================

Hệ thống AI tracking toàn cục để theo dõi instances MuMu real-time
và cập nhật status column tự động.

Author: GitHub Copilot
Date: August 25, 2025
"""

import psutil
import re
from datetime import datetime
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtGui import QColor
from typing import Dict, List, Optional, Any

class GlobalAITracker(QObject):
    """Global AI Tracker để theo dõi instances MuMu real-time"""
    
    # Signals để thông báo khi có thay đổi
    instance_status_changed = pyqtSignal(int, str, dict)  # instance_id, status, data
    instances_updated = pyqtSignal(dict)  # all tracked instances
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Tracking data
        self.tracked_instances = {}
        self.last_scan_time = None
        self.is_active = True
        DEBUG_MODE = False  # ✅ Silent mode for performance
        self.scan_interval = 10000  # Tăng lên 10 giây để giảm lag
        
        # Setup timer với interval lớn hơn
        self.tracker_timer = QTimer()
        self.tracker_timer.timeout.connect(self.scan_instances)
        self.tracker_timer.start(self.scan_interval)  # Scan mỗi 10 giây
        
        print("🤖 Global AI Tracker initialized (Optimized for UI performance)")
    
    def scan_instances(self):
        """Scan và detect MuMu instances (Optimized for UI performance)"""
        try:
            if not self.is_active:
                return
                
            # Reduced debug output - only log when debug mode is enabled
            current_time = datetime.now()
            
            # Clear old data
            old_instances = self.tracked_instances.copy()
            self.tracked_instances.clear()
            
            # Scan MuMu processes  
            mumu_processes = self._scan_mumu_processes()
            
            # Only show debug when processes count changes significantly
            if self.debug_mode:
                current_count = len(mumu_processes)
                if not hasattr(self, '_last_process_count'):
                    self._last_process_count = 0
                    print("🔍 DEBUG: Global AI Tracker initialized")
                
                if abs(current_count - self._last_process_count) > 0:  # Only when there's change
                    print(f"🔍 DEBUG: Found {current_count} MuMu-related processes (was {self._last_process_count})")
                    self._last_process_count = current_count
            
            # Consolidate processes by instance ID
            detected_instances = self._consolidate_instances(mumu_processes)
            
            # Update tracked instances
            for instance_id, instance_data in detected_instances.items():
                self.tracked_instances[instance_id] = {
                    'status': '🟢 Running',
                    'real_status': 'running',
                    'cpu': instance_data['total_cpu'],
                    'memory': instance_data['total_memory'],
                    'last_update': current_time,
                    'source': 'global_ai_tracker',
                    'pid': instance_data['primary_process']['pid'] if instance_data['primary_process'] else None,
                    'process_name': instance_data['primary_process']['name'] if instance_data['primary_process'] else 'Unknown',
                    'process_count': len(instance_data['processes'])
                }
                
                if self.debug_mode:
                    print(f"✅ DEBUG: Global tracked Instance {instance_id}: {instance_data['primary_process']['name'] if instance_data['primary_process'] else 'Unknown'} "
                          f"({len(instance_data['processes'])} processes)")
            
            # Only emit signals if there are actual changes (để giảm UI updates)
            changes_detected = False
            
            # Check for new instances
            for instance_id, data in self.tracked_instances.items():
                if instance_id not in old_instances:
                    # New instance detected
                    self.instance_status_changed.emit(instance_id, data['status'], data)
                    changes_detected = True
            
            # Check for stopped instances
            for instance_id in old_instances:
                if instance_id not in self.tracked_instances:
                    # Instance stopped
                    stopped_data = {'status': '🔴 Stopped', 'real_status': 'stopped'}
                    self.instance_status_changed.emit(instance_id, stopped_data['status'], stopped_data)
                    changes_detected = True
            
            # Only emit general update if there are changes
            if changes_detected or len(old_instances) != len(self.tracked_instances):
                self.instances_updated.emit(self.tracked_instances)
            
            self.last_scan_time = current_time
            
            # Simplified logging (chỉ khi có changes)
            if changes_detected and not self.debug_mode:
                print(f"🤖 AI Tracker: {len(self.tracked_instances)} instances active")
            elif self.debug_mode:
                print(f"✅ DEBUG: Global AI Tracker completed - {len(self.tracked_instances)} active instances")
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ DEBUG: Global AI Tracker error: {e}")
    
    def _scan_mumu_processes(self) -> List[Dict]:
        """Scan for MuMu-related processes"""
        mumu_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
            try:
                proc_name = proc.info['name'].lower()
                cmdline = ' '.join(proc.info['cmdline'] or []).lower()
                
                # MuMu keywords
                mumu_keywords = ['mumu', 'nemu']
                android_keywords = ['android', 'emulator']
                
                # Categorize processes
                is_mumu_primary = any(keyword in proc_name for keyword in mumu_keywords)
                is_android_emu = any(keyword in proc_name for keyword in android_keywords)
                is_mumu_cmdline = any(keyword in cmdline for keyword in mumu_keywords + ['instance', 'player'])
                
                # Exclude false positives
                false_positives = ['nevkms', 'system32', 'windows', 'microsoft', 'nvidia', 'intel', 'dwm', 'explorer']
                is_false_positive = any(keyword in proc_name for keyword in false_positives)
                
                if (is_mumu_primary or is_android_emu or is_mumu_cmdline) and not is_false_positive:
                    proc_info = proc.info.copy()
                    proc_info['category'] = 'primary' if is_mumu_primary else 'secondary' if is_android_emu else 'tertiary'
                    mumu_processes.append(proc_info)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return mumu_processes
    
    def _consolidate_instances(self, mumu_processes: List[Dict]) -> Dict[int, Dict]:
        """Consolidate multiple processes for same instance"""
        detected_instances = {}
        
        for proc_info in mumu_processes:
            try:
                instance_id = self._extract_instance_id_from_process(proc_info)
                if instance_id is not None:
                    if instance_id not in detected_instances:
                        detected_instances[instance_id] = {
                            'processes': [],
                            'total_cpu': 0,
                            'total_memory': 0,
                            'primary_process': None
                        }
                    
                    # Add process to instance group
                    detected_instances[instance_id]['processes'].append(proc_info)
                    detected_instances[instance_id]['total_cpu'] += proc_info.get('cpu_percent', 0)
                    detected_instances[instance_id]['total_memory'] += proc_info.get('memory_percent', 0)
                    
                    # Choose primary process
                    category = proc_info.get('category', 'tertiary')
                    current_primary = detected_instances[instance_id]['primary_process']
                    
                    if (current_primary is None or 
                        (category == 'primary' and current_primary.get('category') != 'primary') or
                        (category == 'secondary' and current_primary.get('category') == 'tertiary')):
                        detected_instances[instance_id]['primary_process'] = proc_info
                        
            except Exception as e:
                print(f"⚠️ DEBUG: Error processing proc_info: {e}")
        
        return detected_instances
    
    def _extract_instance_id_from_process(self, proc_info: Dict) -> Optional[int]:
        """Extract instance ID from process info"""
        try:
            cmdline = ' '.join(proc_info.get('cmdline', []))
            proc_name = proc_info.get('name', '')
            
            # Enhanced patterns for MuMu
            patterns = [
                # HIGH PRIORITY: Direct instance ID patterns
                r'--instance[-_]id\s+(\d+)',
                r'-id\s+(\d+)', 
                r'instance[_-]?(\d+)',
                r'-v\s+(\d+)',  # MuMuPlayer.exe -v 1
                
                # MEDIUM PRIORITY: Path and config patterns
                r'mumu.*?(\d+)',
                r'nemu[_-]?(\d+)',
                r'emulator[_-]?(\d+)',
                r'player[_-]?(\d+)',
                
                # LOW PRIORITY: Heuristic patterns
                r'(\d+)\.exe',
                r'vm(\d+)',
                r'android[_-]?(\d+)',
            ]
            
            # Try patterns in order of priority
            for pattern in patterns:
                # Try cmdline first
                match = re.search(pattern, cmdline, re.IGNORECASE)
                if match:
                    instance_id = int(match.group(1))
                    if 0 <= instance_id <= 1000:
                        return instance_id
                
                # Try process name
                match = re.search(pattern, proc_name, re.IGNORECASE)
                if match:
                    instance_id = int(match.group(1))
                    if 0 <= instance_id <= 1000:
                        return instance_id
            
            # Smart heuristics for primary MuMu processes
            if any(keyword in proc_name.lower() for keyword in ['mumu', 'nemu']):
                # Look for single digits in cmdline
                numbers = re.findall(r'\b(\d+)\b', cmdline)
                for num_str in numbers:
                    num = int(num_str)
                    if 0 <= num <= 50:  # Reasonable instance range
                        return num
                
                # If no clear ID found, assume instance 1 for primary processes
                if any(keyword in proc_name.lower() for keyword in ['mumumultiplayer', 'mumuservice', 'mumuvmm']):
                    return 1
            
            return None
            
        except Exception as e:
            print(f"⚠️ DEBUG: Error extracting instance ID: {e}")
            return None
    
    def get_tracked_instances(self) -> Dict[int, Dict]:
        """Get current tracked instances"""
        return self.tracked_instances.copy()
    
    def start_tracking(self):
        """Start AI tracking"""
        self.is_active = True
        if not self.tracker_timer.isActive():
            self.tracker_timer.start(self.scan_interval)  # Use optimized interval
        print("🤖 Global AI Tracker started (Performance optimized)")
    
    def stop_tracking(self):
        """Stop AI tracking"""
        self.is_active = False
        self.tracker_timer.stop()
        print("🤖 Global AI Tracker stopped")
    
    def set_debug_mode(self, enabled: bool):
        """Enable/disable debug mode"""
        self.debug_mode = enabled
        print(f"🤖 AI Tracker debug mode: {'Enabled' if enabled else 'Disabled'}")
    
    def set_scan_interval(self, interval_ms: int):
        """Change scan interval (minimum 5 seconds to avoid UI lag)"""
        if interval_ms < 5000:
            interval_ms = 5000
        self.scan_interval = interval_ms
        if self.tracker_timer.isActive():
            self.tracker_timer.stop()
            self.tracker_timer.start(self.scan_interval)
        print(f"🤖 AI Tracker scan interval set to {interval_ms/1000} seconds")
    
    def update_instance_in_table(self, table_widget, instance_id: int, status: str, data: Dict):
        """Update instance status in table widget (Performance optimized)"""
        try:
            if not table_widget:
                return
            
            # Disable table updates để batch processing
            table_widget.setUpdatesEnabled(False)
            
            # Find the row for this instance
            for row in range(table_widget.rowCount()):
                item = table_widget.item(row, 0)  # Column 0: ID (#)
                if item and item.text() == str(instance_id):
                    
                    # Update STATUS column (Column 2) với optimized colors
                    status_item = QTableWidgetItem(status)
                    
                    # Optimized color setting
                    if '🟢' in status:
                        status_item.setBackground(QColor(45, 74, 34))  # Dark green
                        status_item.setForeground(QColor(166, 226, 46))  # Bright green
                    elif '🔴' in status:
                        status_item.setBackground(QColor(58, 42, 42))  # Dark red  
                        status_item.setForeground(QColor(249, 38, 114))  # Bright red
                    elif '🟡' in status:
                        status_item.setBackground(QColor(58, 58, 42))  # Dark yellow
                        status_item.setForeground(QColor(230, 219, 116))  # Bright yellow
                    
                    table_widget.setItem(row, 2, status_item)  # Column 2: Status
                    
                    # Only update CPU/Memory if significantly different để avoid unnecessary updates
                    if 'cpu' in data and table_widget.columnCount() > 4:
                        current_cpu = table_widget.item(row, 4)
                        new_cpu_value = f"{data['cpu']:.1f}%"
                        if not current_cpu or current_cpu.text() != new_cpu_value:
                            cpu_item = QTableWidgetItem(new_cpu_value)
                            cpu_item.setForeground(QColor(255, 255, 255))
                            table_widget.setItem(row, 4, cpu_item)  # Column 4: CPU %
                    
                    # Memory update với same optimization
                    if 'memory' in data and table_widget.columnCount() > 5:
                        current_mem = table_widget.item(row, 5)
                        new_mem_value = f"{data['memory']:.1f}%"
                        if not current_mem or current_mem.text() != new_mem_value:
                            mem_item = QTableWidgetItem(new_mem_value)
                            mem_item.setForeground(QColor(255, 255, 255))
                            table_widget.setItem(row, 5, mem_item)  # Column 5: Memory
                    
                    break
            
            # Re-enable updates và force refresh
            table_widget.setUpdatesEnabled(True)
            
        except Exception as e:
            # Silent error handling to avoid spam
            if hasattr(self, 'debug_mode') and self.debug_mode:
                print(f"❌ AI Table Update Error: {e}")
            # Ensure updates are re-enabled
            if table_widget:
                table_widget.setUpdatesEnabled(True)


# Global instance
global_ai_tracker = GlobalAITracker()
