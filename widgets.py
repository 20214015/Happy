# widgets.py - Các widget PyQt6 tùy chỉnh cho ứng dụng

from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtCore import Qt, pyqtSignal
from constants import TableColumn

class StatusPillDelegate(QStyledItemDelegate):
    """Vẽ một viên thuốc màu cho các trạng thái trong bảng."""
    # Tối ưu hóa: Tạo sẵn các đối tượng QColor để tránh tạo lại liên tục
    COLORS = {
        "offline": QColor("#631119"),
        "running": QColor("#28a745"),
        "starting": QColor("#3498db"),
        "stopping": QColor("#f39c12"),
        "restarting": QColor("#8e44ad"),
    }
    
    def paint(self, painter: QPainter, option, index):
        status_data = index.data(Qt.ItemDataRole.UserRole)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = option.rect.adjusted(8, 6, -8, -6)

        # Mặc định
        text = "Offline"
        bg_color = self.COLORS["offline"]

        if isinstance(status_data, bool):
            if status_data: # is_running is True
                text = "Running"
                bg_color = self.COLORS["running"]
        elif isinstance(status_data, str):
            text = f"{status_data.capitalize()}..."
            bg_color = self.COLORS.get(status_data, self.COLORS["offline"])
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)

        painter.setPen(QPen(Qt.GlobalColor.white))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.restore()



# === Model/View for instances table ===
from PyQt6.QtCore import QAbstractTableModel, QSortFilterProxyModel, QModelIndex, Qt, QVariant
from typing import List, Dict, Any, Optional
import collections

try:
    # Import here to avoid circulars when this file is used standalone
    from constants import TableColumn
except Exception:
    TableColumn = type("TableColumn", (), {"CHECKBOX":0, "STT":1, "NAME":2, "STATUS":3, "ADB":4, "DISK_USAGE":5, "SPACER":6})

