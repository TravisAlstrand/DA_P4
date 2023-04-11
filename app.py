from modules import models
from modules.csv_to_db import add_csv_to_db


if __name__ == "__main__":
    # create db
    models.Base.metadata.create_all(models.engine)
    # clean csvs / add to db
    add_csv_to_db()
