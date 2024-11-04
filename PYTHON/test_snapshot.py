from core.snapshot_manager import SnapshotManager
from pathlib import Path

def main():
    # Get the current file's directory and construct path to snapshots
    current_dir = Path(__file__).parent
    snapshots_path = current_dir.parent / "SOAP2" / "snapshots"
    
    # Initialize the snapshot manager with the correct snapshots directory
    manager = SnapshotManager(str(snapshots_path))
    
    # Scan all snapshots
    manager.scan_snapshots()
    
    # Print all projects
    print("\nAvailable Projects:")
    print("-" * 20)
    for project in sorted(manager.projects_list):
        print(project)
        
        # Print dates for each project
        dates = manager.get_project_dates(project)
        print("  Dates available:")
        for date in dates:
            snapshots = manager.get_project_snapshots(project, date)
            print(f"    {date}: {len(snapshots)} snapshots")
        print()

if __name__ == "__main__":
    main()