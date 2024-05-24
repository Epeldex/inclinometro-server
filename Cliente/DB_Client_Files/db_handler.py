import datetime
import psycopg2


class BaseDatabaseHandler:
    db_config = {
        'host': 'localhost',
        'user': 'alex',
        'password': '123456',
        'dbname': 'inclinometro'
    }

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

class DataPersister(BaseDatabaseHandler):
    def insert_data(self, insert):
        self.cursor.execute(insert)
        self.conn.commit()
        
    def select_one(self, select):
        self.cursor.execute(select)
        self.conn.commit()
        return self.cursor.fetchone()
        
    def select_info(self, device_name):
        with self:
            disp = self.select_one("SELECT da.inclinacion_mostrada, da.inclinacion_real, da.bateria, da.version_firmware, da.hold, da.abs, da.date FROM datos da INNER JOIN dispositivo dis ON da.id = dis.id WHERE dis.nombre_dispositivo = '{0}' ORDER BY da.id_datos DESC LIMIT 1".format(device_name))
            return disp