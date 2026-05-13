import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Toplevel, simpledialog
import json
import datetime
import os
import csv
import matplotlib.pyplot as plt

# Constants
THEME = {
    'bg': '#07111F',
    'card_bg': '#0F172A',
    'border': '#334155',
    'accent': '#22D3EE',
    'green': '#22C55E',
    'orange': '#F59E0B',
    'red': '#EF4444',
    'text': '#F8FAFC',
    'input_bg': '#F8FAFC',
    'input_fg': '#111827'
}

PRODUCT_DATABASE = {
    'apple': {'category': 'fruit', 'vitamins': ['C'], 'minerals': ['fiber'], 'fresh_days': 21},
    'banana': {'category': 'fruit', 'vitamins': ['B6'], 'minerals': ['potassium'], 'fresh_days': 5},
    'orange': {'category': 'fruit', 'vitamins': ['C'], 'minerals': ['fiber'], 'fresh_days': 14},
    'strawberry': {'category': 'fruit', 'vitamins': ['C'], 'minerals': ['fiber'], 'fresh_days': 4},
    'lemon': {'category': 'fruit', 'vitamins': ['C'], 'minerals': ['fiber'], 'fresh_days': 30},
    'tomato': {'category': 'vegetable', 'vitamins': ['C', 'A'], 'minerals': ['potassium'], 'fresh_days': 7},
    'cucumber': {'category': 'vegetable', 'vitamins': ['K'], 'minerals': ['potassium'], 'fresh_days': 7},
    'spinach': {'category': 'vegetable', 'vitamins': ['A', 'K'], 'minerals': ['iron'], 'fresh_days': 4},
    'broccoli': {'category': 'vegetable', 'vitamins': ['C', 'K'], 'minerals': ['fiber'], 'fresh_days': 7},
    'carrot': {'category': 'vegetable', 'vitamins': ['A'], 'minerals': ['fiber'], 'fresh_days': 21},
    'pepper': {'category': 'vegetable', 'vitamins': ['C'], 'minerals': ['fiber'], 'fresh_days': 7},
    'potato': {'category': 'vegetable', 'vitamins': ['C'], 'minerals': ['potassium'], 'fresh_days': 30},
    'onion': {'category': 'vegetable', 'vitamins': ['C'], 'minerals': ['fiber'], 'fresh_days': 30},
    'lettuce': {'category': 'vegetable', 'vitamins': ['A', 'K'], 'minerals': ['fiber'], 'fresh_days': 5},
    'milk': {'category': 'dairy', 'vitamins': ['D', 'B12'], 'minerals': ['calcium'], 'fresh_days': 7},
    'yogurt': {'category': 'dairy', 'vitamins': ['D', 'B12'], 'minerals': ['calcium'], 'fresh_days': 14},
    'cheese': {'category': 'dairy', 'vitamins': ['D', 'B12'], 'minerals': ['calcium'], 'fresh_days': 21},
    'kefir': {'category': 'dairy', 'vitamins': ['D'], 'minerals': ['calcium'], 'fresh_days': 14},
    'ayran': {'category': 'drink', 'vitamins': ['D'], 'minerals': ['calcium'], 'fresh_days': 7},
    'egg': {'category': 'deli', 'vitamins': ['D', 'B12'], 'minerals': ['protein'], 'fresh_days': 21},
    'chicken': {'category': 'meat', 'vitamins': ['B12'], 'minerals': ['protein'], 'fresh_days': 3},
    'beef': {'category': 'meat', 'vitamins': ['B12'], 'minerals': ['iron', 'protein'], 'fresh_days': 3},
    'fish': {'category': 'meat', 'vitamins': ['D'], 'minerals': ['protein'], 'fresh_days': 2},
    'olive': {'category': 'other', 'vitamins': [], 'minerals': [], 'fresh_days': 365},
    'butter': {'category': 'dairy', 'vitamins': ['A'], 'minerals': [], 'fresh_days': 14},
    'salami': {'category': 'deli', 'vitamins': ['B12'], 'minerals': ['protein'], 'fresh_days': 14},
    'sausage': {'category': 'deli', 'vitamins': ['B12'], 'minerals': ['protein'], 'fresh_days': 7},
    'turkey': {'category': 'meat', 'vitamins': ['B12'], 'minerals': ['protein'], 'fresh_days': 3},
    'ham': {'category': 'deli', 'vitamins': ['B12'], 'minerals': ['protein'], 'fresh_days': 7}
}

