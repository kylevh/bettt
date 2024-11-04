from ui.pages.base_page import BasePage
import tkinter as tk

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._init_ui()
        
    def _init_ui(self):
        # Create your home page widgets here
        label = tk.Label(self, text="Settings Page")
        label.pack(pady=10)
        
    def refresh(self):
        # Update any dynamic content
        pass