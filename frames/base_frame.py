import customtkinter as ctk

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