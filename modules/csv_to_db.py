from modules.models import session, Brand, Product
import csv
import datetime


# open / read csv files and clean / add them to db
def add_csv_to_db():
    with open("./starter_csvs/brands.csv") as csv_brands:
        brand_data = csv.reader(csv_brands)
        # skip header line
        next(brand_data)
        for row in brand_data:
            # check if brand is already in db
            brand_already_in_db = session.query(Brand). \
                filter(Brand.brand_name == row[0]).one_or_none()
            if brand_already_in_db is None:
                # if not in db, add it
                name = Brand(brand_name=row[0])
                session.add(name)
                session.commit()
            else:
                pass

    with open("./starter_csvs/inventory.csv") as csv_inventory:
        inv_data = csv.reader(csv_inventory)
        # skip header line
        next(inv_data)
        for row in inv_data:
            # check in product is already in db
            product_already_in_db = session.query(Product). \
                filter(Product.product_name == row[0]).one_or_none()
            if product_already_in_db is None:
                # if not in db, add it
                build_new_product(row)
            else:
                # if in db, compare dates for newest
                if product_already_in_db.date_updated < clean_csv_date(row[3]):
                    session.delete(product_already_in_db)
                    build_new_product(row)
                else:
                    pass
        session.commit()


def build_new_product(row):
    # prep new product data
    name = row[0]
    price = clean_csv_price(row[1])
    quantity = clean_csv_quantity(row[2])
    date = clean_csv_date(row[3])
    brand_id = session.query(Brand) \
        .filter(Brand.brand_name == row[4]).first().brand_id
    # create / add product to db
    new_product = Product(product_name=name, product_price=price,
                          product_quantity=quantity, date_updated=date,
                          brand_id=brand_id)
    session.add(new_product)


def clean_csv_price(string):
    reformatted = string.replace("$", "")
    price_float = float(reformatted)
    return int(price_float * 100)


def clean_csv_quantity(string):
    return int(string)


def clean_csv_date(string):
    split_string = string.split("/")
    month = int(split_string[0])
    day = int(split_string[1])
    year = int(split_string[2])
    return datetime.date(year, month, day)
