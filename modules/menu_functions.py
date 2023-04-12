from modules.models import session, Product, Brand
from modules.db_to_csv import backup_to_csv
from sqlalchemy import func
import datetime
import time


def menu_start():
    choice = welcome_menu()
    # view a product
    if choice == "V":
        view_product()
    # add a product
    elif choice == "N":
        add_product()
    elif choice == "A":
        build_analysis()
    elif choice == "B":
        print("\nCreating a backup file...")
        backup_to_csv()
        menu_start()
    elif choice == "Q":
        print("\nThanks for stopping by!")
        quit()


def welcome_menu():
    while True:
        print("""
        \n==================================
        \n======== Store Inventory =========
        \n==================================
        \n- View Single Product Details: (V)
        \n- Add a New Product: (N)
        \n- View an Analysis: (A)
        \n- Backup Entire Database: (B)
        \n- Quit: (Q)
        """)
        choice = input("\nWhat would you like to do? ").upper()
        if choice in ["V", "N", "A", "B", "Q"]:
            return choice
        else:
            print_error("""\nPlease choose one of the following options...
            \nV, N, A, B or Q.
            \n...""")


def view_product():
    product_ids = []
    for product in session.query(Product):
        product_ids.append(product.product_id)
    while True:
        id_selection = input(f"""
                            \nSelect an ID from the options below.
                            \nOptions: {product_ids}
                            \nProduct ID: """)
        try:
            id_selection = int(id_selection)
            if id_selection not in product_ids:
                print_error("Selection must be in the list")
            else:
                # if valid input, find product and display
                searched_product = session.query(Product). \
                    filter(Product.product_id == id_selection).first()
                product_brandname = session.query(Brand). \
                    filter(Brand.brand_id == searched_product.brand_id). \
                    first().brand_name
                print(f"""
                \nBrand name: {product_brandname}
                \nProduct Name: {searched_product.product_name}
                \nPrice: ${searched_product.product_price / 100}
                \nQuantity: {searched_product.product_quantity}
                \nDate Updated: {unclean_date(searched_product.date_updated)}
                \n...
                """)
                time.sleep(2)
                view_menu_2(searched_product)
        except ValueError:
            print_error("Selection must be a whole number")


def view_menu_2(product):
    while True:
        print(f"""
        \n===== Product Options =====
        \n- Edit this product: (E)
        \n- Delete this product: (D)
        \n- Return to Main menu: (R)
        """)
        view_choice = input("What would you like to do? ")
        if view_choice.upper() == "E":
            edit_product(product)
        elif view_choice.upper() == "D":
            delete_product(product.product_id)
        elif view_choice.upper() == "R":
            time.sleep(2)
            menu_start()
        else:
            print_error("""\nPlease choose one of the following options...
            \nE, D or R
            \n...""")
            continue


def edit_product(product):
    print("\n===== Edit Product =====")
    # name
    while True:
        new_name = input(f"""
                        \nOriginal name: {product.product_name}
                        \nEnter new name: """)
        if len(new_name) > 0:
            # check if product already exists
            product_already_in_db = session.query(Product). \
                filter(Product.product_name == new_name).one_or_none()
            if product_already_in_db is None or product_already_in_db == product:
                break
            else:
                print_error("Another product already has that name")
                continue
        else:
            print_error("Name must contain at least one character")
    # price
    while True:
        try:
            new_price = input(f"""
                             \nOriginal price: {product.product_price}
                             \nEnter new price in Cents (ex: 299 = $2.99): """)
            new_price = clean_user_price(new_price)
            break
        except ValueError:
            print_error("Price must be a whole number in cents")
    # quantity
    while True:
        try:
            new_quantity = input(f"""
                                \nOriginal quantity: {product.product_quantity}
                                \nEnter new quantity: """)
            new_quantity = int(new_quantity)
            break
        except ValueError:
            print_error("Quantity must be a whole number")
    # date
    new_date = datetime.date.today()
    # brand
    brands = session.query(Brand)
    brand_ids = []
    while True:
        print("")
        for brand_opt in brands:
            brand_ids.append(brand_opt.brand_id)
            print(f"ID: {brand_opt.brand_id} | Name: {brand_opt.brand_name}")
        print("\nSelect a Brand ID from the options above.")
        try:
            new_brand_selection = input(f"""
                                        \nOriginal Brand ID: {product.brand_id}
                                        \nEnter new Brand ID: """)
            new_brand_selection = int(new_brand_selection)
            if new_brand_selection not in brand_ids:
                raise Exception("\nSelection must be in the list")
            else:
                break
        except ValueError:
            print_error("Brand Id must be a whole number")
        except Exception as e:
            print_error(e)
    print("Updating product...")
    time.sleep(2)
    product.product_name = new_name
    product.product_price = new_price
    product.product_quantity = new_quantity
    product.date_updated = new_date
    product.brand_id = new_brand_selection
    session.commit()
    print("Product updated!")
    time.sleep(2)
    menu_start()


