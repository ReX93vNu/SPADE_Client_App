import customtkinter as ctk
from frames.base_frame import BaseSpadeFrame

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

        # Calibration sensor buttons
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
        self.btn_p = self._create_calib_button(
            "Calibrate\nPhosphorus (P)", 1, 1,
            command=lambda: self.controller.show_frame("PCalibrationFrame")
        )

    def _create_calib_button(self, text, row, col, command=None):
        btn = ctk.CTkButton(
            self.content, text=text, font=ctk.CTkFont(size=28, weight="bold"),
            fg_color="#ffffff", text_color="#2b3036", hover_color="#f0f0f0",
            corner_radius=15, border_width=2, border_color="#cccccc",
            command=command
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
        return btn