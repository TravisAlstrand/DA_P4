from models import session, Product
import csv


def add_csv_to_db():
    with open("../starter_csvs/inventory.csv") as csv_inventory:
        inv_data = csv.reader(csv_inventory)
        # skip header line
        next(inv_data)
        for row in inv_data:
            print(row)
            # check in product is already in db
            # product_already_in_db = session.query(
            #     Product).filter(product_name=row[0]).one_or_none()
            # if product_already_in_db == None:
            #     # if not in db, add it
            #     build_product(row)
            # else:
            #     # if in db, compare dates for newest
            #     if product_already_in_db.date_updated < clean_date(row[3]):
            #         session.delete(product_already_in_db)
            #         build_product(row)
            #     else:
            #         pass
