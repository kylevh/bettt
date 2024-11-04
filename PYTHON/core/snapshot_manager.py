from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
from typing import Dict, List, Tuple, Optional, Callable

class SnapshotManager:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.project_data: Dict[str, Dict[str, List[dict]]] = defaultdict(lambda: defaultdict(list))
        self.projects_list: set = set()
        self._ui_callback: Optional[Callable] = None

    def get_snapshots(self) -> List[Tuple[datetime, Path]]:
        """Return all snapshot directories sorted by date"""
        snapshots = []
        for path in self.root_path.iterdir():
            if path.is_dir():
                try:
                    date = datetime.strptime(path.name, "%Y-%m-%d")
                    snapshots.append((date, path))
                except ValueError:
                    continue
        return sorted(snapshots, key=lambda x: x[0], reverse=True)

    def scan_snapshots(self) -> Dict[str, Dict[str, List[dict]]]:
        """Scans the snapshot directory and organizes data by project and date"""
        self.project_data.clear()
        self.projects_list.clear()

        for date_folder in self.root_path.iterdir():
            if not date_folder.is_dir():
                continue

            for project_folder in date_folder.iterdir():
                if not project_folder.is_dir():
                    continue

                project_name = project_folder.name
                self.projects_list.add(project_name)

                for json_file in project_folder.glob("*.json"):
                    timestamp = self._parse_timestamp(json_file.name)
                    self.project_data[project_name][date_folder.name].append({
                        'timestamp': timestamp,
                        'file_path': json_file
                    })

        self._notify_ui_update()
        return dict(self.project_data)

    def load_snapshot_data(self, file_path: Path) -> dict:
        """Loads snapshot data from a JSON file"""
        try:
            return json.loads(file_path.read_text())
        except Exception as e:
            print(f"Error loading snapshot {file_path}: {e}")
            return {}

    def get_project_dates(self, project_name: str) -> List[str]:
        """Returns all dates available for a specific project"""
        return sorted(self.project_data[project_name].keys())

    def get_project_snapshots(self, project_name: str, date: Optional[str] = None) -> List[dict]:
        """Returns all snapshots for a project, optionally filtered by date"""
        if date:
            return sorted(self.project_data[project_name][date], 
                        key=lambda x: x['timestamp'])
        
        all_snapshots = []
        for date_snapshots in self.project_data[project_name].values():
            all_snapshots.extend(date_snapshots)
        return sorted(all_snapshots, key=lambda x: x['timestamp'])

    def register_ui_callback(self, callback: Callable) -> None:
        """Register a callback for UI updates"""
        self._ui_callback = callback

    def _notify_ui_update(self) -> None:
        """Notify UI components that data has been updated"""
        if self._ui_callback:
            self._ui_callback()

    @staticmethod
    def _parse_timestamp(filename: str) -> datetime:
        """Parse timestamp from filename (e.g., '2024-11-01_22-44-27.json')"""
        datetime_str = filename.split('.')[0]
        return datetime.strptime(datetime_str, '%Y-%m-%d_%H-%M-%S')