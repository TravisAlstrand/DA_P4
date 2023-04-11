from modules.models import Base, engine
from modules.csv_to_db import add_csv_to_db
from modules.menu_functions import menu_start


if __name__ == "__main__":
    # create db
    Base.metadata.create_all(engine)
    # clean csvs / add to db
    add_csv_to_db()
    # start the app
    menu_start()
