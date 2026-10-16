import sqlite3
import customtkinter as ctk
from frames.base_frame import BaseSpadeFrame

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
