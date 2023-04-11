from modules.models import session, Product, Brand
import time


def menu_start():
    choice = welcome_menu()
    # view a product
    if choice == "V":
        view_product()
    elif choice == "N":
        print("add something")
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
                searched_product = session.query(Product). \
                    filter(Product.product_id == id_selection).first()
                product_brandname = session.query(Brand). \
                    filter(Brand.brand_id == searched_product.brand_id). \
                    first().brand_name
                print(f"""
                \nProduct Name: {searched_product.product_name}
                \nPrice: ${searched_product.product_price / 100}
                \nQuantity: {searched_product.product_quantity}
                \nDate Updated: {unclean_date(searched_product.date_updated)}
                \nBrand name: {product_brandname}
                \n...
                """)
                time.sleep(4)
                menu_start()
        except ValueError:
            print_error()
            print("\nSelection must be a whole number")
            time.sleep(2)


def unclean_date(date_object):
    return date_object.strftime("%m/%d/%Y")


def print_error():
    print("""
    \n>>>>>>>>>>>>>
    \n>>> ERROR >>>
    \n>>>>>>>>>>>>>
    """)
