import tkinter as tk

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
    def show(self):
        self.tkraise()
        
    def refresh(self):
        # Override in child classes if needed
        pass