import tkinter as tk
from ui.pages.home_page import HomePage
from ui.pages.projects_page import ProjectsPage
from ui.pages.settings_page import SettingsPage
from ui.components.sidebar import Sidebar

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Snapshot Analyzer")
        self.geometry("800x600")
        
        # Configure grid weights for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Container for all frames
        container = tk.Frame(self)
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self._init_frames(container)

        # Current project and date
        self.current_project = None
        self.current_date = None
        
        # Navigation sidebar
        self._create_sidebar()
        
        # Show initial frame
        self.show_page("HomePage")
    
    def _init_frames(self, container):
        # Initialize all pages
        for F in (HomePage, ProjectsPage, SettingsPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_page(self, frame_name):
        frame = self.frames[frame_name]
        frame.show()
        frame.refresh()
        
    # Update the current project and date
    def update_selected_project(self, project: str, date: str):
        self.current_project = project
        self.current_date = date
        # Refresh the current page to reflect the new selection
        current_frame = [f for f in self.frames.values() if str(f) == self.focus_get()][0]
        current_frame.refresh()
        
    def _create_sidebar(self):
        sidebar = Sidebar(self, self)
        sidebar.grid(row=0, column=0, sticky="nsew")