def add_product():
    product = []
    # name
    while True:
        name = input("\nProduct Name : ")
        if len(name) > 0:
            if name == "asdf":
                print("\nUggh... you're not even trying are you?...")
            product.append(name)
            break
        else:
            print_error("Name must contain at least one character")
    # price
    while True:
        try:
            price = input("\nPrice in Cents (ex: 299 = $2.99): ")
            price = clean_user_price(price)
            product.append(price)
            break
        except ValueError:
            print_error("Price must be a whole number in cents")
    # quantity
    while True:
        try:
            quantity = input("\nQuantity: ")
            quantity = int(quantity)
            product.append(quantity)
            break
        except ValueError:
            print_error("Quantity must be a whole number")
    # date
    date = datetime.date.today()
    product.append(date)
    # brand
    brands = session.query(Brand)
    brand_ids = []
    while True:
        print("")
        for brand in brands:
            brand_ids.append(brand.brand_id)
            print(f"ID: {brand.brand_id} | Name: {brand.brand_name}")
        print("\nSelect a Brand ID from the options above.")
        try:
            brand_selection = input("\nBrand ID: ")
            brand_selection = int(brand_selection)
            if brand_selection not in brand_ids:
                raise Exception("\nSelection must be in the list")
            else:
                product.append(brand_selection)
                break
        except ValueError:
            print_error("Brand Id must be a whole number")
        except Exception as e:
            print_error(e)
    build_new_product(product)


def build_new_product(product):
    # create / add product to db
    new_product = Product(product_name=product[0], product_price=product[1],
                          product_quantity=product[2], date_updated=product[3],
                          brand_id=product[4])
    # check if product already exists
    product_already_in_db = session.query(Product). \
        filter(Product.product_name == new_product.product_name).one_or_none()
    if product_already_in_db is None:
        session.add(new_product)
        session.commit()
        print(f"\nProduct '{new_product.product_name}' added!")
        time.sleep(2)
        menu_start()
    else:
        print(f"\nA product already exists with the name {new_product.product_name}")
        while True:
            edit_choice = input("Would you like to update it? (Y)/(N): ")
            if edit_choice.upper() == "N":
                print("\nOkie dokie!")
                time.sleep(2)
                menu_start()
            elif edit_choice.upper() == "Y":
                update_product(product_already_in_db, new_product)
                print(f"\nProduct '{new_product.product_name}' updated!")
                time.sleep(2)
                menu_start()
            else:
                print_error("Please enter a (Y) or an (N)")


def build_analysis():
    print("\nBuilding an analysis...")
    time.sleep(2)
    most_expensive = session.query(Product).order_by(Product.product_price.desc()).first()
    least_expensive = session.query(Product).order_by(Product.product_price.asc()).first()
    most_products = session.query(Brand).join(Product).group_by(Brand.brand_id). \
        order_by(func.count(Product.product_id).desc()).limit(1).first()
    average = session.query(func.avg(Product.product_price)).scalar()
    avg_price = "{:.2f}".format(average / 100)
    oldest_product = session.query(Product).order_by(Product.date_updated.asc()).first()
    newest_product = session.query(Product).order_by(Product.date_updated.desc()).first()
    print(f"""
        \n- Most expensive product: {most_expensive.product_name} - ${most_expensive.product_price / 100}
        \n- Least expensive product: {least_expensive.product_name} - ${least_expensive.product_price / 100}
        \n- Brand with most products: {most_products.brand_name} - {len(most_products.products)} products
        \n- Average cost of all products: ${avg_price}
        \n- Oldest product: {oldest_product.product_name} - {oldest_product.date_updated} (gross...)
        \n- Newest product: {newest_product.product_name} - {newest_product.date_updated}
        """)
    time.sleep(2)
    menu_start()


def delete_product(prod_id):
    print("\nDeleting product...")
    time.sleep(2)
    product = session.query(Product). \
        filter(Product.product_id == prod_id).first()
    session.delete(product)
    session.commit()
    print("\nProduct deleted!")
    time.sleep(2)
    menu_start()


def clean_user_price(string):
    if "$" in string:
        string = string.replace("$", "")
    return int(string)


def unclean_date(date_object):
    return date_object.strftime("%m/%d/%Y")


def update_product(og_product, new_product):
    og_product.product_name = new_product.product_name
    og_product.product_price = new_product.product_price
    og_product.product_quantity = new_product.product_quantity
    og_product.date_updated = new_product.date_updated
    og_product.brand_id = new_product.brand_id
    session.commit()


def print_error(error_message):
    print(f"""
    \n>>>>>>>>>>>>>
    \n>>> ERROR >>>
    \n>>>>>>>>>>>>>
    \n
    \n{error_message}
    \n
    """)
    time.sleep(2)
