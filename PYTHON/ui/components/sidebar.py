import tkinter as tk
from tkinter import ttk
from core.snapshot_manager import SnapshotManager
from pathlib import Path
import calendar
from datetime import datetime

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50", width=200)
        self.controller = controller
        self.pack_propagate(False)
        
        # Initialize SnapshotManager
        snapshots_path = Path(__file__).parent.parent.parent.parent / "SOAP2" / "snapshots"
        self.snapshot_manager = SnapshotManager(str(snapshots_path))
        self.snapshot_manager.scan_snapshots()
        
        self._init_ui()
        
    def _init_ui(self):
        # Sidebar title
        title = tk.Label(
            self, 
            text="Navigation",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 12, "bold")
        )
        title.pack(pady=10, padx=5)
        
        # Project selection frame
        project_frame = tk.Frame(self, bg="#2c3e50")
        project_frame.pack(pady=5, padx=10, fill="x")
        
        project_label = tk.Label(
            project_frame,
            text="Select Project:",
            bg="#2c3e50",
            fg="white"
        )
        project_label.pack(anchor="w")
        
        # Project dropdown
        self.project_var = tk.StringVar()
        self.project_dropdown = ttk.Combobox(
            project_frame,
            textvariable=self.project_var,
            state="readonly",
            values=sorted(self.snapshot_manager.projects_list)
        )
        self.project_dropdown.pack(pady=5, fill="x")
        self.project_dropdown.bind('<<ComboboxSelected>>', self._on_project_selected)
        
        # Date selection with calendar
        date_label = tk.Label(
            project_frame,
            text="Select Date:",
            bg="#2c3e50",
            fg="white"
        )
        date_label.pack(anchor="w", pady=(10,0))
        
        # Calendar frame
        self.calendar_frame = tk.Frame(project_frame, bg="#2c3e50")
        self.calendar_frame.pack(pady=5, fill="x")
        
        # Month navigation frame
        month_nav_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
        month_nav_frame.pack(fill="x")
        
        self.prev_month_btn = tk.Button(
            month_nav_frame,
            text="<",
            command=self._prev_month,
            bg="#34495e",
            fg="white",
            relief="flat"
        )
        self.prev_month_btn.pack(side="left")
        
        self.month_label = tk.Label(
            month_nav_frame,
            text="",
            bg="#2c3e50",
            fg="white"
        )
        self.month_label.pack(side="left", expand=True)
        
        self.next_month_btn = tk.Button(
            month_nav_frame,
            text=">",
            command=self._next_month,
            bg="#34495e",
            fg="white",
            relief="flat"
        )
        self.next_month_btn.pack(side="right")
        
        # Days of week header
        days_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
        days_frame.pack(fill="x")
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            tk.Label(
                days_frame,
                text=day,
                bg="#2c3e50",
                fg="white",
                width=3
            ).pack(side="left")
        
        # Calendar days
        self.days_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
        self.days_frame.pack(fill="x")
        
        self.current_date = datetime.now()
        self.available_dates = set()
        self.date_var = tk.StringVar()
        
        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#2c3e50")
        nav_frame.pack(pady=20, fill="x")
        self._create_nav_button("Home", "HomePage", nav_frame)
        self._create_nav_button("Projects", "ProjectsPage", nav_frame)
        self._create_nav_button("Settings", "SettingsPage", nav_frame)
        
    def _create_nav_button(self, text, page_id, parent):
        btn = tk.Button(
            parent,
            text=text,
            bg="#34495e",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            width=15,
            command=lambda: self.controller.show_page(page_id)
        )
        btn.pack(pady=5, padx=10)
        
    def _update_calendar(self):
        # Clear existing calendar days and frames
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
            
        # Recreate the month navigation frame
        month_nav_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
        month_nav_frame.pack(fill="x")
        
        self.prev_month_btn = tk.Button(
            month_nav_frame,
            text="<",
            command=self._prev_month,
            bg="#34495e",
            fg="white",
            relief="flat"
        )
        self.prev_month_btn.pack(side="left")
        
        self.month_label = tk.Label(
            month_nav_frame,
            text=f"{calendar.month_name[self.current_date.month]} {self.current_date.year}",
            bg="#2c3e50",
            fg="white"
        )
        self.month_label.pack(side="left", expand=True)
        
        self.next_month_btn = tk.Button(
            month_nav_frame,
            text=">",
            command=self._next_month,
            bg="#34495e",
            fg="white",
            relief="flat"
        )
        self.next_month_btn.pack(side="right")
        
        # Days of week header
        days_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
        days_frame.pack(fill="x")
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            tk.Label(
                days_frame,
                text=day,
                bg="#2c3e50",
                fg="white",
                width=3
            ).pack(side="left")
        
        # Calendar days
        self.days_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
        self.days_frame.pack(fill="x")
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Create calendar buttons
        for week in cal:
            week_frame = tk.Frame(self.calendar_frame, bg="#2c3e50")
            week_frame.pack(fill="x")
            for day in week:
                if day == 0:
                    # Empty day
                    tk.Label(
                        week_frame,
                        text="",
                        width=3,
                        bg="#2c3e50"
                    ).pack(side="left")
                else:
                    date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                    if date_str in self.available_dates:
                        btn = tk.Button(
                            week_frame,
                            text=str(day),
                            width=3,
                            bg="#34495e",
                            fg="white",
                            relief="flat",
                            command=lambda d=date_str: self._on_date_clicked(d)
                        )
                    else:
                        btn = tk.Label(
                            week_frame,
                            text=str(day),
                            width=3,
                            bg="#2c3e50",
                            fg="gray"
                        )
                    btn.pack(side="left")
            
    def _prev_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year-1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month-1)
        self._update_calendar()

    def _next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year+1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month+1)
        self._update_calendar()

    def _on_date_clicked(self, date_str):
        self.date_var.set(date_str)
        self._on_date_selected(None)
        
    def _on_project_selected(self, event):
        project = self.project_var.get()
        if project:
            # Update available dates for the calendar
            dates = self.snapshot_manager.get_project_dates(project)
            self.available_dates = set(dates)
            self._update_calendar()
            if dates:
                self.date_var.set(dates[0])
                self._on_date_selected(None)
                
    def _on_date_selected(self, event):
        project = self.project_var.get()
        date = self.date_var.get()
        if project and date:
            # Notify the controller about the selection
            self.controller.update_selected_project(project, date)