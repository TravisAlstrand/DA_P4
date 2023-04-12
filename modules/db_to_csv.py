from modules.models import Brand, Product, session
import time
import csv


def backup_to_csv():
    with open("./csvs/backup_brands.csv", "w") as brands_csvfile:
        fieldnames = ["brand_name"]
        brands_writer = csv.DictWriter(brands_csvfile, fieldnames=fieldnames)
        brands_writer.writeheader()
        for brand in session.query(Brand):
            brands_writer.writerow({
                "brand_name": brand.brand_name
            })

    with open("./csvs/backup_inventory.csv", "w") as inv_csvfile:
        inv_fieldnames = ["product_name", "product_price", "product_quantity",
                          "date_updated", "brand_name"]
        inv_writer = csv.DictWriter(inv_csvfile, fieldnames=inv_fieldnames)
        inv_writer.writeheader()
        for product in session.query(Product):
            unclean_price = float(product.product_price / 100)
            unclean_date = product.date_updated.strftime("%m/%d/%Y")
            if unclean_date[3] == "0":
                unclean_date = unclean_date[:3] + unclean_date[4:]
            if unclean_date[0] =="0":
                unclean_date = unclean_date[1:]
            brand_to_add = session.query(Brand). \
                filter(Brand.brand_id == product.brand_id).first().brand_name
            inv_writer.writerow({
                "product_name": product.product_name,
                "product_price": "${0:.2f}".format(unclean_price),
                "product_quantity": product.product_quantity,
                "date_updated": unclean_date,
                "brand_name": brand_to_add
            })
    print("\nBackups created!")
    time.sleep(2)
