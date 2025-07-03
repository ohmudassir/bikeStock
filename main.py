import customtkinter as ctk
import tkinter as tk
import datetime
import time
import os
import csv

# Setup theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class BikeSalesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bike Sales System")
        self.geometry("1000x650")  # Better default resolution
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

        # Add Buttons
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
            fg_color="#3B82F6",  # Tailwind blue-500
            hover_color="#2563EB",  # Tailwind blue-600
            text_color="white"
        )
        btn.pack(pady=10, padx=20)  # Horizontal padding to keep button away from edges

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="Dashboard", font=("Arial", 22)).pack(pady=10)

        # Time Label
        self.time_label = ctk.CTkLabel(self.main_content, text="", font=("Arial", 16))
        self.time_label.pack(pady=5)
        self.update_time()

        # Load today's sales data
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        sales_today = self.get_sales_for_date(today_str)

        total_today = len(sales_today)
        ctk.CTkLabel(self.main_content, text=f"Total Bikes Sold Today: {total_today}", font=("Arial", 16)).pack(pady=5)

        if sales_today:
            recent = sales_today[-1]
            buyer = recent.get("customer_name", "Unknown")
            model = recent.get("bike_model", "Unknown")
            ctk.CTkLabel(self.main_content, text=f"Recent Buyer: {buyer} - {model}", font=("Arial", 14)).pack(pady=5)
        else:
            ctk.CTkLabel(self.main_content, text="No sales yet today.", font=("Arial", 14)).pack(pady=5)
    def update_time(self):
        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            current_time = time.strftime("%I:%M:%S %p")
            self.time_label.configure(text=f"Current Time: {current_time}")
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
        ctk.CTkLabel(self.main_content, text="Add Sale Form", font=("Arial", 18)).pack(pady=20)

    def show_daily_sales(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="Daily Sales View", font=("Arial", 18)).pack(pady=20)

    def show_all_sales(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="All Sales Records", font=("Arial", 18)).pack(pady=20)

    def show_summary(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="Sales Summary", font=("Arial", 18)).pack(pady=20)


if __name__ == "__main__":
    app = BikeSalesApp()
    app.mainloop()
