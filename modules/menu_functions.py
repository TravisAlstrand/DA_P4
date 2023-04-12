from modules.models import session, Product, Brand
from modules.db_to_csv import backup_to_csv
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
        print("analyze something")
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
                time.sleep(4)
                menu_start()
        except ValueError:
            print_error("Selection must be a whole number")


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
                raise Exception("\nSelection must in in the list")
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
    print(product)
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
