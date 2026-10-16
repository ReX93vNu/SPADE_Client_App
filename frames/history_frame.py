import customtkinter as ctk
from frames.base_frame import BaseSpadeFrame

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
