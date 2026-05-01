import json
import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

FILE = "fridge.json"
CSV_FILE = "fridge_report.csv"
products = []

shelf_life = {
    "apple": 21, "banana": 5, "orange": 14, "strawberry": 4,
    "grape": 7, "pear": 10, "tomato": 7, "cucumber": 6,
    "pepper": 7, "carrot": 21, "potato": 30, "onion": 30,
    "lettuce": 5, "parsley": 4, "spinach": 4,
    "eggplant": 5, "zucchini": 5, "lemon": 21,
    "watermelon": 7, "melon": 7
}

translate = {
    "elma": "apple", "muz": "banana", "portakal": "orange",
    "çilek": "strawberry", "üzüm": "grape", "uzum": "grape",
    "armut": "pear", "domates": "tomato",
    "salatalık": "cucumber", "salatalik": "cucumber",
    "biber": "pepper", "havuç": "carrot", "havuc": "carrot",
    "patates": "potato", "soğan": "onion", "sogan": "onion",
    "marul": "lettuce", "maydanoz": "parsley",
    "ıspanak": "spinach", "ispanak": "spinach",
    "patlıcan": "eggplant", "patlican": "eggplant",
    "kabak": "zucchini", "limon": "lemon",
    "karpuz": "watermelon", "kavun": "melon"
}


def load_data():
    global products
    if not os.path.exists(FILE):
        products = []
        return

    try:
        with open(FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            products = json.loads(content) if content else []
    except:
        products = []
        save_data()


def save_data():
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4, ensure_ascii=False)


def normalize(name):
    return translate.get(name.strip().lower(), name.strip().lower())


def calculate(product):
    today = datetime.now()
    added_date = datetime.strptime(product["date"], "%d.%m.%Y")

    passed_days = (today - added_date).days
    total_life = product["life"]
    remaining_days = total_life - passed_days
    freshness = max(0, (remaining_days / total_life) * 100)

    if remaining_days > 3:
        status = "Fresh"
    elif remaining_days >= 0:
        status = "Warning"
    else:
        status = "Expired"

    return passed_days, remaining_days, freshness, status


def get_color(status):
    if status == "Fresh":
        return "green"
    if status == "Warning":
        return "orange"
    return "red"


def refresh_list():
    product_list.delete(0, tk.END)

    if not products:
        product_list.insert(tk.END, "No products found.")
        return

    for product in products:
        passed, remaining, freshness, status = calculate(product)
        text = (
            f"{product['name']} | {product['weight']} kg | "
            f"Date: {product['date']} | Freshness: %{freshness:.1f} | "
            f"Remaining: {remaining} days | {status}"
        )
        product_list.insert(tk.END, text)


def add_product():
    name = normalize(name_entry.get())
    date = date_entry.get().strip()

    if name not in shelf_life:
        messagebox.showerror("Error", "Product not found in the system.")
        return

    try:
        weight = float(weight_entry.get())
        if weight <= 0:
            messagebox.showerror("Error", "Weight must be greater than 0.")
            return
    except:
        messagebox.showerror("Error", "Invalid weight.")
        return

    if date == "":
        date = datetime.now().strftime("%d.%m.%Y")
    else:
        try:
            datetime.strptime(date, "%d.%m.%Y")
        except:
            messagebox.showerror("Error", "Invalid date format. Use dd.mm.yyyy")
            return

    for product in products:
        if product["name"] == name:
            product["weight"] += weight
            product["date"] = date
            save_data()
            refresh_list()
            clear_entries()
            messagebox.showinfo("Success", "Product already exists. Weight updated.")
            return

    products.append({
        "name": name,
        "weight": weight,
        "date": date,
        "life": shelf_life[name]
    })

    save_data()
    refresh_list()
    clear_entries()
    messagebox.showinfo("Success", "Product added.")


def delete_product():
    selected = product_list.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a product first.")
        return

    index = selected[0]

    if index >= len(products):
        return

    deleted = products.pop(index)
    save_data()
    refresh_list()
    messagebox.showinfo("Deleted", f"{deleted['name']} deleted.")


