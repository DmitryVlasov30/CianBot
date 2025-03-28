from json import load
from pathlib import Path
from sqlite3 import connect


class DataBase:
    def __init__(self, name_db):
        with open("config.json") as data:
            information = load(data)
            self.__PATH_TO_DB = Path(information["data_base_path"])
            self.__NAME_MAIN_TABLE = information["name_main_table"]

        self.create_main_table()

    def create_main_table(self):
        db = connect(self.__PATH_TO_DB)
        curr = db.cursor()
        curr.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__NAME_MAIN_TABLE} (
                "id"	INTEGER NOT NULL UNIQUE,
                "ads"   INTEGER NOT NULL UNIQUE,  
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """)
        db.commit()
        db.close()

    def new_information(self, id_ads: list[int]):
        db = connect(self.__PATH_TO_DB)
        curr = db.cursor()
        try:
            last_id = self.get_information()
            for id_el in id_ads:
                if id_el in last_id:
                    continue
                curr.execute(f"""
                    INSERT INTO {self.__NAME_MAIN_TABLE} (ads) VALUES
                        (?)
                """, (id_el,))
        except Exception as ex:
            print(ex)
        finally:
            db.commit()
            db.close()

    # noinspection PyBroadException
    def get_information(self) -> set[int]:
        db = connect(self.__PATH_TO_DB)
        curr = db.cursor()
        try:
            curr.execute(f"""
                SELECT ads
                FROM {self.__NAME_MAIN_TABLE}
            """)
            return set(map(lambda el: el[0], curr.fetchall()))
        except:
            res = set()
            res.add(-1)
            return res
        finally:
            db.commit()
            db.close()

    def get_path_db(self):
        return self.__PATH_TO_DB

    def get_name_table(self):
        return self.__NAME_MAIN_TABLE