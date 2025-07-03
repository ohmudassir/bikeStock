import customtkinter as ctk
import tkinter as tk
import datetime
import time
import os
import csv
import tkinter.messagebox as messagebox
from CTkTable import CTkTable

# Setup theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BikeSalesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bike Sales System")
        self.state("zoomed")
        self.configure(bg="#F5F5F5")

        self.reset_sales_monthly()  # Clear sales if a new month has started

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

        ctk.CTkLabel(self.sidebar, text="🚲 Menu", font=self.header_font).pack(pady=(30, 20))

        self.add_button("🏠 Home", self.show_home)
        self.add_button("📈 Customer Sales", self.show_customer_sales)
        self.add_button("➕ Add Sale", self.show_add_sale)
        self.add_button("👤 Add Customer", self.show_add_customer)
        self.add_button("📊 Summary", self.show_summary)
        self.add_button("❌ Exit", self.quit)

        self.show_home()

    def reset_sales_monthly(self):
        os.makedirs("data", exist_ok=True)
        now = datetime.datetime.now()
        current_month = now.strftime("%Y-%m")
        flag_file = os.path.join("data", "monthly_sales.csv")
        sales_file = os.path.join("data", "sales.csv")

        # Read the last recorded month
        if os.path.exists(flag_file):
            with open(flag_file, "r") as f:
                last_month = f.read().strip()
        else:
            last_month = ""

        # If month changed, archive and reset sales file
        if last_month != current_month:
            if os.path.exists(sales_file):
                archived_file = os.path.join("data", f"sales_{last_month}.csv")
                os.rename(sales_file, archived_file)  # Move old sales to new file

            with open(flag_file, "w") as f:
                f.write(current_month)


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
        card_container.pack(pady=(10, 10), padx=20, fill="both", expand=True)
        card_container.grid_columnconfigure((0, 1, 2), weight=1)

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        sales_today = self.get_sales_for_date(today_str)

        total_bikes = 0
        model_counts = {}
        recent = sales_today[-1] if sales_today else None

        for sale in sales_today:
            model = sale["bike_model"]
            qty = int(sale.get("quantity", 1))
            total_bikes += qty
            model_counts[model] = model_counts.get(model, 0) + qty

        # Top Summary Cards
        card1 = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color="#DC2626")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card1, text="🛵 Bikes Sold Today", font=self.label_font, text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(card1, text=str(total_bikes), font=ctk.CTkFont(size=34, weight="bold"), text_color="white").pack()

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

        # Red gradient shades for model cards
        red_shades = ["#7F1D1D", "#991B1B", "#B91C1C", "#DC2626", "#EF4444", "#F87171"]

        # Model-specific cards
        if model_counts:
            row = 1
            col = 0
            for i, (model, qty) in enumerate(model_counts.items()):
                color = red_shades[i % len(red_shades)]
                card = ctk.CTkFrame(card_container, corner_radius=12, height=160, fg_color=color)
                card.grid(row=row, column=col, padx=10, pady=(10, 10), sticky="nsew")
                ctk.CTkLabel(card, text=model, font=self.label_font, text_color="white").pack(pady=(15, 5))
                ctk.CTkLabel(card, text=f"{qty} Sold", font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack()

                col += 1
                if col > 2:
                    row += 1
                    col = 0


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
        self.form_entries = {}

        # Customer name
        customer_label = ctk.CTkLabel(form_frame, text="Customer Name:", font=self.label_font, text_color="white")
        customer_label.pack(pady=5)
        customer_combo = ctk.CTkComboBox(form_frame, width=300, values=names)
        customer_combo.pack(pady=5)
        self.form_entries["Customer Name"] = customer_combo

        # Sale date
        date_label = ctk.CTkLabel(form_frame, text="Sale Date:", font=self.label_font, text_color="white")
        date_label.pack(pady=5)
        sale_date = ctk.CTkEntry(form_frame, width=300)
        sale_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        sale_date.pack(pady=5)
        self.form_entries["Sale Date"] = sale_date

        # Section for multiple bikes
        self.bike_entries = []
        bike_models = ["CD 70", "CG 125", "CD 70 Dream", "Pridor", "CG 125S", "CG 125S GOLD"]
        bike_colors = ["Red", "Black", "Blue", "Silver"]

        self.bikes_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.bikes_container.pack(pady=10)

        def add_bike_row():
            row = ctk.CTkFrame(self.bikes_container, fg_color="transparent")
            row.pack(pady=5)

            model = ctk.CTkComboBox(row, width=120, values=bike_models)
            model.pack(side="left", padx=5)
            color = ctk.CTkComboBox(row, width=100, values=bike_colors)
            color.pack(side="left", padx=5)
            qty = ctk.CTkEntry(row, width=80, placeholder_text="Qty")
            qty.pack(side="left", padx=5)

            self.bike_entries.append({"model": model, "color": color, "qty": qty})

        add_bike_row()  # Add the first row

        ctk.CTkButton(form_frame, text="➕ Add Another Bike", command=add_bike_row, fg_color="#DC2626", hover_color="#B91C1C").pack(pady=10)

        submit_btn = ctk.CTkButton(
            form_frame,
            text="Submit Sale",
            font=self.label_font,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=20,
            command=self.submit_sale
        )
        submit_btn.pack(pady=(20, 10))

    def submit_sale(self):
        customer_name = self.form_entries["Customer Name"].get()
        sale_date = self.form_entries["Sale Date"].get().strip()

        if not customer_name or not sale_date:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Find customer ID
        customers_path = os.path.join("data", "customers.csv")
        customer_id = None
        if os.path.exists(customers_path):
            with open(customers_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["name"] == customer_name:
                        customer_id = row["id"]
                        break

        if not customer_id:
            messagebox.showerror("Error", "Customer not found.")
            return

        # Prepare sales data
        sales_path = os.path.join("data", "sales.csv")
        file_exists = os.path.isfile(sales_path)
        os.makedirs("data", exist_ok=True)

        with open(sales_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["customer_id", "bike_model", "color", "quantity", "sale_date"])
            if not file_exists:
                writer.writeheader()

            for entry in self.bike_entries:
                model = entry["model"].get()
                color = entry["color"].get()
                qty = entry["qty"].get()

                if not model or not color or not qty.isdigit():
                    continue

                writer.writerow({
                    "customer_id": customer_id,
                    "bike_model": model,
                    "color": color,
                    "quantity": qty,
                    "sale_date": sale_date
                })

        messagebox.showinfo("Success", "✅ Sale recorded successfully!")
        self.show_home()

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
        total_quantity = 0
        sales_path = os.path.join("data", "sales.csv")
        if os.path.exists(sales_path):
            with open(sales_path, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["customer_id"] == customer_id and condition(row["sale_date"]):
                        try:
                            qty = int(row.get("quantity", 1))
                        except ValueError:
                            qty = 1
                        total_quantity += qty
        return total_quantity


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

        
    # def show_daily_sales(self):
    #     self.clear_main_content()
    #     ctk.CTkLabel(self.main_content, text="Daily Sales View", font=self.header_font).pack(pady=20)

    # def show_all_sales(self):
    #     self.clear_main_content()
    #     ctk.CTkLabel(self.main_content, text="All Sales Records", font=self.header_font).pack(pady=20)

    def show_summary(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content, text="📊 Customer Summary", font=self.header_font).pack(pady=(20, 10))

        customers_path = os.path.join("data", "customers.csv")
        sales_path = os.path.join("data", "sales.csv")

        bike_models = ["CD 70", "CG 125", "CD 70 Dream", "Pridor", "CG 125S", "CG 125S GOLD"]
        summary_data = {}
        grand_totals = {model: 0 for model in bike_models}
        grand_total_all = 0

        if os.path.exists(customers_path) and os.path.exists(sales_path):
            with open(customers_path, newline='') as c_file:
                customers = {row["id"]: row["name"] for row in csv.DictReader(c_file)}

            with open(sales_path, newline='') as s_file:
                for row in csv.DictReader(s_file):
                    cid = row["customer_id"]
                    name = customers.get(cid, "Unknown")
                    model = row["bike_model"]
                    quantity = int(row.get("quantity", 1))

                    if name not in summary_data:
                        summary_data[name] = {"total": 0, "models": {m: 0 for m in bike_models}}
                    summary_data[name]["total"] += quantity
                    summary_data[name]["models"][model] += quantity

                    grand_totals[model] += quantity
                    grand_total_all += quantity

        # Build table header
        table_values = [["Customer Name", "Total Bikes"] + bike_models]

        for name, info in summary_data.items():
            row = [name, str(info["total"])] + [str(info["models"][model]) for model in bike_models]
            table_values.append(row)

        # Add grand total row
        total_row = ["Grand Total: ", str(grand_total_all)] + [""] * len(bike_models)
        table_values.append(total_row)

        # Frame for table with scrollbars
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(table_frame, bg="#2b2b2b", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Add vertical and horizontal scrollbars
        v_scrollbar = ctk.CTkScrollbar(table_frame, orientation="vertical", command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = ctk.CTkScrollbar(self.main_content, orientation="horizontal", command=canvas.xview)
        h_scrollbar.pack(fill="x")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        table_container = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=table_container, anchor="nw")

        # Use larger font for better readability
        table = CTkTable(
            master=table_container,
            values=table_values,
            corner_radius=10,
            header_color="#DC2626",
            colors=["#1E1E1E", "#2A2A2A"],
            font=("Segoe UI", 16)
        )
        table.pack()

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        table_container.bind("<Configure>", update_scroll_region)



if __name__ == "__main__":
    app = BikeSalesApp()
    app.mainloop()