def update_weight():
    selected = product_list.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a product first.")
        return

    index = selected[0]

    if index >= len(products):
        return

    product = products[index]

    action = simpledialog.askstring("Update Weight", "Type add or reduce:")
    if action is None:
        return

    action = action.lower().strip()

    try:
        amount = float(simpledialog.askstring("Amount", "Enter amount in kg:"))
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            return
    except:
        messagebox.showerror("Error", "Invalid amount.")
        return

    if action == "add":
        product["weight"] += amount

    elif action == "reduce":
        if amount > product["weight"]:
            messagebox.showerror("Error", "You cannot reduce more than current weight.")
            return

        product["weight"] -= amount

        if product["weight"] == 0:
            products.remove(product)
    else:
        messagebox.showerror("Error", "Invalid action. Type add or reduce.")
        return

    save_data()
    refresh_list()


def show_warnings():
    warning_text = ""

    for product in products:
        _, remaining, _, status = calculate(product)

        if status == "Warning":
            warning_text += f"{product['name']} should be consumed soon. Remaining: {remaining} days\n"
        elif status == "Expired":
            warning_text += f"{product['name']} may be spoiled. Remove it from fridge.\n"

    if warning_text == "":
        warning_text = "No warnings. All products are fresh."

    messagebox.showinfo("Warnings", warning_text)


def show_single_graph():
    selected = product_list.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a product first.")
        return

    index = selected[0]

    if index >= len(products):
        return

    product = products[index]
    passed, _, freshness, status = calculate(product)

    days = list(range(product["life"] + 1))
    values = [100 - (day / product["life"]) * 100 for day in days]
    current_day = min(max(passed, 0), product["life"])
    color = get_color(status)

    plt.plot(days, values, color=color, label=product["name"])
    plt.scatter([current_day], [freshness], color=color, s=80, label="Current")
    plt.title(f"{product['name']} Freshness Graph")
    plt.xlabel("Days")
    plt.ylabel("Freshness %")
    plt.grid()
    plt.legend()
    plt.show()


def show_multi_graph():
    if not products:
        messagebox.showwarning("Warning", "No products found.")
        return

    for product in products:
        passed, _, freshness, status = calculate(product)
        days = list(range(product["life"] + 1))
        values = [100 - (day / product["life"]) * 100 for day in days]
        current_day = min(max(passed, 0), product["life"])

        plt.plot(days, values, label=product["name"])
        plt.scatter([current_day], [freshness], color=get_color(status), s=70)

    plt.title("Freshness Comparison")
    plt.xlabel("Days")
    plt.ylabel("Freshness %")
    plt.grid()
    plt.legend(title="Products")
    plt.show()


def export_csv():
    if not products:
        messagebox.showwarning("Warning", "No products to export.")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "name", "weight", "date", "passed_days",
            "remaining_days", "freshness_percent", "status"
        ])

        for product in products:
            passed, remaining, freshness, status = calculate(product)
            writer.writerow([
                product["name"],
                product["weight"],
                product["date"],
                passed,
                remaining,
                round(freshness, 2),
                status
            ])

    messagebox.showinfo("CSV Exported", f"Report created: {CSV_FILE}")


def clear_entries():
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


load_data()

root = tk.Tk()
root.title("Smart Fridge - Food Freshness Tracker")
root.geometry("900x600")

title = tk.Label(root, text="Smart Fridge", font=("Arial", 22, "bold"))
title.pack(pady=10)

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Product").grid(row=0, column=0, padx=5)
name_entry = tk.Entry(form_frame, width=20)
name_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Weight (kg)").grid(row=0, column=2, padx=5)
weight_entry = tk.Entry(form_frame, width=15)
weight_entry.grid(row=0, column=3, padx=5)

tk.Label(form_frame, text="Date").grid(row=0, column=4, padx=5)
date_entry = tk.Entry(form_frame, width=15)
date_entry.grid(row=0, column=5, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Product", width=18, command=add_product).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Delete Product", width=18, command=delete_product).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Update Weight", width=18, command=update_weight).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Warnings", width=18, command=show_warnings).grid(row=0, column=3, padx=5, pady=5)

tk.Button(button_frame, text="Single Graph", width=18, command=show_single_graph).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Multi Graph", width=18, command=show_multi_graph).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Export CSV", width=18, command=export_csv).grid(row=1, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Refresh", width=18, command=refresh_list).grid(row=1, column=3, padx=5, pady=5)

product_list = tk.Listbox(root, width=120, height=20)
product_list.pack(pady=10)

refresh_list()
root.mainloop()