"""
GUI for Rex HVAC Checklist System
Optimized for Raspberry Pi 5 with OSOYOO 4.3" 800x480 DSI touchscreen
"""

import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import tkinter.font as tkFont
from config import *

class UI:
    """Tkinter GUI for HVAC checklist"""
    
    def __init__(self, root, job_manager, voice_handler):
        self.root = root
        self.job_manager = job_manager
        self.voice_handler = voice_handler
        
        # Configure window
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLOR_BG)
        
        # Try fullscreen on Pi
        try:
            self.root.attributes('-zoomed', True)
        except:
            pass
        
        # Current state
        self.current_unit = 1
        self.current_item_index = 0
        self.reading_entries = {}
        
        # Setup UI
        self.setup_styles()
        self.show_main_menu()
    
    def setup_styles(self):
        """Configure fonts and styles"""
        self.font_title = tkFont.Font(family=FONT_TITLE[0], size=FONT_TITLE[1], weight=FONT_TITLE[2])
        self.font_header = tkFont.Font(family=FONT_HEADER[0], size=FONT_HEADER[1], weight=FONT_HEADER[2])
        self.font_large = tkFont.Font(family=FONT_LARGE[0], size=FONT_LARGE[1])
        self.font_normal = tkFont.Font(family=FONT_NORMAL[0], size=FONT_NORMAL[1])
        self.font_small = tkFont.Font(family=FONT_SMALL[0], size=FONT_SMALL[1])
    
    def clear_screen(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display main menu"""
        self.clear_screen()
        
        # Header
        header = tk.Frame(self.root, bg=COLOR_HEADER, height=60)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header,
            text="Rex HVAC Checklist",
            font=self.font_title,
            bg=COLOR_HEADER,
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Main content
        content = tk.Frame(self.root, bg=COLOR_BG)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status
        status_text = "No Active Job"
        if self.job_manager.get_current_job():
            job = self.job_manager.get_job_summary()
            status_text = f"Active: {job['name']} ({job['num_units']} units)"
        
        status = tk.Label(
            content,
            text=status_text,
            font=self.font_normal,
            bg=COLOR_BG,
            fg=COLOR_TEXT
        )
        status.pack(pady=10)
        
        # Buttons
        btn_new = tk.Button(
            content,
            text="Start New Job",
            font=BUTTON_FONT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            bg=COLOR_BUTTON,
            fg="white",
            command=self.start_new_job
        )
        btn_new.pack(pady=10)
        
        btn_view = tk.Button(
            content,
            text="View Saved Jobs",
            font=BUTTON_FONT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            bg=COLOR_BUTTON,
            fg="white",
            command=self.show_saved_jobs
        )
        btn_view.pack(pady=10)
        
        btn_exit = tk.Button(
            content,
            text="Exit",
            font=BUTTON_FONT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            bg=COLOR_WARNING,
            fg="white",
            command=self.root.quit
        )
        btn_exit.pack(pady=10)
    
    def start_new_job(self):
        """Start a new job - ask for job name, units, and system types"""
        # Job name
        job_name = simpledialog.askstring(
            "New Job",
            "Enter job name:",
            parent=self.root
        )
        
        if not job_name:
            return
        
        # Number of units
        num_units = simpledialog.askinteger(
            "New Job",
            "Enter number of units:",
            minvalue=1,
            maxvalue=10,
            parent=self.root
        )
        
        if not num_units:
            return
        
        # Get system type for each unit
        unit_types = {}
        for i in range(1, num_units + 1):
            system_type = self.select_system_type(f"Unit {i} - Select System Type")
            if not system_type:
                messagebox.showwarning("Cancelled", "Job creation cancelled")
                return
            unit_types[i] = system_type
        
        # Create job with mixed unit types
        self.job_manager.create_job_with_units(job_name, unit_types)
        self.current_unit = 1
        self.current_item_index = 0
        
        messagebox.showinfo("Success", f"Created job: {job_name}\n{num_units} units")
        self.show_active_job()
    
    def select_system_type(self, prompt="Select System Type"):
        """Show dialog to select system type"""
        select_window = tk.Toplevel(self.root)
        select_window.title(prompt)
        select_window.geometry("500x250")
        select_window.resizable(False, False)
        
        # Center on parent
        select_window.transient(self.root)
        
        label = tk.Label(
            select_window,
            text=prompt,
            font=self.font_header,
            bg=COLOR_BG,
            fg=COLOR_TEXT
        )
        label.pack(pady=20)
        
        selected = tk.StringVar()
        
        button_frame = tk.Frame(select_window, bg=COLOR_BG)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for stype in SYSTEM_TYPES:
            btn = tk.Button(
                button_frame,
                text=stype,
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=COLOR_BUTTON,
                fg="white",
                command=lambda s=stype: (selected.set(s), select_window.destroy())
            )
            btn.pack(pady=10)
        
        self.root.wait_window(select_window)
        return selected.get() if selected.get() else None
    
    def show_active_job(self):
        """Display active job with checklist"""
        self.clear_screen()
        
        job = self.job_manager.get_current_job()
        if not job:
            self.show_main_menu()
            return
        
        # Configure grid layout with 3 rows: header, content, footer
        self.root.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.root.grid_rowconfigure(1, weight=1)  # Content - expandable
        self.root.grid_rowconfigure(2, weight=0)  # Footer - fixed
        self.root.grid_columnconfigure(0, weight=1)
        
        # ===== HEADER =====
        header = tk.Frame(self.root, bg=COLOR_HEADER, height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        job_info = tk.Label(
            header,
            text=f"{job['name']}",
            font=self.font_header,
            bg=COLOR_HEADER,
            fg="white"
        )
        job_info.pack(pady=10)
        
        # ===== CONTENT =====
        content = tk.Frame(self.root, bg=COLOR_BG)
        content.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content.grid_propagate(True)
        
        # Unit selector
        unit_frame = tk.Frame(content, bg=COLOR_BG)
        unit_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(unit_frame, text="Select Unit:", font=self.font_normal, bg=COLOR_BG).pack(side=tk.LEFT, padx=5)
        
        unit_buttons = tk.Frame(unit_frame, bg=COLOR_BG)
        unit_buttons.pack(side=tk.LEFT, fill=tk.X, padx=5)
        
        for i in range(1, len(job["units"]) + 1):
            btn_bg = COLOR_STATUS if i == self.current_unit else COLOR_BUTTON
            btn = tk.Button(
                unit_buttons,
                text=f"Unit {i}",
                width=8,
                bg=btn_bg,
                fg="white",
                font=BUTTON_FONT,
                command=lambda u=i: self.select_unit(u)
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Checklist
        unit = self.job_manager.get_unit(self.current_unit)
        if unit:
            self.show_unit_checklist(content, unit)
        
        # ===== FOOTER =====
        footer = tk.Frame(self.root, bg=COLOR_BG)
        footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        footer.grid_propagate(False)
        
        btn_save = tk.Button(
            footer,
            text="Save Job",
            font=BUTTON_FONT,
            width=12,
            bg=COLOR_STATUS,
            fg="white",
            command=self.save_job
        )
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_back = tk.Button(
            footer,
            text="Back to Menu",
            font=BUTTON_FONT,
            width=12,
            bg=COLOR_WARNING,
            fg="white",
            command=self.show_main_menu
        )
        btn_back.pack(side=tk.LEFT, padx=5, pady=5)
    
    def select_unit(self, unit_num):
        """Select a different unit"""
        self.sync_current_unit_readings()
        self.current_unit = unit_num
        self.current_item_index = 0
        self.show_active_job()

    def sync_current_unit_readings(self):
        """Persist current unit entry fields to job manager"""
        if not self.reading_entries:
            return
        
        for item_name, entry in self.reading_entries.items():
            try:
                self.save_reading_value(self.current_unit, item_name, entry.get())
            except tk.TclError:
                # Entry may be destroyed during screen transitions; skip stale refs.
                continue

    def save_reading_value(self, unit_number, item_name, value):
        """Persist one reading value to job manager"""
        self.job_manager.update_reading(unit_number, item_name, value)
    
    def show_unit_checklist(self, parent, unit):
        """Display checklist for current unit"""
        # Unit header with system type
        unit_header = tk.Label(
            parent,
            text=f"Unit {unit['unit_number']} - {unit['system_type']}",
            font=self.font_large,
            bg=COLOR_BG,
            fg=COLOR_HEADER
        )
        unit_header.pack(pady=5)
        
        checklist_frame = tk.Frame(parent, bg=COLOR_BG)
        checklist_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create scrollable frame
        canvas = tk.Canvas(checklist_frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(checklist_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add checklist items
        readings = unit.get("readings", {})
        self.reading_entries = {}
        
        if not readings:
            # No readings - show message
            empty_label = tk.Label(
                scrollable_frame,
                text="No readings for this unit",
                font=self.font_normal,
                bg=COLOR_BG,
                fg=COLOR_TEXT
            )
            empty_label.pack(pady=20)
        else:
            for item_name, reading_data in readings.items():
                item_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
                item_frame.pack(fill=tk.X, pady=3, padx=3)
                
                # Item name label
                name_label = tk.Label(
                    item_frame,
                    text=item_name,
                    font=self.font_normal,
                    bg="white",
                    justify=tk.LEFT
                )
                name_label.pack(anchor=tk.W, padx=10, pady=5)
                
                # Value entry
                value_frame = tk.Frame(item_frame, bg="white")
                value_frame.pack(fill=tk.X, padx=20, pady=3)
                
                tk.Label(value_frame, text="Value:", font=self.font_small, bg="white").pack(side=tk.LEFT, padx=5)
                
                entry = tk.Entry(value_frame, font=self.font_small, width=20)
                entry.insert(0, reading_data.get("value", "") or "")
                entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
                self.reading_entries[item_name] = entry
                
                def save_value(e=None, entry_ref=entry, item=item_name, u=unit["unit_number"]):
                    self.save_reading_value(u, item, entry_ref.get())
                
                entry.bind("<Return>", save_value)
                entry.bind("<FocusOut>", save_value)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_saved_jobs(self):
        """Display list of saved jobs"""
        self.clear_screen()
        
        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=1)  # Content
        self.root.grid_rowconfigure(2, weight=0)  # Footer
        self.root.grid_columnconfigure(0, weight=1)
        
        # Header
        header = tk.Frame(self.root, bg=COLOR_HEADER, height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        title = tk.Label(
            header,
            text="Saved Jobs",
            font=self.font_title,
            bg=COLOR_HEADER,
            fg="white"
        )
        title.pack(pady=10)
        
        # Content
        content = tk.Frame(self.root, bg=COLOR_BG)
        content.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        saved_jobs = self.job_manager.get_saved_jobs()
        
        if not saved_jobs:
            label = tk.Label(content, text="No saved jobs", font=self.font_normal, bg=COLOR_BG)
            label.pack(pady=20)
        else:
            # Create scrollable list
            canvas = tk.Canvas(content, bg=COLOR_BG, highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=COLOR_BG)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # List items
            for job_file in saved_jobs:
                btn = tk.Button(
                    scrollable_frame,
                    text=job_file,
                    font=self.font_normal,
                    width=50,
                    bg=COLOR_BUTTON,
                    fg="white",
                    command=lambda jf=job_file: self.load_saved_job(jf)
                )
                btn.pack(pady=5, padx=5, fill=tk.X)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Footer
        footer = tk.Frame(self.root, bg=COLOR_BG)
        footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        btn_back = tk.Button(
            footer,
            text="Back",
            font=BUTTON_FONT,
            bg=COLOR_WARNING,
            fg="white",
            command=self.show_main_menu
        )
        btn_back.pack(side=tk.LEFT, padx=5)
    
    def load_saved_job(self, job_filename):
        """Load a saved job"""
        if self.job_manager.load_job(job_filename):
            self.current_unit = 1
            self.current_item_index = 0
            messagebox.showinfo("Success", f"Loaded job: {job_filename}")
            self.show_active_job()
        else:
            messagebox.showerror("Error", "Could not load job")
    
    def save_job(self):
        """Save current job"""
        self.sync_current_unit_readings()
        if self.job_manager.save_job():
            messagebox.showinfo("Success", "Job saved successfully!")
        else:
            messagebox.showerror("Error", "Could not save job")

# Test
if __name__ == "__main__":
    print("ui.py loaded successfully")
