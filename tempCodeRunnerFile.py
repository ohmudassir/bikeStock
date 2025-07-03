        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="📊 Dashboard", font=self.header_font, anchor="w").pack(side="left")
