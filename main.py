import customtkinter as ctk
import tkinter as tk
import datetime
import time
import os
import csv

# Setup theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BikeSalesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bike Sales System")
        self.geometry("1000x650")
        self.minsize(800, 600)
        self.configure(bg="#F5F5F5")

        # Fonts
        self.header_font = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        self.label_font = ctk.CTkFont(family="Segoe UI", size=16)
        self.small_font = ctk.CTkFont(family="Segoe UI", size=13)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=15)
        self.sidebar.pack(side="left", fill="y", padx=20, pady=20)

        # Main Content
        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Sidebar Title
        ctk.CTkLabel(self.sidebar, text="🚲 Menu", font=self.header_font).pack(pady=(30, 20))

        # Sidebar Buttons
        self.add_button("🏠 Home", self.show_home)
        self.add_button("➕ Add Sale", self.show_add_sale)
        self.add_button("📆 Daily Sales", self.show_daily_sales)
        self.add_button("📋 All Sales", self.show_all_sales)
        self.add_button("📊 Summary", self.show_summary)
        self.add_button("❌ Exit", self.quit)

        self.show_home()

    def add_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            font=self.label_font,
            corner_radius=10,
            width=180,
            height=40,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white"
        )
        btn.pack(pady=10, padx=20)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def show_home(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="📊 Dashboard", font=self.header_font).pack(pady=(30, 5))

        # 🟦 Card Container Frame with equal spacing as sidebar
        card_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        card_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Configure grid responsiveness
        card_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Fetch today's data
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        sales_today = self.get_sales_for_date(today_str)
        total_today = len(sales_today)
        recent = sales_today[-1] if sales_today else None

        # 🟩 Total Sales Card
        card1 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#1E3A8A")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card1, text="🛵 Bikes Sold Today", font=self.label_font, text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(card1, text=str(total_today), font=ctk.CTkFont(size=34, weight="bold"), text_color="#93C5FD").pack()

        # 🟨 Recent Buyer Card
        card2 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#78350F")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card2, text="🧑‍💼 Recent Buyer", font=self.label_font, text_color="white").pack(pady=(15, 5))
        if recent:
            buyer_text = f"{recent.get('customer_name', 'N/A')}\n{recent.get('bike_model', '')}"
        else:
            buyer_text = "No Sales Yet"
        ctk.CTkLabel(card2, text=buyer_text, font=ctk.CTkFont(size=14), text_color="#FDE68A", justify="center").pack()

        # 🕒 Time Card
        card3 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#4C1D95")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card3, text="⏰ Current Time", font=self.label_font, text_color="white").pack(pady=(15, 5))
        self.time_label = ctk.CTkLabel(card3, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color="#DDD6FE")
        self.time_label.pack()
        self.update_time()


    def update_time(self):
        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            current_time = time.strftime("%I:%M:%S %p")
            self.time_label.configure(text=f"{current_time}")
            self.after(1000, self.update_time)

    def get_sales_for_date(self, date_str):
        sales = []
        sales_path = os.path.join("data", "sales.csv")
        if os.path.exists(sales_path):
            with open(sales_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["sale_date"] == date_str:
                        row["customer_name"] = self.get_customer_name(row["customer_id"])
                        sales.append(row)
        return sales

    def get_customer_name(self, customer_id):
        customers_path = os.path.join("data", "customers.csv")
        if os.path.exists(customers_path):
            with open(customers_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["id"] == customer_id:
                        return row["name"]
        return "Unknown"

    # Placeholder pages
    def show_add_sale(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="Add Sale Form", font=self.header_font).pack(pady=20)

    def show_daily_sales(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="Daily Sales View", font=self.header_font).pack(pady=20)

    def show_all_sales(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="All Sales Records", font=self.header_font).pack(pady=20)

    def show_summary(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="Sales Summary", font=self.header_font).pack(pady=20)


if __name__ == "__main__":
    app = BikeSalesApp()
    app.mainloop()
