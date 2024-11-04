from ui.pages.base_page import BasePage
import tkinter as tk

class ProjectsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._init_ui()
        
    def _init_ui(self):
        self.info_label = tk.Label(self, text="Select a project to begin")
        self.info_label.pack(pady=10)
        
    def refresh(self):
        if self.controller.current_project and self.controller.current_date:
            self.info_label.config(
                text=f"Viewing project: {self.controller.current_project}\n"
                     f"Date: {self.controller.current_date}"
            )