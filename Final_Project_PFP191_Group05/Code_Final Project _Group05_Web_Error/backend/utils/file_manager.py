"""
File Manager utility for Campus Event Management System
"""

import json
import csv
import os
from typing import Any, Dict, List
from datetime import datetime


class FileManager:
    """Lớp quản lý file JSON và CSV"""
    
    def __init__(self):
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Tạo thư mục data nếu chưa tồn tại"""
        directories = ['data', 'data/reports']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def load_json(self, filename: str, default: Any = None) -> Any:
        """Load dữ liệu từ file JSON"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                return default if default is not None else {}
        except (json.JSONDecodeError, FileNotFoundError):
            return default if default is not None else {}
    
    def save_json(self, filename: str, data: Any) -> bool:
        """Lưu dữ liệu vào file JSON"""
        try:
            # Tạo thư mục nếu chưa tồn tại
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Lỗi lưu file JSON {filename}: {str(e)}")
            return False
    
    def export_to_csv(self, filename: str, data: List[Dict], fieldnames: List[str] = None) -> bool:
        """Xuất dữ liệu ra file CSV"""
        try:
            if not data:
                return False
            
            # Tạo thư mục nếu chưa tồn tại
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Sử dụng fieldnames từ item đầu tiên nếu không được cung cấp
            if not fieldnames:
                fieldnames = list(data[0].keys())
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return True
        except Exception as e:
            print(f"Lỗi xuất file CSV {filename}: {str(e)}")
            return False
    
    def load_csv(self, filename: str) -> List[Dict]:
        """Load dữ liệu từ file CSV"""
        try:
            data = []
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    data = list(reader)
            return data
        except Exception as e:
            print(f"Lỗi load file CSV {filename}: {str(e)}")
            return []
    
    def backup_data(self, backup_suffix: str = None) -> Dict[str, bool]:
        """Sao lưu tất cả dữ liệu"""
        try:
            if not backup_suffix:
                backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_dir = f"data/backups/backup_{backup_suffix}"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            files_to_backup = [
                'data/users.json',
                'data/events.json',
                'data/registrations.json'
            ]
            
            results = {}
            for filename in files_to_backup:
                if os.path.exists(filename):
                    backup_filename = os.path.join(backup_dir, os.path.basename(filename))
                    data = self.load_json(filename, [])
                    results[filename] = self.save_json(backup_filename, data)
                else:
                    results[filename] = False
            
            return results
        except Exception as e:
            print(f"Lỗi backup dữ liệu: {str(e)}")
            return {}
    
    def restore_data(self, backup_suffix: str) -> Dict[str, bool]:
        """Khôi phục dữ liệu từ backup"""
        try:
            backup_dir = f"data/backups/backup_{backup_suffix}"
            
            if not os.path.exists(backup_dir):
                return {'error': 'Backup không tồn tại'}
            
            files_to_restore = [
                'users.json',
                'events.json', 
                'registrations.json'
            ]
            
            results = {}
            for filename in files_to_restore:
                backup_file = os.path.join(backup_dir, filename)
                target_file = os.path.join('data', filename)
                
                if os.path.exists(backup_file):
                    data = self.load_json(backup_file, [])
                    results[filename] = self.save_json(target_file, data)
                else:
                    results[filename] = False
            
            return results
        except Exception as e:
            print(f"Lỗi restore dữ liệu: {str(e)}")
            return {}
    
    def get_file_info(self, filename: str) -> Dict:
        """Lấy thông tin file"""
        try:
            if os.path.exists(filename):
                stat = os.stat(filename)
                return {
                    'exists': True,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                }
            else:
                return {'exists': False}
        except Exception as e:
            return {'exists': False, 'error': str(e)}
    
    def cleanup_old_backups(self, keep_days: int = 30) -> int:
        """Dọn dẹp backup cũ"""
        try:
            backup_dir = "data/backups"
            if not os.path.exists(backup_dir):
                return 0
            
            current_time = datetime.now()
            deleted_count = 0
            
            for item in os.listdir(backup_dir):
                item_path = os.path.join(backup_dir, item)
                if os.path.isdir(item_path):
                    # Lấy thời gian tạo thư mục backup
                    creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
                    age_days = (current_time - creation_time).days
                    
                    if age_days > keep_days:
                        # Xóa thư mục backup cũ
                        import shutil
                        shutil.rmtree(item_path)
                        deleted_count += 1
            
            return deleted_count
        except Exception as e:
            print(f"Lỗi dọn dẹp backup: {str(e)}")
            return 0
    
    def generate_report_filename(self, report_type: str, extension: str = 'csv') -> str:
        """Tạo tên file báo cáo với timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"data/reports/{report_type}_report_{timestamp}.{extension}"
    
    def delete_file(self, filename: str) -> bool:
        """Xóa file"""
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return True
            return False
        except Exception as e:
            print(f"Lỗi xóa file {filename}: {str(e)}")
            return False