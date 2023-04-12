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
    print("\nBackup created!")
    time.sleep(2)
