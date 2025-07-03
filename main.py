import customtkinter as ctk
import tkinter as tk
import datetime
import time
import os
import csv
import tkinter.messagebox as messagebox  # At the top of your file

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
        self.add_button("📈 Customer Sales", self.show_customer_sales)
        self.add_button("➕ Add Sale", self.show_add_sale)
        self.add_button("👤 Add Customer", self.show_add_customer)
        self.add_button("🗖 Daily Sales", self.show_daily_sales)
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
            corner_radius=20,
            width=180,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white"
        )
        btn.pack(pady=10, padx=20)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def get_customers(self):
        customers_path = os.path.join("data", "customers.csv")
        names = []
        if os.path.exists(customers_path):
            with open(customers_path, newline='') as file:
                reader = csv.DictReader(file)
                names = [row["name"] for row in reader]
        return names

    def show_home(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="📊 Dashboard", font=self.header_font).pack(pady=(30, 5))

        card_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        card_container.pack(pady=20, padx=20, fill="both", expand=True)
        card_container.grid_columnconfigure((0, 1, 2), weight=1)

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        sales_today = self.get_sales_for_date(today_str)
        total_today = len(sales_today)
        recent = sales_today[-1] if sales_today else None

        card1 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#DC2626")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card1, text="🛵 Bikes Sold Today", font=self.label_font, text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(card1, text=str(total_today), font=ctk.CTkFont(size=34, weight="bold"), text_color="white").pack()

        card2 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#DC2626")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card2, text="🧑‍💼 Recent Buyer", font=self.label_font, text_color="white").pack(pady=(15, 5))
        buyer_text = f"{recent.get('customer_name', 'N/A')}\n{recent.get('bike_model', '')}" if recent else "No Sales Yet"
        ctk.CTkLabel(card2, text=buyer_text, font=ctk.CTkFont(size=14), text_color="white", justify="center").pack()

        card3 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#DC2626")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card3, text="⏰ Current Time", font=self.label_font, text_color="white").pack(pady=(15, 5))
        self.time_label = ctk.CTkLabel(card3, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color="white")
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

    def show_add_sale(self):
        self.clear_main_content()

        form_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        form_frame.pack(pady=30, padx=40, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="➕ Add New Sale", font=self.header_font, text_color="white").pack(pady=(10, 20))

        names = self.get_customers()
        models = ["CD 70", "CG 125", "CB 150F", "Pridor", "Deluxe"]
        colors = ["Red", "Black", "Blue", "Silver"]

        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack()

        labels = ["Customer Name", "Bike Model", "Chassis Number", "Engine Number", "Color", "Sale Date"]
        self.form_entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(fields_frame, text=label + ":", font=self.label_font, text_color="white").grid(row=i, column=0, sticky="e", padx=10, pady=10)

            if label == "Customer Name":
                entry = ctk.CTkComboBox(fields_frame, width=300, values=names)
            elif label == "Bike Model":
                entry = ctk.CTkComboBox(fields_frame, width=300, values=models)
            elif label == "Color":
                entry = ctk.CTkComboBox(fields_frame, width=300, values=colors)
            else:
                entry = ctk.CTkEntry(fields_frame, width=300)

            entry.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            self.form_entries[label] = entry

        self.form_entries["Sale Date"].insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        submit_btn = ctk.CTkButton(
            form_frame,
            text="Submit",
            font=self.label_font,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=20,
            command=self.submit_sale
        )
        submit_btn.pack(pady=(20, 10))

    def submit_sale(self):
        data = {label: field.get() for label, field in self.form_entries.items()}
        if not data["Customer Name"]:
            print("❌ Customer Name required")
            return

        customers_path = os.path.join("data", "customers.csv")
        customer_id = None
        if os.path.exists(customers_path):
            with open(customers_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["name"] == data["Customer Name"]:
                        customer_id = row["id"]
                        break

        if not customer_id:
            print("❌ Customer not found")
            return

        sales_path = os.path.join("data", "sales.csv")
        file_exists = os.path.isfile(sales_path)
        with open(sales_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["customer_id", "bike_model", "chassis_number", "engine_number", "color", "sale_date"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "customer_id": customer_id,
                "bike_model": data["Bike Model"],
                "chassis_number": data["Chassis Number"],
                "engine_number": data["Engine Number"],
                "color": data["Color"],
                "sale_date": data["Sale Date"]
            })

        print("✅ Sale recorded")

    def show_add_customer(self):
        self.clear_main_content()

        frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        frame.pack(pady=50, padx=50, fill="both", expand=True)

        ctk.CTkLabel(frame, text="➕ Add New Customer", font=self.header_font, text_color="white").pack(pady=(10, 30))

        self.customer_name_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter customer name")
        self.customer_name_entry.pack(pady=10)

        submit_btn = ctk.CTkButton(
            frame,
            text="Save Customer",
            font=self.label_font,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=20,
            command=self.save_new_customer
        )
        submit_btn.pack(pady=20)

    def save_new_customer(self):
        name = self.customer_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Customer name cannot be empty.")
            return

        os.makedirs("data", exist_ok=True)
        customers_path = os.path.join("data", "customers.csv")
        file_exists = os.path.exists(customers_path)
        new_id = 1

        if file_exists:
            with open(customers_path, newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if rows:
                    last = rows[-1]
                    new_id = int(last["id"]) + 1

        with open(customers_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"id": new_id, "name": name})

        messagebox.showinfo("Success", f"Customer '{name}' added successfully.")
        self.show_add_sale()  # Refresh dropdown
        
    def show_customer_sales(self):
        self.clear_main_content()

        ctk.CTkLabel(self.main_content, text="📈 Customer Sales Summary", font=self.header_font).pack(pady=20)

        # Dropdown for customer names
        names = self.get_customers()
        self.selected_customer = ctk.CTkComboBox(self.main_content, values=names, width=300)
        self.selected_customer.pack(pady=10)

        # Duration Buttons (Today, Last 7 Days, This Month)
        btn_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Today", command=self.count_today, width=100, fg_color="#DC2626",
            hover_color="#B91C1C", corner_radius=20).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Last 7 Days", command=self.count_last_7_days, width=100, fg_color="#DC2626",
            hover_color="#B91C1C", corner_radius=20).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="This Month", command=self.count_this_month, width=100, fg_color="#DC2626",
            hover_color="#B91C1C", corner_radius=20).grid(row=0, column=2, padx=5)

        # Manual Date Entry
        self.date_entry = ctk.CTkEntry(self.main_content, width=300, placeholder_text="Enter date (YYYY-MM-DD)")
        self.date_entry.pack(pady=(20, 5))

        ctk.CTkButton(self.main_content, text="Check This Date",fg_color="#DC2626",
            hover_color="#B91C1C", corner_radius=20, command=self.count_on_date).pack()

        self.sales_result_label = ctk.CTkLabel(self.main_content, text="", font=self.label_font)
        self.sales_result_label.pack(pady=10)

    def get_customer_id(self, name):
        customers_path = os.path.join("data", "customers.csv")
        if os.path.exists(customers_path):
            with open(customers_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["name"] == name:
                        return row["id"]
        return None

    def count_sales(self, customer_id, condition):
        count = 0
        sales_path = os.path.join("data", "sales.csv")
        if os.path.exists(sales_path):
            with open(sales_path, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["customer_id"] == customer_id and condition(row["sale_date"]):
                        count += 1
        return count

    def show_sales_result(self, count):
        name = self.selected_customer.get()
        self.sales_result_label.configure(text=f"🛵 {name} bought {count} bike(s) in this period.")

    def count_today(self):
        name = self.selected_customer.get()
        customer_id = self.get_customer_id(name)
        today = datetime.date.today().strftime("%Y-%m-%d")
        count = self.count_sales(customer_id, lambda d: d == today)
        self.show_sales_result(count)

    def count_last_7_days(self):
        name = self.selected_customer.get()
        customer_id = self.get_customer_id(name)
        today = datetime.date.today()
        last_7 = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        count = self.count_sales(customer_id, lambda d: d in last_7)
        self.show_sales_result(count)

    def count_this_month(self):
        name = self.selected_customer.get()
        customer_id = self.get_customer_id(name)
        month_prefix = datetime.date.today().strftime("%Y-%m")
        count = self.count_sales(customer_id, lambda d: d.startswith(month_prefix))
        self.show_sales_result(count)

    def count_on_date(self):
        name = self.selected_customer.get()
        customer_id = self.get_customer_id(name)
        date = self.date_entry.get().strip()
        if not date:
            messagebox.showwarning("Missing Date", "Please enter a date.")
            return
        count = self.count_sales(customer_id, lambda d: d == date)
        self.show_sales_result(count)

        
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
