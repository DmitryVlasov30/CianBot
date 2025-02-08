from json import load
from pathlib import Path
from sqlite3 import connect



with open("config.json") as data:
    information = load(data)
    PATH_TO_DB = Path(information["data_base_path"])
    NAME_MAIN_TABLE = information["name_main_table"]


def create_main_table(name_db=NAME_MAIN_TABLE):
    db = connect(PATH_TO_DB)
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


def new_information(id_ads: list[int]):
    db = connect(PATH_TO_DB)
    curr = db.cursor()
    try:
        last_id = get_information()
        for id_el in id_ads:
            if id_el in last_id:
                continue
            curr.execute(f"""
                INSERT INTO {NAME_MAIN_TABLE} (ads) VALUES
                    (?)
            """, (id_el,))
    except Exception as ex:
        print(ex)
    finally:
        db.commit()
        db.close()


# noinspection PyBroadException
def get_information() -> set[int]:
    db = connect(PATH_TO_DB)
    curr = db.cursor()
    try:
        curr.execute(f"""
            SELECT ads
            FROM {NAME_MAIN_TABLE}
        """)
        return set(map(lambda el: el[0], curr.fetchall()))
    except:
        res = set()
        res.add(-1)
        return res
    finally:
        db.commit()
        db.close()