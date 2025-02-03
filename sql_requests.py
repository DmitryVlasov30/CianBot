from json import load
from pathlib import Path
from sqlite3 import connect



with open("config.json") as data:
    information = load(data)
    path_to_db = Path(information["data_base_path"])
    name_main_table = information["name_main_table"]


def create_main_table(name_db=name_main_table):
    db = connect(path_to_db)
    curr = db.cursor()
    curr.execute(f"""
        CREATE TABLE IF NOT EXISTS {name_db} (
            "id"	INTEGER NOT NULL UNIQUE,
            "ads"   INTEGER NOT NULL UNIQUE,  
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    db.commit()
    db.close()


def new_information(id_ads: int):
    db = connect(path_to_db)
    curr = db.cursor()
    try:
        curr.execute(f"""
            INSERT INTO {name_main_table} (ads) VALUES
                (?)
        """, (id_ads,))
    except Exception as ex:
        print(ex)
    finally:
        db.commit()
        db.close()


def get_information() -> list[int]:
    db = connect(path_to_db)
    curr = db.cursor()
    try:
        curr.execute(f"""
            SELECT ads
            FROM {name_main_table}
        """)
        return list(map(lambda el: el[0], curr.fetchall()))
    except Exception:
        return [-1]
    finally:
        db.commit()
        db.close()


