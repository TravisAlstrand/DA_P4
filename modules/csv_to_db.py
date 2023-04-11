from modules import models
import csv


def add_csv_to_db():
    with open("./starter_csvs/brands.csv") as csv_brands:
        brand_data = csv.reader(csv_brands)
        # skip header line
        next(brand_data)
        for row in brand_data:
            # check if brand is already in db
            brand_already_in_db = models.session.query(models.Brand).filter(models.Brand.brand_name == row[0]).one_or_none()
            if brand_already_in_db is None:
                # if not in db, add it
                name = models.Brand(brand_name=row[0])
                models.session.add(name)
                models.session.commit()
            else:
                pass

    with open("./starter_csvs/inventory.csv") as csv_inventory:
        inv_data = csv.reader(csv_inventory)
        # skip header line
        next(inv_data)
        for row in inv_data:
            print(row)
            # check in product is already in db
            product_already_in_db = models.session.query(
                models.Product).filter(models.Product.product_name == row[0]).one_or_none()
            if product_already_in_db is None:
                # if not in db, add it
                build_product(row)
            else:
                # if in db, compare dates for newest
                if product_already_in_db.date_updated < clean_date(row[3]):
                    models.session.delete(product_already_in_db)
                    build_product(row)
                else:
                    pass
