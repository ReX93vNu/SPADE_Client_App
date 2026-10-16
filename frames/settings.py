import customtkinter as ctk
from frames.base_frame import BaseSpadeFrame

class SettingsFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.auto_sync_enabled = False 
        self._build_main_area()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.top_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("MainMenuFrame")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(self.top_bar, text="Settings", font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000").grid(row=0, column=1, sticky="n", padx=(0, 120)) 

        self.scroll_menu = ctk.CTkScrollableFrame(self.main_area, fg_color="#ffffff", corner_radius=15)
        self.scroll_menu.grid(row=1, column=0, sticky="nsew")
        self.scroll_menu.grid_columnconfigure(0, weight=1)

        self._build_settings_content()

    def _build_settings_content(self):
        # Analysis
        ctk.CTkLabel(self.scroll_menu, text="ANALYSIS PREFERENCES", text_color="#000000", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        
        sync_row = ctk.CTkFrame(self.scroll_menu, fg_color="transparent")
        sync_row.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(sync_row, text="Manual Sync", text_color="#000000", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 15))
        self.btn_manual_sync = ctk.CTkButton(
            sync_row, text="Sync records", font=ctk.CTkFont(size=20), 
            fg_color="#1ba345", hover_color="#148236", width=140, height=45, corner_radius=8, 
            command=self._trigger_manual_sync
        )
        self.btn_manual_sync.pack(side="left", padx=(0, 30))
        
        ctk.CTkLabel(sync_row, text="Auto Sync", text_color="#000000", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 15))
        toggle_frame = ctk.CTkFrame(sync_row, fg_color="transparent")
        toggle_frame.pack(side="left")
        
        self.btn_toggle_off = ctk.CTkButton(
            toggle_frame, text="Off", font=ctk.CTkFont(size=20), width=60, height=45, corner_radius=8, 
            command=lambda: self._set_auto_sync(False)
        )
        self.btn_toggle_off.pack(side="left", padx=2)
        
        self.btn_toggle_on = ctk.CTkButton(
            toggle_frame, text="On", font=ctk.CTkFont(size=20), width=60, height=45, corner_radius=8, 
            command=lambda: self._set_auto_sync(True)
        )
        self.btn_toggle_on.pack(side="left", padx=2)
        
        self._set_auto_sync(self.auto_sync_enabled) 
        ctk.CTkFrame(self.scroll_menu, height=2, fg_color="#e0e0e0").pack(fill="x", padx=20, pady=15)

        # Hardware Calibration
        ctk.CTkLabel(self.scroll_menu, text="HARDWARE CALIBRATION", text_color="#000000", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkLabel(self.scroll_menu, text="Calibrate and configure system sensors", text_color="#555555", font=ctk.CTkFont(size=18)).pack(anchor="w", padx=20, pady=(0, 10))
        
        ctk.CTkButton(
            self.scroll_menu, text="Calibrate Sensors", font=ctk.CTkFont(size=22, weight="bold"), 
            fg_color="#1ba345", hover_color="#148236", height=60, corner_radius=8,
            command=lambda: self.controller.show_frame("CalibrationFrame")
        ).pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkFrame(self.scroll_menu, height=2, fg_color="#e0e0e0").pack(fill="x", padx=20, pady=15)

        # Data Management
        ctk.CTkLabel(self.scroll_menu, text="Data Management", text_color="#000000", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkLabel(self.scroll_menu, text="Manage your stored soil test records", text_color="#555555", font=ctk.CTkFont(size=18)).pack(anchor="w", padx=20, pady=(0, 10))
        
        ctk.CTkButton(
            self.scroll_menu, text="Clear All Data", font=ctk.CTkFont(size=22, weight="bold"), 
            fg_color="#1ba345", hover_color="#148236", height=60, corner_radius=8,
            command=self._show_delete_modal
        ).pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkFrame(self.scroll_menu, height=2, fg_color="#e0e0e0").pack(fill="x", padx=20, pady=15)

        # Data Export
        ctk.CTkLabel(self.scroll_menu, text="Data Export", text_color="#000000", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkLabel(self.scroll_menu, text="Export your records to a CSV file", text_color="#555555", font=ctk.CTkFont(size=18)).pack(anchor="w", padx=20, pady=(0, 10))
        
        self.btn_export_data = ctk.CTkButton(
            self.scroll_menu, text="Export Data (CSV)", font=ctk.CTkFont(size=22, weight="bold"), 
            fg_color="#1ba345", hover_color="#148236", height=60, corner_radius=8,
            command=self._trigger_export_data
        )
        self.btn_export_data.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkFrame(self.scroll_menu, height=2, fg_color="#e0e0e0").pack(fill="x", padx=20, pady=15)

        # App Info
        ctk.CTkLabel(self.scroll_menu, text="APP INFO", text_color="#000000", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=(5, 10))
        self.btn_help = ctk.CTkButton(
            self.scroll_menu, text="Help & Guide                                                                               🔗", 
            font=ctk.CTkFont(size=22), text_color="#000000", fg_color="transparent", hover_color="#f0f0f0",
            height=50, corner_radius=8, anchor="w", command=self._open_help_guide
        )
        self.btn_help.pack(fill="x", padx=10, pady=(0, 30))

    # Modal Logic -------------------------------------------------------
    def _show_delete_modal(self):
        self.modal_blocker = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.modal_blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.modal = ctk.CTkFrame(self.modal_blocker, fg_color="#ffffff", corner_radius=15, border_width=2, border_color="#cccccc")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.modal, text="Delete Past Records", font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000").pack(pady=(30, 15), padx=40)
        ctk.CTkLabel(self.modal, text="Are you sure you want to delete all past\nsoil test records?", font=ctk.CTkFont(size=20), text_color="#333333").pack(pady=(0, 30), padx=40)

        btn_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        btn_frame.pack(pady=(0, 30), padx=30, fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="Cancel", font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#ffffff", text_color="#000000", border_width=2, border_color="#555555",
            height=55, corner_radius=8, hover_color="#f0f0f0", command=self._hide_delete_modal
        ).grid(row=0, column=0, padx=(0, 10), sticky="ew")

        ctk.CTkButton(
            btn_frame, text="Clear Data", font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#ff0000", text_color="#ffffff", hover_color="#cc0000",
            height=55, corner_radius=8, command=self._execute_clear_data
        ).grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def _hide_delete_modal(self):
        if hasattr(self, 'modal_blocker'):
            self.modal_blocker.destroy()

    def _execute_clear_data(self):
        print("Executing Database WIPE...")
        self._hide_delete_modal()

    # Button Functions ----------------------------------------------------------------
    def _trigger_manual_sync(self):
        self.btn_manual_sync.configure(fg_color="#0d5221", text="Syncing...")
        self.after(1500, lambda: self.btn_manual_sync.configure(fg_color="#1ba345", text="Sync records"))
        
    def _trigger_export_data(self):
        self.btn_export_data.configure(fg_color="#0d5221", text="Exporting...")
        self.after(1500, lambda: self.btn_export_data.configure(fg_color="#1ba345", text="Export Data (CSV)"))

    def _set_auto_sync(self, state):
        self.auto_sync_enabled = state
        if state:
            self.btn_toggle_on.configure(fg_color="#1ba345", text_color="#ffffff", border_width=0)
            self.btn_toggle_off.configure(fg_color="#f0f0f0", text_color="#000000", border_width=1, border_color="#cccccc")
        else:
            self.btn_toggle_on.configure(fg_color="#f0f0f0", text_color="#000000", border_width=1, border_color="#cccccc")
            self.btn_toggle_off.configure(fg_color="#1ba345", text_color="#ffffff", border_width=0)

    def _open_help_guide(self):
        print("Opening User Manual PDF or Window...")
