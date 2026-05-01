import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE = "fridge.json"
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
        with open(FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            products = json.loads(content) if content else []
    except:
        products = []
        save_data()

def save_data():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

def normalize(name):
    return translate.get(name.strip().lower(), name.strip().lower())

def get_date():
    d = input("Date (dd.mm.yyyy) or Enter: ").strip()
    if d == "":
        return datetime.now().strftime("%d.%m.%Y")
    try:
        datetime.strptime(d, "%d.%m.%Y")
        return d
    except:
        return datetime.now().strftime("%d.%m.%Y")

def calculate(p):
    today = datetime.now()
    added = datetime.strptime(p["date"], "%d.%m.%Y")
    passed = (today - added).days
    total = p["life"]
    remaining = total - passed
    percent = max(0, (remaining / total) * 100)
    if remaining > 3:
        status = "Fresh"
    elif remaining >= 0:
        status = "Warning"
    else:
        status = "Expired"
    return passed, remaining, percent, status

def color(status):
    return "green" if status == "Fresh" else "orange" if status == "Warning" else "red"

def add_product():
    name = normalize(input("Product: "))
    if name not in shelf_life:
        print("Not found\n"); return
    try:
        w = float(input("Weight: "))
        if w <= 0: return
    except:
        return
    d = get_date()
    for p in products:
        if p["name"] == name:
            p["weight"] += w
            p["date"] = d
            save_data()
            return
    products.append({"name": name, "weight": w, "date": d, "life": shelf_life[name]})
    save_data()

def list_products():
    if not products:
        print("Empty\n"); return
    for i, p in enumerate(products, 1):
        passed, rem, per, s = calculate(p)
        print(f"{i}- {p['name']} ({p['weight']}kg) | {p['date']} | %{per:.1f} | {s}")

def delete_product():
    list_products()
    try:
        i = int(input("Delete: ")) - 1
        products.pop(i)
        save_data()
    except:
        pass

def update_weight():
    list_products()
    try:
        i = int(input("Select: ")) - 1
        p = products[i]
    except:
        return
    print("1 Add | 2 Reduce")
    try:
        a = input("Choice: ")
        amt = float(input("Amount: "))
    except:
        return
    if a == "1":
        p["weight"] += amt
    elif a == "2":
        if amt > p["weight"]: return
        p["weight"] -= amt
        if p["weight"] == 0:
            products.remove(p)
    save_data()

def warnings():
    for p in products:
        _, r, _, s = calculate(p)
        if s == "Warning":
            print(p["name"], "→ soon")
        elif s == "Expired":
            print(p["name"], "→ spoiled")

def single_graph():
    list_products()
    try:
        i = int(input("Select: ")) - 1
        p = products[i]
    except:
        return

    passed, _, per, s = calculate(p)

    days = list(range(p["life"] + 1))
    vals = [100 - (d / p["life"]) * 100 for d in days]

    cd = min(max(passed, 0), p["life"])

    plt.plot(days, vals, color=color(s), label=p["name"])
    plt.scatter([cd], [per], color=color(s), label="Current")

    plt.title(p["name"] + " Freshness Graph")
    plt.xlabel("Days")
    plt.ylabel("Freshness %")
    plt.legend()
    plt.grid()

    plt.show()

def multi_graph():
    list_products()
    ch = input("Select (1,2) or ALL: ").strip()

    selected = products if ch.lower() == "all" else []

    if ch.lower() != "all":
        for x in ch.split(","):
            try:
                selected.append(products[int(x.strip()) - 1])
            except:
                pass

    if not selected:
        return

    for p in selected:
        passed, _, per, s = calculate(p)
        days = list(range(p["life"] + 1))
        vals = [100 - (d / p["life"]) * 100 for d in days]
        cd = min(max(passed, 0), p["life"])

        plt.plot(days, vals, label=p["name"])
        plt.scatter([cd], [per], color=color(s))

    plt.title("Freshness Comparison")
    plt.xlabel("Days")
    plt.ylabel("Freshness %")
    plt.legend(title="Products")
    plt.grid()

    plt.show()

def menu():
    while True:
        print("\n1 Add\n2 List\n3 Delete\n4 Warn\n5 Graph\n6 Multi\n7 Update\n8 Exit")
        c = input("Choice: ")
        if c == "1": add_product()
        elif c == "2": list_products()
        elif c == "3": delete_product()
        elif c == "4": warnings()
        elif c == "5": single_graph()
        elif c == "6": multi_graph()
        elif c == "7": update_weight()
        elif c == "8": break

load_data()
menu()
