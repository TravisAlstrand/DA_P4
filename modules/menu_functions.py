from modules.models import session, Product, Brand
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
        print("backup now!")
    elif choice == "Q":
        print("peace out!")
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
            print_error()
            print("""
            \nPlease choose one of the following options...
            \nV, N, A, B or Q.
            \n...
            """)
            time.sleep(2)


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
                print_error()
                print("\nSelection must be in the list")
                time.sleep(2)
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
            print_error()
            print("\nSelection must be a whole number")
            time.sleep(2)


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
            print_error()
            print("Name must contain at least one character")
            time.sleep(2)
    # price
    while True:
        try:
            price = input("\nPrice in Cents (ex: 299 = $2.99): ")
            price = clean_user_price(price)
            product.append(price)
            break
        except ValueError:
            print_error()
            print("\nPrice must be a whole number in cents")
            time.sleep(2)
    # quantity
    while True:
        try:
            quantity = input("\nQuantity: ")
            quantity = int(quantity)
            product.append(quantity)
            break
        except ValueError:
            print_error()
            print("\nQuantity must be a whole number")
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
            print_error()
            print("\nBrand Id must be a whole number")
            time.sleep(2)
        except Exception as e:
            print_error()
            print(e)
            time.sleep(2)
    build_new_product(product)


def build_new_product(product):
    # create / add product to db
    new_product = Product(product_name=product[0], product_price=product[1],
                          product_quantity=product[2], date_updated=product[3],
                          brand_id=product[4])
    


def clean_user_price(string):
    if "$" in string:
        string = string.replace("$", "")
    return int(string)


def unclean_date(date_object):
    return date_object.strftime("%m/%d/%Y")


def print_error():
    print("""
    \n>>>>>>>>>>>>>
    \n>>> ERROR >>>
    \n>>>>>>>>>>>>>
    """)