TRANSLATIONS = {
    'elma': 'apple', 'muz': 'banana', 'portakal': 'orange', 'çilek': 'strawberry', 'limon': 'lemon',
    'domates': 'tomato', 'salatalık': 'cucumber', 'salatalik': 'cucumber', 'ıspanak': 'spinach', 'ispanak': 'spinach',
    'brokoli': 'broccoli', 'havuç': 'carrot', 'havuc': 'carrot', 'biber': 'pepper', 'patates': 'potato',
    'soğan': 'onion', 'sogan': 'onion', 'marul': 'lettuce', 'süt': 'milk', 'sut': 'milk', 'yoğurt': 'yogurt',
    'yogurt': 'yogurt', 'peynir': 'cheese', 'yumurta': 'egg', 'tavuk': 'chicken', 'et': 'beef', 'balık': 'fish',
    'balik': 'fish', 'zeytin': 'olive', 'tereyağı': 'butter', 'tereyagi': 'butter', 'salam': 'salami', 'sucuk': 'sausage'
}

ESSENTIAL_NUTRIENTS = {
    'C': ['orange', 'lemon', 'strawberry', 'pepper'],
    'A': ['carrot', 'spinach', 'lettuce'],
    'B12': ['egg', 'cheese', 'beef', 'chicken'],
    'D': ['milk', 'yogurt', 'cheese', 'egg'],
    'calcium': ['milk', 'yogurt', 'cheese'],
    'iron': ['spinach', 'beef', 'egg'],
    'potassium': ['banana', 'potato', 'tomato'],
    'protein': ['chicken', 'egg', 'fish'],
    'fiber': ['apple', 'broccoli', 'carrot']
}

# Global variables
fridge_data = {}
usage_history = []