class InstancesModel(QAbstractTableModel):
    stats_updated = pyqtSignal(int, int) # total, running

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows: List[Dict[str, Any]] = []  # each: {'index': int, 'info': dict, 'checked': bool}
        self._ui_states: Dict[int, Any] = {}   # transient status per index
        self._index_map: Dict[int, int] = {} # Map vm_index to row_index for fast lookup

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return 7

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            headers = ["", "Index", "Tên máy", "Trạng thái", "ADB", "Dung lượng", ""]
            return headers[section] if 0 <= section < len(headers) else ""
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == TableColumn.CHECKBOX:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        r = index.row()
        c = index.column()
        
        # Tối ưu hóa: Tránh truy cập self._rows nhiều lần
        try:
            row = self._rows[r]
        except IndexError:
            return None
            
        info = row.get("info", {})
        idx = row.get("index")

        if c == TableColumn.CHECKBOX:
            if role == Qt.ItemDataRole.CheckStateRole:
                return Qt.CheckState.Checked if row.get("checked", False) else Qt.CheckState.Unchecked
            return None

        if c == TableColumn.STT:
            if role == Qt.ItemDataRole.DisplayRole:
                return str(idx) if idx is not None else "N/A"
            if role == Qt.ItemDataRole.UserRole:
                return idx if idx is not None else -1
            if role == Qt.ItemDataRole.TextAlignmentRole:
                return int(Qt.AlignmentFlag.AlignCenter)
            return None

        if c == TableColumn.NAME:
            if role == Qt.ItemDataRole.DisplayRole:
                return info.get("name", "N/A")
            if role == Qt.ItemDataRole.UserRole:
                return idx
            return None

        if c == TableColumn.STATUS:
            if role == Qt.ItemDataRole.UserRole:
                if idx in self._ui_states:
                    return self._ui_states[idx]
                return info.get("is_process_started", False)
            if role == Qt.ItemDataRole.DisplayRole:
                # Delegate sẽ xử lý việc hiển thị text
                return ""
            return None

        if c == TableColumn.ADB:
            if role == Qt.ItemDataRole.DisplayRole:
                val = info.get("adb_port", "—")
                return str(val if val not in (None, "") else "—")
            return None

        if c == TableColumn.DISK_USAGE:
            if role == Qt.ItemDataRole.DisplayRole:
                disk_bytes = info.get("disk_size_bytes", 0) or 0
                if disk_bytes > 0:
                    gb = disk_bytes / (1024**3)
                    return f"{gb:.2f} GB" if gb >= 1 else f"{disk_bytes / (1024**2):.2f} MB"
                raw_disk = info.get("disk_usage", "")
                return str(raw_disk) if raw_disk else "0MB"
            if role == Qt.ItemDataRole.TextAlignmentRole:
                return int(Qt.AlignmentFlag.AlignCenter)
            return None

        return None

    def setData(self, index: QModelIndex, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False
        r = index.row()
        c = index.column()
        if c == TableColumn.CHECKBOX and role == Qt.ItemDataRole.CheckStateRole:
            self._rows[r]["checked"] = (value == Qt.CheckState.Checked)
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
            return True
        return False

    def set_rows(self, items):
        """Cập nhật model một cách thông minh, tránh reset toàn bộ."""
        # Handle both tuple (index, info) and dict formats
        if items and isinstance(items[0], tuple):
            # Convert tuple format (index, info) to dict format
            new_data_map = {idx: {'index': idx, 'info': info} for idx, info in items}
        else:
            # Handle dict format for backward compatibility
            new_data_map = {item['index']: item for item in items}
        
        new_indices = set(new_data_map.keys())
        old_indices = set(self._index_map.keys())

        # 1. Xác định các hàng cần xóa
        to_remove_indices = old_indices - new_indices
        if to_remove_indices:
            # Sắp xếp ngược để không làm thay đổi index của các hàng chưa xóa
            rows_to_remove = sorted([self._index_map[idx] for idx in to_remove_indices], reverse=True)
            for row_idx in rows_to_remove:
                self.beginRemoveRows(QModelIndex(), row_idx, row_idx)
                del self._rows[row_idx]
                self.endRemoveRows()
            # Cập nhật lại map sau khi xóa
            self._rebuild_index_map()

        # 2. Xác định các hàng cần cập nhật và thêm mới
        to_update_indices = old_indices.intersection(new_indices)
        to_add_indices = new_indices - old_indices

        # Cập nhật các hàng hiện có
        for vm_index in to_update_indices:
            row_idx = self._index_map[vm_index]
            new_info = new_data_map[vm_index]['info']
            # So sánh sâu hơn để tránh cập nhật không cần thiết
            if not self._are_dicts_equal(self._rows[row_idx]['info'], new_info):
                self._rows[row_idx]['info'] = new_info
                # Phát tín hiệu thay đổi cho cả hàng
                first_col = self.index(row_idx, 0)
                last_col = self.index(row_idx, self.columnCount() - 1)
                self.dataChanged.emit(first_col, last_col)

        # Thêm các hàng mới
        if to_add_indices:
            new_rows_data = [new_data_map[idx] for idx in sorted(list(to_add_indices))]
            first_row_to_add = self.rowCount()
            self.beginInsertRows(QModelIndex(), first_row_to_add, first_row_to_add + len(new_rows_data) - 1)
            for item in new_rows_data:
                self._rows.append(dict(index=item['index'], info=item['info'], checked=False))
            self.endInsertRows()
            # Cập nhật lại map sau khi thêm
            self._rebuild_index_map()

        # 3. Tính toán và phát tín hiệu thống kê
        total_count = self.rowCount()
        running_count = sum(1 for row in self._rows if row.get('info', {}).get('is_process_started'))
        self.stats_updated.emit(total_count, running_count)

    def _rebuild_index_map(self):
        """Xây dựng lại map từ vm_index sang row index."""
        self._index_map = {row['index']: i for i, row in enumerate(self._rows)}

    def _are_dicts_equal(self, d1: Dict, d2: Dict) -> bool:
        """So sánh hai dictionary, bỏ qua một số key không quan trọng."""
        # Các key có thể thay đổi thường xuyên nhưng không ảnh hưởng đến hiển thị
        ignored_keys = {'pid', 'headless_pid', 'main_wnd', 'render_wnd'}
        keys1 = set(d1.keys()) - ignored_keys
        keys2 = set(d2.keys()) - ignored_keys
        if keys1 != keys2:
            return False
        for key in keys1:
            if d1[key] != d2[key]:
                return False
        return True

    def update_row_by_index(self, idx: int, info: Dict[str, Any]):
        """Cập nhật thông tin cho một hàng dựa trên vm_index."""
        if idx in self._index_map:
            row_idx = self._index_map[idx]
            self._rows[row_idx]["info"] = info
            tl = self.index(row_idx, 0)
            br = self.index(row_idx, self.columnCount()-1)
            self.dataChanged.emit(tl, br, [])

    def set_all_checked(self, checked: bool):
        """Tối ưu hóa: Chỉ phát tín hiệu dataChanged cho cột checkbox."""
        if not self._rows: return
        # Không cần layoutAboutToBeChanged/layoutChanged vì layout không đổi
        for row in self._rows:
            row["checked"] = checked
        
        if self.rowCount() > 0:
            # Chỉ cần phát tín hiệu cho cột checkbox
            tl = self.index(0, TableColumn.CHECKBOX)
            br = self.index(self.rowCount()-1, TableColumn.CHECKBOX)
            self.dataChanged.emit(tl, br, [Qt.ItemDataRole.CheckStateRole])

    def get_checked_indices(self) -> List[int]:
        return [row["index"] for row in self._rows if row.get("checked")]

    def find_source_row_by_index(self, idx: int) -> int:
        return self._index_map.get(idx, -1)

    def set_ui_states(self, ui_states: Dict[int, Any]):
        """Set transient ui status ('starting', 'stopping', ...) and refresh status column."""
        self._ui_states = dict(ui_states or {})
        if self.rowCount() > 0:
            tl = self.index(0, TableColumn.STATUS)
            br = self.index(self.rowCount()-1, TableColumn.STATUS)
            self.dataChanged.emit(tl, br, [Qt.ItemDataRole.UserRole])

class InstancesProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._keyword = ""
        self._status = "Tất cả"
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def set_filters(self, keyword: str, status: str):
        self._keyword = (keyword or "").strip().lower()
        self._status = status or "Tất cả"
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        m: InstancesModel = self.sourceModel()  # type: ignore
        if m is None: return True
        # status
        row = m._rows[source_row]
        info = row.get("info", {})
        running = info.get("is_process_started", False)
        if self._status == "Đang chạy" and not running: return False
        if self._status == "Đã tắt" and running: return False
        # keyword
        if not self._keyword:
            return True
        name = (info.get("name") or "").lower()
        return self._keyword in name or self._keyword == str(row.get("index", "")).lower()

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        # Override STT to show VM index and provide proper sorting
        if index.column() == TableColumn.STT:
            # Validate that index belongs to this proxy model
            if index.model() != self:
                return super().data(index, role)
                
            source_index = self.mapToSource(index)
            if source_index.isValid():
                row_data = self.sourceModel()._rows[source_index.row()]
                vm_index = row_data.get("index")
                
                if role == Qt.ItemDataRole.DisplayRole:
                    return str(vm_index) if vm_index is not None else "N/A"
                elif role == Qt.ItemDataRole.UserRole:
                    # Return integer for proper numeric sorting
                    return vm_index if vm_index is not None else -1
                    
        return super().data(index, role)
    
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """Custom sorting logic for proper numeric sorting of Index column."""
        # For STT column, sort by numeric value instead of string
        if left.column() == TableColumn.STT:
            left_data = self.sourceModel().data(left, Qt.ItemDataRole.UserRole)
            right_data = self.sourceModel().data(right, Qt.ItemDataRole.UserRole)
            
            # Handle None/invalid values
            if left_data is None:
                left_data = -1
            if right_data is None:
                right_data = -1
                
            return left_data < right_data
            
        # For other columns, use default sorting
        return super().lessThan(left, right)
