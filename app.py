import pandas as pd
import math

inventory = pd.read_csv("inventory.csv")
sales = pd.read_csv("sales.csv")


def show_inventory():

    print("\n===== INVENTORY =====")
    print(inventory.to_string(index=False))


def sell_item():

    global inventory

    item_id = int(input("Enter Item ID: "))
    qty = int(input("Enter Quantity Sold: "))

    idx = inventory[inventory["ItemID"] == item_id].index

    if len(idx) == 0:
        print("Item Not Found")
        return

    idx = idx[0]

    current_stock = inventory.loc[idx, "Stock"]

    if qty > current_stock:
        print("Not enough stock available")
        return

    inventory.loc[idx, "Stock"] -= qty

    print("Sale recorded")

    if inventory.loc[idx, "Stock"] <= inventory.loc[idx, "ReorderLevel"]:
        print("ALERT: REORDER REQUIRED")

    inventory.to_csv("inventory.csv", index=False)


def add_stock():

    global inventory

    item_id = int(input("Enter Item ID: "))
    qty = int(input("Enter Quantity Added: "))

    idx = inventory[inventory["ItemID"] == item_id].index

    if len(idx) == 0:
        print("Item Not Found")
        return

    idx = idx[0]

    inventory.loc[idx, "Stock"] += qty

    print("Stock Updated")

    inventory.to_csv("inventory.csv", index=False)


def forecast_demand():

    item_id = int(input("Enter Item ID: "))

    row = sales[sales["ItemID"] == item_id]

    if row.empty:
        print("No Sales Data Found")
        return

    values = row.iloc[0, 1:].tolist()

    forecast = sum(values[-3:]) / 3

    print(
        f"Predicted Next Month Demand = {forecast:.2f} units"
    )


def calculate_eoq():

    annual_demand = float(input("Annual Demand: "))
    ordering_cost = float(input("Ordering Cost: "))
    holding_cost = float(input("Holding Cost: "))

    eoq = math.sqrt(
        (2 * annual_demand * ordering_cost)
        / holding_cost
    )

    print(f"EOQ = {eoq:.2f} units")


def inventory_value():

    total = (
        inventory["Stock"]
        * inventory["UnitCost"]
    ).sum()

    print(
        f"\nTotal Inventory Value = ₹{total:,.2f}"
    )


def low_stock_items():

    low_stock = inventory[
        inventory["Stock"]
        <= inventory["ReorderLevel"]
    ]

    if low_stock.empty:
        print("\nNo Low Stock Items")
    else:
        print("\n===== LOW STOCK ITEMS =====")
        print(low_stock.to_string(index=False))

def reorder_point_report():

    print("\n===== REORDER POINT REPORT =====")

    for _, item in inventory.iterrows():

        item_id = item["ItemID"]

        sales_row = sales[sales["ItemID"] == item_id]

        if sales_row.empty:
            continue

        sales_values = sales_row.iloc[0, 1:].tolist()

        avg_monthly_demand = sum(sales_values) / len(sales_values)

        avg_daily_demand = avg_monthly_demand / 30

        lead_time = item["LeadTime"]

        safety_stock = item["SafetyStock"]

        reorder_point = (
            avg_daily_demand * lead_time
        ) + safety_stock

        print(f"\nItem: {item['ItemName']}")
        print(f"Current Stock: {item['Stock']}")
        print(f"Reorder Point: {reorder_point:.2f}")

        if item["Stock"] <= reorder_point:
            print("REORDER REQUIRED")
        else:
            print("Stock Sufficient")


while True:

    print("\n")
    print("================================")
    print(" INVENTORY MANAGEMENT SYSTEM")
    print("================================")

    print("1. Show Inventory")
    print("2. Sell Item")
    print("3. Add Stock")
    print("4. Forecast Demand")
    print("5. Calculate EOQ")
    print("6. Inventory Value")
    print("7. Low Stock Report")
    print("8. Reorder Point Report")
    print("9. Exit")

    choice = input("\nEnter Choice: ")

    if choice == "1":
        show_inventory()

    elif choice == "2":
        sell_item()

    elif choice == "3":
        add_stock()

    elif choice == "4":
        forecast_demand()

    elif choice == "5":
        calculate_eoq()

    elif choice == "6":
        inventory_value()

    elif choice == "7":
        low_stock_items()

    elif choice == "8":
        reorder_point_report()

    elif choice == "9":
        print("Exiting...")
        break

    else:
        print("Invalid Choice")
