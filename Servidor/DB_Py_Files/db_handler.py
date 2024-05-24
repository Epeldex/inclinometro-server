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
        return self.cursor.fetchone()[0]
        
    def insert_client(self, client_name: str):
        with self:
            cliente = self.select_one("SELECT ID_CLIENTE FROM CLIENTE WHERE NOMBRE_CLIENTE = '{0}'".format(client_name))
            if cliente is None:
                self.insert_data("INSERT INTO cliente (NOMBRE_CLIENTE) VALUES ('{0}')".format(client_name))
            return cliente
    def insert_disp(self, disp_name, mac, client_id):
        with self:
            disp = self.select_one("SELECT * FROM dispositivo WHERE nombre_dispositivo = '{0}'".format(disp_name))
            if disp is None:
                self.insert_data("INSERT INTO dispositivo (NOMBRE_DISPOSITIVO, MAC, ID_CLIENTE) VALUES ('{0}', '{1}', '{2}')".format(disp_name, mac, client_id))
    def insert_datos(self, obj, nombre):
        with self:
            id_dispositivo = self.select_one("SELECT id FROM dispositivo WHERE nombre_dispositivo = '{0}'".format(nombre))
            self.insert_data("INSERT INTO datos (ID, INCLINACION_MOSTRADA, INCLINACION_REAL, BATERIA, VERSION_FIRMWARE, HOLD, ABS, DATE, TIME_STAMP) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(id_dispositivo, obj.inc_mostrada, obj.inc_real, obj.bateria, obj.firmware, obj.hold, obj.abs, obj.date, obj.timestamp))