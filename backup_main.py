import customtkinter as ctk
from PIL import Image
import os
import sqlite3
import math 

class SpadeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SPADE OS - Touch Interface")
        self.geometry("800x480")
        self.resizable(False, False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._load_shared_images()

        self.frames = {}
        # CalibrationFrame to the initialization loop
        for F in (MainMenuFrame, SettingsFrame, StartFrame, HistoryFrame, CalibrationFrame, PhCalibrationFrame, NCalibrationFrame, KCalibrationFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuFrame")

    def _load_shared_images(self):
        def load_img(filename, size):
            path = os.path.join("assets", filename)
            try:
                return ctk.CTkImage(light_image=Image.open(path), size=size)
            except FileNotFoundError:
                return None

        self.img_leaf = load_img("logo.png", size=(30, 30))
        self.img_battery = load_img("battery_icon.png", size=(35, 20))
        self.img_start = load_img("play_btn.png", size=(60, 60))
        self.img_history = load_img("history_btn.png", size=(60, 60))
        self.img_settings = load_img("settings_btn.png", size=(60, 60))
        self.img_power = load_img("power_btn.png", size=(60, 60))

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class BaseSpadeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#d9d9d9", corner_radius=0)
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._build_sidebar()
        
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=70, corner_radius=0, fg_color="#3a3c42")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False) 
        
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(2, weight=1) 
        
        self.leaf_label = ctk.CTkLabel(
            self.sidebar, text="🍃" if not self.controller.img_leaf else "", 
            image=self.controller.img_leaf, font=ctk.CTkFont(size=45), text_color="#1ba345"
        )
        self.leaf_label.grid(row=0, column=0, pady=(20, 5))

        self.logo_text = ctk.CTkLabel(self.sidebar, text="SPADE", font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffffff")
        self.logo_text.grid(row=1, column=0)

        self.battery_label = ctk.CTkLabel(
            self.sidebar, text="🔋" if not self.controller.img_battery else "", 
            image=self.controller.img_battery, font=ctk.CTkFont(size=35), text_color="#ffffff"
        )
        self.battery_label.grid(row=3, column=0, pady=(0, 20), sticky="s")


class MainMenuFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build_grid_menu()

    def _build_grid_menu(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure((0, 1), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_start = self._create_menu_button(self.controller.img_start, "Start", 0, 0, lambda: self.controller.show_frame("StartFrame"))
        self.btn_history = self._create_menu_button(self.controller.img_history, "History", 0, 1, lambda: self.controller.show_frame("HistoryFrame"))
        self.btn_settings = self._create_menu_button(self.controller.img_settings, "Settings", 1, 0, lambda: self.controller.show_frame("SettingsFrame"))
        self.btn_power = self._create_menu_button(self.controller.img_power, "Power", 1, 1, self.controller.quit)

    def _create_menu_button(self, ctk_image, text, row, col, command=None):
        btn = ctk.CTkButton(
            self.main_frame, image=ctk_image, text=f" {text}", font=ctk.CTkFont(size=34, weight="bold"),
            fg_color="#ffffff", text_color="#2b3036", hover_color="#f0f0f0", corner_radius=12, anchor="center", command=command
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        return btn


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

    # Button Functions ----------------------------------------------------------
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


class StartFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build_main_area()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("MainMenuFrame")
        ).pack(side="left")

        self.content = ctk.CTkFrame(self.main_area, fg_color="#ffffff", corner_radius=15)
        self.content.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        ctk.CTkLabel(self.content, text="Sensor Testing Interface Goes Here", font=ctk.CTkFont(size=24, weight="bold"), text_color="#cccccc").place(relx=0.5, rely=0.5, anchor="center")


class HistoryFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build_main_area()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("MainMenuFrame")
        ).pack(side="left")

        self.content = ctk.CTkFrame(self.main_area, fg_color="#ffffff", corner_radius=15)
        self.content.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        ctk.CTkLabel(self.content, text="Historical Data Records Go Here", font=ctk.CTkFont(size=24, weight="bold"), text_color="#cccccc").place(relx=0.5, rely=0.5, anchor="center")


# Calibration ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class CalibrationFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build_main_area()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Top Bar
        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("SettingsFrame")
        ).pack(side="left")

        # 2x2 Grid Content Area
        self.content = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", pady=(0, 0))
        
        self.content.grid_rowconfigure((0, 1), weight=1)
        self.content.grid_columnconfigure((0, 1), weight=1)

        # Calibration Buttons
        self.btn_ph = self._create_calib_button(
            "Calibrate\npH Sensor", 0, 0, 
            command=lambda: self.controller.show_frame("PhCalibrationFrame")
        )
        self.btn_n = self._create_calib_button(
            "Calibrate\nNitrogen (N)", 0, 1,
            command=lambda: self.controller.show_frame("NCalibrationFrame")
        )
        self.btn_k = self._create_calib_button(
            "Calibrate\nPotassium (K)", 1, 0,
            command=lambda: self.controller.show_frame("KCalibrationFrame")
        )
        self.btn_p = self._create_calib_button("Calibrate\nPhosphorus (P)", 1, 1)

    def _create_calib_button(self, text, row, col, command=None):
        btn = ctk.CTkButton(
            self.content, text=text, font=ctk.CTkFont(size=28, weight="bold"),
            fg_color="#ffffff", text_color="#2b3036", hover_color="#f0f0f0",
            corner_radius=15, border_width=2, border_color="#cccccc",
            command=command
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
        return btn


class PhCalibrationFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.v7 = 0.0
        self.v4 = 0.0
        self.current_step = 1
        
        self._init_hardware()
        self._build_main_area()

    def _init_hardware(self):
        """Initializes the ADS1115 using I2C if running on the Raspberry Pi."""
        try:
            import board
            import busio
            import adafruit_ads1x15.ads1115 as ADS
            from adafruit_ads1x15.analog_in import AnalogIn

            # Initializes I2C using SDA (Pin 3) and SCL (Pin 5)
            self.i2c = busio.I2C(board.SCL, board.SDA) 
            self.ads = ADS.ADS1115(self.i2c)
            
            # Connects to the voltage divider junction on A1
            self.chan = AnalogIn(self.ads, ADS.P1) 
            
            self.hardware_active = True
            print("ADS1115 hardware connected successfully on A1.")
        except (NotImplementedError, ImportError, ValueError):
            self.hardware_active = False
            print("Hardware not detected. Running in UI simulation mode.")

    def tkraise(self, *args, **kwargs):
        """Overrides tkraise to reset the calibration flow every time the screen is opened."""
        super().tkraise(*args, **kwargs)
        self.current_step = 1
        self.v7 = 0.0
        self.v4 = 0.0
        self._render_step()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("CalibrationFrame")
        ).pack(side="left")

        self.content = ctk.CTkFrame(self.main_area, fg_color="#ffffff", corner_radius=15)
        self.content.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

    def _render_step(self):
        """Clears the content frame and renders the UI for the current step."""
        for widget in self.content.winfo_children():
            widget.destroy()

        if self.current_step == 1:
            title = "Step 1: pH 7.0 Calibration"
            instructions = "Place the probe into the pH 7.0 buffer solution.\nWait 60 seconds for the reading to stabilize,\nthen press Continue."
            btn_text = "Record pH 7 & Continue"
            action = self._record_ph7

        elif self.current_step == 2:
            title = "Step 2: pH 4.0 Calibration"
            instructions = "Place the probe into the pH 4.0 buffer solution.\nWait 60 seconds for the reading to stabilize,\nthen press Continue."
            btn_text = "Record pH 4 & Finish"
            action = self._record_ph4

        elif self.current_step == 3:
            title = "Calibration Complete"
            slope = (self.v4 - self.v7) / (4.0 - 7.0)
            intercept = self.v7 - (slope * 7.0)
            
            instructions = f"Hardware configured successfully.\n\nRecorded pH 7: {self.v7:.3f}V\nRecorded pH 4: {self.v4:.3f}V\n\nCalculated Slope: {slope:.4f}\nCalculated Intercept: {intercept:.4f}"
            btn_text = "Return to Menu"
            action = lambda: self.controller.show_frame("CalibrationFrame")
            
            self._save_calibration_profile(self.v7, self.v4, slope, intercept)

        ctk.CTkLabel(
            self.content, text=title, font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000"
        ).pack(pady=(40, 20))

        ctk.CTkLabel(
            self.content, text=instructions, font=ctk.CTkFont(size=22), text_color="#333333"
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            self.content, text=btn_text, width=280, height=50, font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", corner_radius=8, command=action
        ).pack()

    def _get_live_voltage(self):
        """Reads the voltage from A1 and reverses the 5.1k/2k voltage divider."""
        multiplier = 3.55 
        
        if self.hardware_active:
            raw_adc_voltage = self.chan.voltage
        else:
            import random
            if self.current_step == 1:
                raw_adc_voltage = (2.50 / multiplier) + random.uniform(-0.01, 0.01)
            else:
                raw_adc_voltage = (3.00 / multiplier) + random.uniform(-0.01, 0.01)
        
        adjusted_voltage = raw_adc_voltage * multiplier
        
        # Terminal monitoring for hardware response
        print(f"[DEBUG] Step {self.current_step} | Raw ADC (A1): {raw_adc_voltage:.4f}V  -->  Adjusted (True): {adjusted_voltage:.4f}V")
        
        return adjusted_voltage

    def _record_ph7(self):
        self.v7 = self._get_live_voltage()
        self.current_step = 2
        self._render_step()

    def _record_ph4(self):
        self.v4 = self._get_live_voltage()
        self.current_step = 3
        self._render_step()

    def _save_calibration_profile(self, v7, v4, slope, intercept):
        """Commits the calibration math to the SQLite database."""
        conn = sqlite3.connect("spade_system.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CalibrationProfile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_type TEXT,
                ph7_voltage REAL,
                ph4_voltage REAL,
                slope REAL,
                intercept REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            INSERT INTO CalibrationProfile (sensor_type, ph7_voltage, ph4_voltage, slope, intercept)
            VALUES (?, ?, ?, ?, ?)
        ''', ("pH-4502C", v7, v4, slope, intercept))
        
        conn.commit()
        conn.close()


class NCalibrationFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.v10 = 0.0
        self.v100 = 0.0
        self.current_step = 1
        
        self._init_hardware()
        self._build_main_area()

    def _init_hardware(self):
        """Initializes the ADS1115 using I2C if running on the Raspberry Pi."""
        try:
            import board
            import busio
            import adafruit_ads1x15.ads1115 as ADS
            from adafruit_ads1x15.analog_in import AnalogIn

            self.i2c = busio.I2C(board.SCL, board.SDA) 
            self.ads = ADS.ADS1115(self.i2c)
            self.chan = AnalogIn(self.ads, ADS.P1) 
            
            self.hardware_active = True
            print("ADS1115 hardware connected successfully on A1 for Nitrate ISE.")
        except (NotImplementedError, ImportError, ValueError):
            self.hardware_active = False
            print("Hardware not detected. Running in UI simulation mode.")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.current_step = 1
        self.v10 = 0.0
        self.v100 = 0.0
        self._render_step()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("CalibrationFrame")
        ).pack(side="left")

        self.content = ctk.CTkFrame(self.main_area, fg_color="#ffffff", corner_radius=15)
        self.content.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

    def _render_step(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        pad_bottom = 40

        if self.current_step == 1:
            title = "Step 1: 10 ppm Nitrate Standard"
            instructions = "Place the probe into the 10 ppm Nitrate standard (with ISA).\nWait 60 seconds for the reading to stabilize,\nthen press Continue."
            btn_text = "Record 10 ppm & Continue"
            action = self._record_v10

        elif self.current_step == 2:
            title = "Step 2: 100 ppm Nitrate Standard"
            instructions = "Rinse probe in DI water, then place in the 100 ppm Nitrate standard.\nWait 60 seconds for the reading to stabilize,\nthen press Continue."
            btn_text = "Record 100 ppm & Finish"
            action = self._record_v100

        elif self.current_step == 3:
            pad_bottom = 15
            title = "Calibration Complete"
            
            # Nernst Equation Math (Decade Slope)
            slope = self.v100 - self.v10
            intercept = self.v10 - slope
            
            instructions = f"Hardware configured successfully.\n\nRecorded 10 ppm: {self.v10:.3f}V\nRecorded 100 ppm: {self.v100:.3f}V\n\nCalculated Decade Slope: {slope:.4f}V\nCalculated Intercept: {intercept:.4f}V"
            btn_text = "Return to Menu"
            action = lambda: self.controller.show_frame("CalibrationFrame")
            
            self._save_calibration_profile(self.v10, self.v100, slope, intercept)

        ctk.CTkLabel(
            self.content, text=title, font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000"
        ).pack(pady=(40, 20))

        ctk.CTkLabel(
            self.content, text=instructions, font=ctk.CTkFont(size=22), text_color="#333333"
        ).pack(pady=(0, pad_bottom))

        ctk.CTkButton(
            self.content, text=btn_text, width=280, height=60, font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", corner_radius=8, command=action
        ).pack()

    def _get_live_voltage(self):
        multiplier = 3.55 
        
        if self.hardware_active:
            raw_adc_voltage = self.chan.voltage
        else:
            import random
            if self.current_step == 1:
                raw_adc_voltage = (2.20 / multiplier) + random.uniform(-0.01, 0.01)
            else:
                raw_adc_voltage = (2.15 / multiplier) + random.uniform(-0.01, 0.01)
        
        adjusted_voltage = raw_adc_voltage * multiplier
        print(f"[DEBUG - Nitrate] Step {self.current_step} | Raw ADC (A1): {raw_adc_voltage:.4f}V  -->  Adjusted (True): {adjusted_voltage:.4f}V")
        return adjusted_voltage

    def _record_v10(self):
        self.v10 = self._get_live_voltage()
        self.current_step = 2
        self._render_step()

    def _record_v100(self):
        self.v100 = self._get_live_voltage()
        self.current_step = 3
        self._render_step()

    def _save_calibration_profile(self, v10, v100, slope, intercept):
        conn = sqlite3.connect("spade_system.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CalibrationProfile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_type TEXT,
                ph7_voltage REAL,
                ph4_voltage REAL,
                slope REAL,
                intercept REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Storing the 10ppm and 100ppm voltages in the existing ph7/ph4 columns to reuse the table structure (both are just high and low baselines (i think))
        cursor.execute('''
            INSERT INTO CalibrationProfile (sensor_type, ph7_voltage, ph4_voltage, slope, intercept)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Nitrate-ISE", v10, v100, slope, intercept))
        
        conn.commit()
        conn.close()


class KCalibrationFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.v10 = 0.0
        self.v100 = 0.0
        self.current_step = 1
        
        self._init_hardware()
        self._build_main_area()

    def _init_hardware(self):
        try:
            import board
            import busio
            import adafruit_ads1x15.ads1115 as ADS
            from adafruit_ads1x15.analog_in import AnalogIn

            self.i2c = busio.I2C(board.SCL, board.SDA) 
            self.ads = ADS.ADS1115(self.i2c)
            self.chan = AnalogIn(self.ads, ADS.P1) 
            
            self.hardware_active = True
            print("ADS1115 hardware connected successfully on A1 for Potassium ISE.")
        except (NotImplementedError, ImportError, ValueError):
            self.hardware_active = False
            print("Hardware not detected. Running in UI simulation mode.")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.current_step = 1
        self.v10 = 0.0
        self.v100 = 0.0
        self._render_step()

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(
            self.top_bar, text="← Back", width=120, height=50, font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", command=lambda: self.controller.show_frame("CalibrationFrame")
        ).pack(side="left")

        self.content = ctk.CTkFrame(self.main_area, fg_color="#ffffff", corner_radius=15)
        self.content.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

    def _render_step(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        pad_bottom = 40

        if self.current_step == 1:
            title = "Step 1: 10 ppm Potassium Standard"
            instructions = "Place the probe into the 10 ppm Potassium standard (with ISA).\nWait 60 seconds for the reading to stabilize,\nthen press Continue."
            btn_text = "Record 10 ppm & Continue"
            action = self._record_v10

        elif self.current_step == 2:
            title = "Step 2: 100 ppm Potassium Standard"
            instructions = "Rinse probe in DI water, then place in the 100 ppm Potassium standard.\nWait 60 seconds for the reading to stabilize,\nthen press Continue."
            btn_text = "Record 100 ppm & Finish"
            action = self._record_v100

        elif self.current_step == 3:
            pad_bottom = 15
            title = "Calibration Complete"
            
            slope = self.v100 - self.v10
            intercept = self.v10 - slope
            
            instructions = f"Hardware configured successfully.\n\nRecorded 10 ppm: {self.v10:.3f}V\nRecorded 100 ppm: {self.v100:.3f}V\n\nCalculated Decade Slope: {slope:.4f}V\nCalculated Intercept: {intercept:.4f}V"
            btn_text = "Return to Menu"
            action = lambda: self.controller.show_frame("CalibrationFrame")
            
            self._save_calibration_profile(self.v10, self.v100, slope, intercept)

        ctk.CTkLabel(
            self.content, text=title, font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000"
        ).pack(pady=(40, 20))

        ctk.CTkLabel(
            self.content, text=instructions, font=ctk.CTkFont(size=22), text_color="#333333"
        ).pack(pady=(0, pad_bottom))

        ctk.CTkButton(
            self.content, text=btn_text, width=280, height=60, font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", corner_radius=8, command=action
        ).pack()

    def _get_live_voltage(self):
        multiplier = 3.55 
        
        if self.hardware_active:
            raw_adc_voltage = self.chan.voltage
        else:
            import random
            if self.current_step == 1:
                raw_adc_voltage = (2.20 / multiplier) + random.uniform(-0.01, 0.01)
            else:
                raw_adc_voltage = (2.15 / multiplier) + random.uniform(-0.01, 0.01)
        
        adjusted_voltage = raw_adc_voltage * multiplier
        print(f"[DEBUG - Potassium] Step {self.current_step} | Raw ADC (A1): {raw_adc_voltage:.4f}V  -->  Adjusted (True): {adjusted_voltage:.4f}V")
        return adjusted_voltage

    def _record_v10(self):
        self.v10 = self._get_live_voltage()
        self.current_step = 2
        self._render_step()

    def _record_v100(self):
        self.v100 = self._get_live_voltage()
        self.current_step = 3
        self._render_step()

    def _save_calibration_profile(self, v10, v100, slope, intercept):
        conn = sqlite3.connect("spade_system.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CalibrationProfile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_type TEXT,
                ph7_voltage REAL,
                ph4_voltage REAL,
                slope REAL,
                intercept REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            INSERT INTO CalibrationProfile (sensor_type, ph7_voltage, ph4_voltage, slope, intercept)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Potassium-ISE", v10, v100, slope, intercept))
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = SpadeApp()
    app.mainloop()