def load_data():
    global fridge_data, usage_history
    if os.path.exists('fridge.json'):
        with open('fridge.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, list):  # Old format
                fridge_data = {}
                for item in data:
                    name = item['name']
                    info = get_product_info(name)
                    key = f"{name}_kg"  # Assume kg for old data
                    fridge_data[key] = {
                        'name': name,
                        'category': info['category'],
                        'amount': item['weight'],
                        'unit': 'kg',
                        'date_added': item['date']
                    }
            else:  # New format
                fridge_data = data
    if os.path.exists('usage_history.json'):
        with open('usage_history.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, list):  # Old format
                usage_history = []
                for item in data:
                    usage_history.append({
                        'action': item['action'],
                        'name': item['name'],
                        'amount': item.get('weight', 0),
                        'date': item['date'].split()[0] if ' ' in item['date'] else item['date']
                    })
            else:  # New format
                usage_history = data

def save_data():
    with open('fridge.json', 'w') as f:
        json.dump(fridge_data, f, indent=4)
    with open('usage_history.json', 'w') as f:
        json.dump(usage_history, f, indent=4)

def normalize_name(name):
    name = name.lower().strip()
    return TRANSLATIONS.get(name, name)

def calculate_freshness(date_added, fresh_days):
    today = datetime.date.today()
    added_date = datetime.datetime.strptime(date_added, '%d.%m.%Y').date()
    passed_days = (today - added_date).days
    remaining_days = fresh_days - passed_days
    freshness_percent = max(0, remaining_days / fresh_days * 100)
    if remaining_days > 3:
        status = 'Fresh'
    elif 0 <= remaining_days <= 3:
        status = 'Consume Soon'
    else:
        status = 'Expired'
    return freshness_percent, remaining_days, status

def get_product_info(name):
    name = normalize_name(name)
    return PRODUCT_DATABASE.get(name, {'category': 'other', 'vitamins': [], 'minerals': [], 'fresh_days': 7})

def add_product(name, category, amount, unit, date):
    name = normalize_name(name)
    if not date:
        date = datetime.date.today().strftime('%d.%m.%Y')
    key = f"{name}_{unit}"
    if key in fridge_data:
        fridge_data[key]['amount'] += amount
        fridge_data[key]['date_added'] = date
        messagebox.showinfo("Success", "Existing product amount updated.")
    else:
        fridge_data[key] = {
            'name': name,
            'category': category,
            'amount': amount,
            'unit': unit,
            'date_added': date
        }
        messagebox.showinfo("Success", "Product added successfully.")
    save_data()
    log_action('add', name, amount, date)

def log_action(action, name, amount, date):
    usage_history.append({
        'action': action,
        'name': name,
        'amount': amount,
        'date': date
    })
    save_data()

def consume_product(key, amount):
    if key in fridge_data:
        fridge_data[key]['amount'] -= amount
        if fridge_data[key]['amount'] <= 0:
            del fridge_data[key]
        log_action('consume', fridge_data[key]['name'], amount, datetime.date.today().strftime('%d.%m.%Y'))
        save_data()

def delete_product():
    global inventory_tree, priority_panel, result_panel
    
    selected = inventory_tree.selection()

    if not selected:
        messagebox.showwarning("Delete Product", "Please select a product first.")
        return

    selected_item = selected[0]

    if selected_item not in fridge_data:
        messagebox.showwarning("Delete Product", "Selected product could not be found.")
        return

    product = fridge_data[selected_item]

    confirm = messagebox.askyesno(
        "Delete Product",
        f"Are you sure you want to delete {product.get('name', '')}?"
    )

    if not confirm:
        return

    deleted_product = fridge_data.pop(selected_item)

    usage_history.append({
        "action": "delete",
        "name": deleted_product.get("name", ""),
        "amount": deleted_product.get("amount", 0),
        "date": datetime.date.today().strftime("%d.%m.%Y")
    })

    save_data()
    update_inventory_table(inventory_tree)
    update_today_priority(priority_panel)
    update_result_panel(
        result_panel,
        "Product deleted. Select another product or search again."
    )

    messagebox.showinfo("Delete Product", "Product deleted successfully.")

def consume_reduce(tree, result_panel, priority_panel):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Consume / Reduce", "Please select a product first.")
        return
    key = selected[0]
    amount = simpledialog.askfloat("Consume / Reduce", "Enter amount to reduce:", minvalue=0.1)
    if amount is None:
        return
    consume_product(key, amount)
    update_inventory_table(tree)
    update_today_priority(priority_panel)
    update_result_panel(result_panel, "Product consumed. Select another product or search again.")

def add_more(tree, result_panel, priority_panel):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Add More", "Please select a product first.")
        return
    key = selected[0]
    product = fridge_data[key]
    amount = simpledialog.askfloat("Add More", f"Enter amount to add to {product['name']}:", minvalue=0.1)
    if amount is None:
        return
    add_product(product['name'], product['category'], amount, product['unit'], datetime.date.today().strftime('%d.%m.%Y'))
    update_inventory_table(tree)
    update_today_priority(priority_panel)
    update_result_panel(result_panel, "Product amount added. Select another product or search again.")

def product_matches_search(product, search_text):
    search_text = search_text.lower().strip()
    name = product['name']
    category = product['category']
    if search_text in name.lower() or search_text in category.lower():
        return True
    # Check translations
    for turkish, english in TRANSLATIONS.items():
        if search_text == turkish and english == name:
            return True
    return False

def search_product(search_text, tree, result_panel):
    search_text = search_text.lower().strip()
    if not search_text:
        update_inventory_table(tree)
        update_result_panel(result_panel, "Search a product or select one from the inventory table.")
        return
    for item in tree.get_children():
        tree.delete(item)
    found = False
    for key, product in fridge_data.items():
        if product_matches_search(product, search_text):
            tree.insert('', 'end', values=(product['name'], product['category'], product['amount'], product['unit'], product['date_added'], 
                                           f"{calculate_freshness(product['date_added'], get_product_info(product['name'])['fresh_days'])[0]:.1f}%",
                                           calculate_freshness(product['date_added'], get_product_info(product['name'])['fresh_days'])[1],
                                           calculate_freshness(product['date_added'], get_product_info(product['name'])['fresh_days'])[2]))
            tree.selection_set(tree.get_children()[-1])
            tree.focus(tree.get_children()[-1])
            update_product_details(tree, result_panel)
            found = True
            break
    if not found:
        update_result_panel(result_panel, "No matching product found.")
        update_inventory_table(tree)

def update_inventory_table(tree, category_filter='All'):
    for item in tree.get_children():
        tree.delete(item)
    for key, product in fridge_data.items():
        if category_filter == 'All' or product['category'] == category_filter:
            name = product['name']
            info = get_product_info(name)
            freshness, remaining, status = calculate_freshness(product['date_added'], info['fresh_days'])
            tree.insert('', 'end', iid=key, values=(name, product['category'], product['amount'], product['unit'], 
                                                     product['date_added'], f"{freshness:.1f}%", remaining, status))

def update_product_details(tree, panel):
    selected = tree.selection()
    if selected:
        key = selected[0]
        product = fridge_data[key]
        name = product['name']
        info = get_product_info(name)
        freshness, remaining, status = calculate_freshness(product['date_added'], info['fresh_days'])
        details = f"Product: {name}\nCategory: {product['category']}\nAmount: {product['amount']} {product['unit']}\nDate Added: {product['date_added']}\nFreshness: {freshness:.1f}%\nRemaining Days: {remaining}\nStatus: {status}\nVitamins: {', '.join(info['vitamins']) if info['vitamins'] else 'None'}\nMinerals: {', '.join(info['minerals']) if info['minerals'] else 'None'}"
        update_result_panel(panel, details)
    else:
        update_result_panel(panel, "Search a product or select one from the inventory table.")

def update_result_panel(panel, text):
    panel.config(state='normal')
    panel.delete(1.0, tk.END)
    panel.insert(tk.END, text)
    panel.config(state='disabled')

def update_today_priority(panel):
    urgent = []
    for key, product in fridge_data.items():
        name = product['name']
        info = get_product_info(name)
        _, remaining, status = calculate_freshness(product['date_added'], info['fresh_days'])
        if status == 'Expired' or (0 <= remaining <= 3):
            urgent.append((name, remaining if remaining >= 0 else 'Expired'))
    urgent.sort(key=lambda x: x[1] if isinstance(x[1], int) else -1)
    text = "Today's Priority\n\n"
    if urgent:
        for i, (name, rem) in enumerate(urgent[:3], 1):
            text += f"{i}. {name} - {rem}\n"
    else:
        text += "No urgent products today."
    update_result_panel(panel, text)

def show_report_window(title, text):
    window = Toplevel()
    window.title(title)
    window.configure(bg=THEME['bg'])
    text_area = scrolledtext.ScrolledText(window, bg=THEME['card_bg'], fg=THEME['text'], font=('Arial', 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_area.insert(tk.END, text)
    text_area.config(state='disabled')

def weekly_report():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    week_actions = [h for h in usage_history if datetime.datetime.strptime(h['date'], '%d.%m.%Y').date() >= week_ago]
    total_actions = len(week_actions)
    consumed = [h for h in week_actions if h['action'] == 'consume']
    added = [h for h in week_actions if h['action'] == 'add']
    deleted = [h for h in week_actions if h['action'] == 'delete']
    text = f"Weekly Report (Last 7 days)\n\nTotal Actions: {total_actions}\n\nConsumed Products:\n"
    for h in consumed:
        text += f"- {h['name']}: {h['amount']}\n"
    text += "\nAdded Products:\n"
    for h in added:
        text += f"- {h['name']}: {h['amount']}\n"
    text += "\nDeleted Products:\n"
    for h in deleted:
        text += f"- {h['name']}\n"
    show_report_window("Weekly Report", text)

def nutrition_suggestions():
    recent_consumed = [h['name'] for h in usage_history[-50:] if h['action'] == 'consume']  # Last 50 actions
    consumed_nutrients = set()
    for name in recent_consumed:
        info = get_product_info(name)
        consumed_nutrients.update(info['vitamins'] + info['minerals'])
    missing = set(ESSENTIAL_NUTRIENTS.keys()) - consumed_nutrients
    suggestions = []
    for nutrient in missing:
        suggestions.extend(ESSENTIAL_NUTRIENTS[nutrient])
    suggestions = list(set(suggestions))
    text = "Educational Nutrition Awareness Suggestions\n\nMissing / low nutrient groups:\n"
    for nutrient in missing:
        prods = ', '.join(ESSENTIAL_NUTRIENTS[nutrient][:3])  # İlk 3
        text += f"- {nutrient}: consider {prods}\n"
    text += "\nCombination ideas:\n"
    current_products = [p['name'] for p in fridge_data.values()]
    if 'spinach' in current_products and 'lemon' in current_products:
        text += "- spinach + lemon can be a good combination\n"
    if 'yogurt' in current_products and any(p in ['apple', 'orange', 'strawberry'] for p in current_products):
        text += "- yogurt + fruit can be a good option\n"
    if 'egg' in current_products and any(p in ['lettuce', 'spinach', 'pepper'] for p in current_products):
        text += "- egg + greens can be a good option\n"
    text += "\nThis is an educational nutrition awareness suggestion, not medical advice."
    show_report_window("Nutrition Suggestions", text)

def export_csv():
    with open('fridge_report.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Product', 'Category', 'Amount', 'Unit', 'Date Added', 'Freshness %', 'Remaining Days', 'Status'])
        for key, product in fridge_data.items():
            name = product['name']
            info = get_product_info(name)
            freshness, remaining, status = calculate_freshness(product['date_added'], info['fresh_days'])
            writer.writerow([name, product['category'], product['amount'], product['unit'], product['date_added'], f"{freshness:.1f}%", remaining, status])
    messagebox.showinfo("Success", "Exported to fridge_report.csv")

def load_demo_data():
    if not fridge_data:
        demo_products = [
            ('apple', 'fruit', 5, 'adet', (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y')),
            ('milk', 'dairy', 1, 'litre', (datetime.date.today() - datetime.timedelta(days=5)).strftime('%d.%m.%Y')),
            ('strawberry', 'fruit', 200, 'kg', (datetime.date.today() - datetime.timedelta(days=3)).strftime('%d.%m.%Y')),
            ('egg', 'deli', 12, 'adet', (datetime.date.today() - datetime.timedelta(days=10)).strftime('%d.%m.%Y')),
            ('spinach', 'vegetable', 0.5, 'kg', (datetime.date.today() - datetime.timedelta(days=2)).strftime('%d.%m.%Y')),
            ('cheese', 'dairy', 0.3, 'kg', (datetime.date.today() - datetime.timedelta(days=15)).strftime('%d.%m.%Y')),
            ('orange', 'fruit', 3, 'adet', (datetime.date.today() - datetime.timedelta(days=10)).strftime('%d.%m.%Y')),
            ('carrot', 'vegetable', 1, 'kg', (datetime.date.today() - datetime.timedelta(days=20)).strftime('%d.%m.%Y'))
        ]
        for name, cat, amt, unit, date in demo_products:
            add_product(name, cat, amt, unit, date)
        messagebox.showinfo("Success", "Demo data loaded.")

def freshness_graph(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Freshness Graph", "Please select a product first.")
        return
    key = selected[0]
    if key in fridge_data:
        product = fridge_data[key]
        name = product['name']
        info = get_product_info(name)
        fresh_days = info['fresh_days']
        added_date = datetime.datetime.strptime(product['date_added'], '%d.%m.%Y').date()
        days = list(range(fresh_days + 1))
        freshness = [max(0, (fresh_days - d) / fresh_days * 100) for d in days]
        dates = [(added_date + datetime.timedelta(days=d)).strftime('%d.%m') for d in days]
        plt.figure(figsize=(8, 4))
        plt.plot(dates, freshness, marker='o')
        plt.title(f'{name} Freshness Graph')
        plt.xlabel('Date')
        plt.ylabel('Freshness %')
        plt.grid(True)
        plt.show()

def category_graph():
    categories = {}
    for product in fridge_data.values():
        cat = product['category']
        categories[cat] = categories.get(cat, 0) + 1
    if categories:
        plt.figure(figsize=(8, 4))
        plt.bar(categories.keys(), categories.values())
        plt.title('Product Count by Category')
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.show()
    else:
        messagebox.showinfo("Info", "No products to display.")

def weekly_usage_graph():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    week_actions = [h for h in usage_history if datetime.datetime.strptime(h['date'], '%d.%m.%Y').date() >= week_ago]
    dates = [(week_ago + datetime.timedelta(days=i)).strftime('%d.%m') for i in range(8)]
    counts = [0] * 8
    for h in week_actions:
        if h['action'] == 'consume':
            day_index = (datetime.datetime.strptime(h['date'], '%d.%m.%Y').date() - week_ago).days
            if 0 <= day_index < 8:
                counts[day_index] += 1
    plt.figure(figsize=(8, 4))
    plt.bar(dates, counts)
    plt.title('Weekly Consumption Activity')
    plt.xlabel('Date')
    plt.ylabel('Consume Actions')
    plt.show()

def freshness_overview_graph():
    if not fridge_data:
        messagebox.showinfo("Info", "No products to display.")
        return
    products = []
    freshness = []
    colors = []
    for key, product in fridge_data.items():
        name = product['name']
        info = get_product_info(name)
        fresh, _, status = calculate_freshness(product['date_added'], info['fresh_days'])
        products.append(name)
        freshness.append(fresh)
        if status == 'Fresh':
            colors.append('green')
        elif status == 'Consume Soon':
            colors.append('orange')
        else:
            colors.append('red')
    plt.figure(figsize=(10, 5))
    plt.bar(products, freshness, color=colors)
    plt.title('Current Freshness Overview')
    plt.xlabel('Product')
    plt.ylabel('Freshness %')
    plt.xticks(rotation=45)
    plt.show()

def main():
    global inventory_tree, priority_panel, result_panel
    
    load_data()
    
    root = tk.Tk()
    root.title("Smart Fridge Nutrition Assistant")
    root.configure(bg=THEME['bg'])
    root.geometry("1400x850")
    
    # Header
    header_frame = tk.Frame(root, bg=THEME['bg'])
    header_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Label(header_frame, text="🥗 Smart Fridge Nutrition Assistant", font=('Arial', 20, 'bold'), bg=THEME['bg'], fg=THEME['accent']).pack(side=tk.LEFT)
    tk.Label(header_frame, text="Track your fridge inventory, freshness status and nutrition awareness.", font=('Arial', 10), bg=THEME['bg'], fg=THEME['text']).pack(side=tk.LEFT, padx=20)
    
    # Search Area
    search_frame = tk.Frame(root, bg=THEME['card_bg'], relief='solid', bd=1)
    search_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(search_frame, text="Search product in your fridge...", font=('Arial', 12), bg=THEME['card_bg'], fg=THEME['text']).pack(side=tk.LEFT, padx=10, pady=10)
    search_entry = tk.Entry(search_frame, font=('Arial', 14), bg=THEME['input_bg'], fg=THEME['input_fg'])
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=10)
    search_entry.bind('<Return>', lambda e: search_product(search_entry.get(), inventory_tree, result_panel))
    tk.Button(search_frame, text="Search", command=lambda: search_product(search_entry.get(), inventory_tree, result_panel), bg=THEME['accent'], fg=THEME['bg'], width=12).pack(side=tk.LEFT, padx=4, pady=10)
    tk.Button(search_frame, text="Clear Search", command=lambda: [search_entry.delete(0, tk.END), update_inventory_table(inventory_tree), update_result_panel(result_panel, "Search a product or select one from the inventory table.")], bg=THEME['border'], fg=THEME['text'], width=12).pack(side=tk.LEFT, padx=4, pady=10)
    
    # Search Result Card
    result_card = tk.Frame(root, bg=THEME['card_bg'], relief='solid', bd=1)
    result_card.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(result_card, text="Search Result / Selected Product", font=('Arial', 12, 'bold'), bg=THEME['card_bg'], fg=THEME['accent']).pack(anchor=tk.W, padx=10, pady=(10, 0))
    result_panel = tk.Text(result_card, bg=THEME['card_bg'], fg=THEME['text'], font=('Arial', 11), state='disabled', height=4, wrap='word')
    result_panel.pack(fill=tk.X, padx=10, pady=10)
    
    # Main Content
    content_frame = tk.Frame(root, bg=THEME['bg'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Left Panel: Add Product
    left_frame = tk.Frame(content_frame, bg=THEME['card_bg'], relief='solid', bd=1, width=270)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
    left_frame.pack_propagate(False)
    tk.Label(left_frame, text="Add Product", font=('Arial', 14, 'bold'), bg=THEME['card_bg'], fg=THEME['accent']).pack(pady=10)
    tk.Label(left_frame, text="Product Name", bg=THEME['card_bg'], fg=THEME['text']).pack(anchor=tk.W, padx=10)
    name_entry = tk.Entry(left_frame, bg=THEME['input_bg'], fg=THEME['input_fg'])
    name_entry.pack(fill=tk.X, padx=10, pady=2)
    tk.Label(left_frame, text="Category", bg=THEME['card_bg'], fg=THEME['text']).pack(anchor=tk.W, padx=10)
    category_combo = ttk.Combobox(left_frame, values=['fruit', 'vegetable', 'dairy', 'meat', 'deli', 'drink', 'other'])
    category_combo.pack(fill=tk.X, padx=10, pady=2)
    tk.Label(left_frame, text="Amount", bg=THEME['card_bg'], fg=THEME['text']).pack(anchor=tk.W, padx=10)
    amount_entry = tk.Entry(left_frame, bg=THEME['input_bg'], fg=THEME['input_fg'])
    amount_entry.pack(fill=tk.X, padx=10, pady=2)
    tk.Label(left_frame, text="Unit", bg=THEME['card_bg'], fg=THEME['text']).pack(anchor=tk.W, padx=10)
    unit_combo = ttk.Combobox(left_frame, values=['kg', 'adet', 'litre', 'paket'])
    unit_combo.pack(fill=tk.X, padx=10, pady=2)
    tk.Label(left_frame, text="Date Added (dd.mm.yyyy)", bg=THEME['card_bg'], fg=THEME['text']).pack(anchor=tk.W, padx=10)
    date_entry = tk.Entry(left_frame, bg=THEME['input_bg'], fg=THEME['input_fg'])
    date_entry.pack(fill=tk.X, padx=10, pady=2)
    tk.Label(left_frame, text="Leave empty for today", font=('Arial', 8), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor=tk.W, padx=10)
    tk.Button(left_frame, text="Add Product", command=lambda: [add_product(name_entry.get(), category_combo.get() or get_product_info(name_entry.get())['category'], float(amount_entry.get() or 0), unit_combo.get() or 'adet', date_entry.get()), update_inventory_table(inventory_tree), update_today_priority(priority_panel)], bg=THEME['green'], fg=THEME['bg']).pack(pady=(10, 4), fill=tk.X, padx=10)
    
    # Center: Inventory Table
    center_frame = tk.Frame(content_frame, bg=THEME['card_bg'], relief='solid', bd=1)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    tk.Label(center_frame, text="Current Fridge Inventory", font=('Arial', 14, 'bold'), bg=THEME['card_bg'], fg=THEME['accent']).pack(pady=10)
    tk.Label(center_frame, text="All products currently in your fridge", font=('Arial', 10), bg=THEME['card_bg'], fg=THEME['text']).pack(pady=5)
    
    # Category Filter
    filter_frame = tk.Frame(center_frame, bg=THEME['card_bg'])
    filter_frame.pack(fill=tk.X, padx=10)
    tk.Label(filter_frame, text="Filter by Category:", bg=THEME['card_bg'], fg=THEME['text']).pack(side=tk.LEFT)
    category_filter = ttk.Combobox(filter_frame, values=['All', 'fruit', 'vegetable', 'dairy', 'meat', 'deli', 'drink', 'other'])
    category_filter.set('All')
    category_filter.pack(side=tk.LEFT, padx=5)
    category_filter.bind('<<ComboboxSelected>>', lambda e: update_inventory_table(inventory_tree, category_filter.get()))
    
    # Table
    table_frame = tk.Frame(center_frame, bg=THEME['card_bg'])
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    columns = ('Product', 'Category', 'Amount', 'Unit', 'Date Added', 'Freshness %', 'Remaining Days', 'Status')
    inventory_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
    for col in columns:
        inventory_tree.heading(col, text=col)
        inventory_tree.column(col, width=120)
    inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=inventory_tree.yview)
    inventory_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    inventory_tree.bind('<<TreeviewSelect>>', lambda e: update_product_details(inventory_tree, selected_panel))
    
    # Action Buttons
    action_frame = tk.Frame(center_frame, bg=THEME['card_bg'])
    action_frame.pack(fill=tk.X, padx=10, pady=5)
    # Row 0
    tk.Button(action_frame, text="Consume / Reduce", command=lambda: consume_reduce(inventory_tree, result_panel, priority_panel), bg=THEME['orange'], fg=THEME['bg'], width=20).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(action_frame, text="Add More", command=lambda: add_more(inventory_tree, result_panel, priority_panel), bg=THEME['green'], fg=THEME['bg'], width=20).grid(row=0, column=1, padx=4, pady=4)
    tk.Button(action_frame, text="Delete Product", command=delete_product, bg='#EF4444', fg='white', font=('Arial', 10, 'bold'), width=20).grid(row=0, column=2, padx=4, pady=4)
    tk.Button(action_frame, text="Freshness Graph", command=lambda: freshness_graph(inventory_tree), bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=0, column=3, padx=4, pady=4)
    # Row 1
    tk.Button(action_frame, text="Category Graph", command=category_graph, bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(action_frame, text="Weekly Usage Graph", command=weekly_usage_graph, bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=1, column=1, padx=4, pady=4)
    tk.Button(action_frame, text="Freshness Overview", command=freshness_overview_graph, bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=1, column=2, padx=4, pady=4)
    tk.Button(action_frame, text="Weekly Report", command=weekly_report, bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=1, column=3, padx=4, pady=4)
    # Row 2
    tk.Button(action_frame, text="Nutrition Suggestions", command=nutrition_suggestions, bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=2, column=0, padx=4, pady=4)
    tk.Button(action_frame, text="Export CSV", command=export_csv, bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=2, column=1, padx=4, pady=4)
    tk.Button(action_frame, text="Load Demo Data", command=lambda: [load_demo_data(), update_inventory_table(inventory_tree), update_today_priority(priority_panel)], bg=THEME['accent'], fg=THEME['bg'], width=20).grid(row=2, column=2, padx=4, pady=4)
    tk.Button(action_frame, text="Refresh", command=lambda: [update_inventory_table(inventory_tree), update_today_priority(priority_panel)], bg=THEME['border'], fg=THEME['text'], width=20).grid(row=2, column=3, padx=4, pady=4)
    
    # Right Panel: Selected Product Details + Today’s Priority
    right_frame = tk.Frame(content_frame, bg=THEME['card_bg'], relief='solid', bd=1, width=300)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
    right_frame.pack_propagate(False)
    tk.Label(right_frame, text="Selected Product Details", font=('Arial', 12, 'bold'), bg=THEME['card_bg'], fg=THEME['accent']).pack(anchor=tk.W, padx=10, pady=(10, 0))
    selected_panel = tk.Text(right_frame, bg=THEME['card_bg'], fg=THEME['text'], font=('Arial', 10), state='disabled', height=8, wrap='word')
    selected_panel.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(right_frame, text="Today's Priority", font=('Arial', 12, 'bold'), bg=THEME['card_bg'], fg=THEME['accent']).pack(anchor=tk.W, padx=10, pady=(10, 0))
    priority_panel = tk.Text(right_frame, bg=THEME['card_bg'], fg=THEME['text'], font=('Arial', 10), state='disabled', height=6, wrap='word')
    priority_panel.pack(fill=tk.X, padx=10, pady=10)
    
    # Initial load
    update_inventory_table(inventory_tree)
    update_today_priority(priority_panel)
    update_result_panel(result_panel, "Search a product or select one from the inventory table.")
    
    root.mainloop()

if __name__ == "__main__":
    main()