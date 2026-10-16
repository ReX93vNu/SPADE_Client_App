import sqlite3
import customtkinter as ctk
import time
from frames.base_frame import BaseSpadeFrame

class PCalibrationFrame(BaseSpadeFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.freq_blank = 0.0
        self.freq_standard = 0.0
        self.current_step = 1
        
        # Mapped exactly to your physical board diagram[cite: 9]
        self.S0_PIN = 7
        self.S1_PIN = 29
        self.S2_PIN = 31
        self.S3_PIN = 32
        self.OUT_PIN = 33
        self.LED_PIN = 36
        
        self._init_hardware()
        self._build_main_area()

    def _init_hardware(self):
        """Initializes the TCS3200 using physical board pin numbers."""
        try:
            import RPi.GPIO as GPIO
            # Use BOARD mode to match physical pins 7, 29, 31, 32, 33, and 36
            GPIO.setmode(GPIO.BOARD)
            
            # Setup inputs and outputs
            GPIO.setup(self.OUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.S0_PIN, GPIO.OUT)
            GPIO.setup(self.S1_PIN, GPIO.OUT)
            GPIO.setup(self.S2_PIN, GPIO.OUT)
            GPIO.setup(self.S3_PIN, GPIO.OUT)
            GPIO.setup(self.LED_PIN, GPIO.OUT)
            
            # Turn on the sensor's built-in white LEDs
            GPIO.output(self.LED_PIN, GPIO.HIGH)
            
            # Set Frequency Scaling to 20% (S0 HIGH, S1 LOW) for stable Pi reading
            GPIO.output(self.S0_PIN, GPIO.HIGH)
            GPIO.output(self.S1_PIN, GPIO.LOW)
            
            # Set to Red Filter (S2 LOW, S3 LOW) to measure absorption of the blue P-solution
            GPIO.output(self.S2_PIN, GPIO.LOW)
            GPIO.output(self.S3_PIN, GPIO.LOW)
            
            self.hardware_active = True
            print("TCS3200 hardware connected successfully on physical pins.")
        except (NotImplementedError, ImportError, RuntimeError):
            self.hardware_active = False
            print("Hardware not detected. Running in UI simulation mode.")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.current_step = 1
        self.freq_blank = 0.0
        self.freq_standard = 0.0
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
            title = "Step 1: Blank Calibration"
            instructions = "Insert the blank cuvette (distilled water) into the sensor.\nWait for the reading to stabilize,\nthen press Continue."
            btn_text = "Record Blank & Continue"
            action = self._record_blank

        elif self.current_step == 2:
            title = "Step 2: Phosphorus Standard"
            instructions = "Insert the known Phosphorus standard cuvette (blue solution).\nWait for the reading to stabilize,\nthen press Continue."
            btn_text = "Record Standard & Finish"
            action = self._record_standard

        elif self.current_step == 3:
            pad_bottom = 15
            title = "Calibration Complete"
            
            slope = self.freq_blank - self.freq_standard
            intercept = self.freq_standard
            
            instructions = f"Hardware configured successfully.\n\nRecorded Blank Frequency: {self.freq_blank:.0f} Hz\nRecorded Standard Frequency: {self.freq_standard:.0f} Hz\n\nCalculated Slope: {slope:.0f}\nCalculated Intercept: {intercept:.0f}"
            btn_text = "Return to Menu"
            action = lambda: self.controller.show_frame("CalibrationFrame")
            
            self._save_calibration_profile(self.freq_blank, self.freq_standard, slope, intercept)

        ctk.CTkLabel(self.content, text=title, font=ctk.CTkFont(size=28, weight="bold"), text_color="#000000").pack(pady=(40, 20))
        ctk.CTkLabel(self.content, text=instructions, font=ctk.CTkFont(size=22), text_color="#333333").pack(pady=(0, pad_bottom))
        
        ctk.CTkButton(
            self.content, text=btn_text, width=280, height=60, font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#1ba345", hover_color="#148236", corner_radius=8, command=action
        ).pack()

    def _get_live_frequency(self):
        if self.hardware_active:
            import RPi.GPIO as GPIO
            count = 0
            start_time = time.time()
            # Basic frequency counting logic over 0.5 seconds
            while time.time() - start_time < 0.5:
                GPIO.wait_for_edge(self.OUT_PIN, GPIO.FALLING, timeout=500)
                count += 1
            freq = count * 2  # Multiply by 2 to get Hz (cycles per second)
            return freq
        else:
            import random
            if self.current_step == 1:
                freq = 15000 + random.uniform(-100, 100)
            else:
                freq = 4000 + random.uniform(-100, 100)
            
        print(f"[DEBUG - Phosphorus TCS3200] Step {self.current_step} | Recorded Frequency: {freq:.0f} Hz")
        return freq

    def _record_blank(self):
        self.freq_blank = self._get_live_frequency()
        self.current_step = 2
        self._render_step()

    def _record_standard(self):
        self.freq_standard = self._get_live_frequency()
        self.current_step = 3
        self._render_step()

    def _save_calibration_profile(self, freq_blank, freq_standard, slope, intercept):
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
        ''', ("Phosphorus-TCS3200", freq_blank, freq_standard, slope, intercept))
        
        conn.commit()
        conn.close()