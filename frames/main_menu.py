import customtkinter as ctk
from frames.base_frame import BaseSpadeFrame

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