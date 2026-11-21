#!/usr/bin/env python3

# file: app.py
# descr: enter manually or load data and administer inventory


from models import Base, session, Product, engine
from sqlite_CSV_backup import *
from datetime import datetime, date
import csv
import logging
import time
from pathlib import Path
import pdb

logging.basicConfig(level=logging.INFO)


logging.info("initial setup")


def initial_setup():
    while True:
        print("""
        ## INVENTORY SETUP ##

        1. Load Inventory from CSV
        2. Start new inventory
        3. Continue with existing inventory
        """)

        choice = input("Select an option: ").strip()
        if choice == "1":
            filename = input("CSV filename: ").strip()
            if not Path(filename).is_file():
                print("CSV file not found.")
                continue
            Base.metadata.create_all(engine)
            add_csv_to_db(filename)
            return "database"

        elif choice == "2":
            # can exit early when the filename already exists
            if new_csv_inventory():
                return "csv"

        elif choice == "3":
            Base.metadata.create_all(engine)
            print("Using existing inventory.")
            return "database"

        else:
            print("Invalid option.")


def selections_menu():
    while True:
        print("""
              \n
              \n## STORE INVENTORY ##
              \rSelect an option from the following letters:
              \rv) Enter v to view details of a single product by id.
              \ra) Enter a to add a new product.
              \rb) Enter b to make a backup of the database and export a new csv as backup.csv.
              \re) Press e to exit.""")
        user_interaction = input("Select v, a, b or e: ").lower().strip()
        if user_interaction in ["v", "a", "b", "e"]:
            return user_interaction
        else:
            input(
                "Wrong selection. Return to the main menu by pressing enter. Then enter only v, a, b or e: "
            )


def new_csv_inventory():
    filename = (
        input("New inventory filename [new_inventory.csv]: ").strip()
        or "new_inventory.csv"
    )

    if Path(filename).exists():
        print("File already exists. Choose another filename.")
        return False

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["product_name", "product_price", "product_quantity", "date_updated"]
        )
    print(f"\nNew inventory created: {filename}")

    while True:
        add_product_to_csv(filename)
        another = input("Add another product? (y/n): ").lower().strip()
        if another != "y":
            break
    return True


def add_product_to_csv(filename):
    while True:
        product_name = input("Product name: ").strip()

        if product_name:
            break
        print("Enter a value.")

    product_price = clean_price(input("Product price (Ex: 25.64): "))

    product_quantity = clean_quantity(input("Product quantity: "))

    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                product_name,
                f"${product_price / 100:.2f}",
                product_quantity,
                date.today().strftime("%m/%d/%Y"),
            ]
        )
    print(f"\nProduct '{product_name}' added successfully!\n")


def clean_id(id_string, options):
    try:
        id = int(id_string)
    except ValueError:
        input("""
              \n****** ID ERROR ******
              \rThe id should be a number without a symbol...
              \rEx: 1, 2, 3...
              \rPress Enter to return to the last menu... 
              \r**********************""")
        return
    else:
        if id in options:
            return id
        else:
            input(f"""
              \n****** ID ERROR ******
              \rOptions: {options}"
              \rPress Enter to return to the last menu... 
              \r**********************""")
            return


def clean_price(price_string_csv):
    while True:
        try:
            replace_m = price_string_csv.replace("$", "").strip()
            price_float = float(replace_m)
            return int(price_float * 100)
        except ValueError:
            price_string_csv = input("""
              \n***** PRICE ERROR *****
              \rThe price should be a number without a currency symbol...
              \rEx: 12.99
              \rTry again: """)


def clean_quantity(quantity_string):
    while True:
        try:
            quantity_string = quantity_string.strip().replace(",", ".")
            return float(quantity_string)
        except ValueError:
            quantity_string = input("""
              \n****** QUANTITY ERROR ********
              \rThe quantity should be a number without symbols
              \rEx: 1, 200
              \rTry again: """)


def clean_date(date_string_csv):
    """parse csv date strings"""
    while True:
        try:
            dt = datetime.strptime(date_string_csv, "%m/%d/%Y").date()
            return dt
        except ValueError:
            date_string_csv = input("""
              \n***** DATE ERROR *****
              \rThe date format should be MM/DD/YYYY.
              \rEx: 01/12/2003
              \rTry again: """)


def add_csv_to_db(filename):
    """import products from any file"""
    with open(filename, newline="") as csvfile:
        iter_gener = csv.DictReader(csvfile, delimiter=",")
        for row in iter_gener:
            no_dup_product_in_db = (
                session.query(Product)
                .filter(Product.product_name == row["product_name"])
                .one_or_none()
            )

            if no_dup_product_in_db is None:
                name = row["product_name"]
                price = clean_price(row["product_price"])
                quantity = clean_quantity(row["product_quantity"])
                date = clean_date(row["date_updated"])
                new_product = Product(
                    product_name=name,
                    product_price=price,
                    product_quantity=quantity,
                    date_updated=date,
                )
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        user_interaction = selections_menu()

        if user_interaction == "v":
            id_options = []
            for product in session.query(Product):
                id_options.append(product.id)
            id_error = True
            while id_error:
                id_choice = input(f"""
                      \nId Options: {id_options}...
                      \rProduct id: """)
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.id == id_choice).first()
            print(f"""
                  \nProduct name: {the_product.product_name}
                  \rProduct current price: ${the_product.product_price / 100}
                  \rProduct quantity: {the_product.product_quantity}
                  \rLast date updated: (YYYY-MM-DD): {the_product.date_updated}""")
            input("\nPress enter to return to the main menu()...")

        elif user_interaction == "a":
            # todo: add function
            while True:
                product_name = input("Product name: ").strip()
                if product_name:
                    break
                print("Enter a value...")
            product_price = clean_price(input("Product price (Ex: 25.53): "))
            product_quantity = clean_quantity(input("Product quantity: "))
            date_updated = datetime.now()
            breakpoint()
            new_product = Product(
                product_name=product_name,
                product_price=product_price,
                product_quantity=product_quantity,
                date_updated=date_updated,
            )
            session.add(new_product)
            session.commit()
            print(f"\nProduct '{product_name}' added successfully\n")
            time.sleep(1.5)

        elif user_interaction == "b":
            make_csv_backup_from_sqlite("inventory.db", "backup_csv.csv")

        else:
            print("\nGOODBYE")
            app_running = False


if __name__ == "__main__":
    setup_mode = initial_setup()
    if setup_mode == "database":
        app()
