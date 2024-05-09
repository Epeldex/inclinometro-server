import random
from datetime import datetime
import psycopg2


class BaseDatabaseHandler:
    db_config = {
        'host': '127.0.0.1',
        'user': 'alex',
        'password': '123456',
        'dbname': 'rtu_prot_int'
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


class JsonParser:
    def parse_json(self, json_data):
        parsed_data = {}
        device_id, data = next(iter(json_data.items()))
        vals, ids = data['I2'][0]['Val'], data['I3']

        for id_val, val in zip(ids, vals[1:]):  # Skip the first value as it's a date
            parsed_data[id_val] = val  # Keep the value as-is (string or integer)

        parsed_data[0] = vals[0]  # The first value is the date
        return device_id, parsed_data


class DataPersister(BaseDatabaseHandler):
    def get_or_create(self, query, insert, data):
        self.cursor.execute(insert, data)
        self.conn.commit()
        self.cursor.execute(query, data)
        result = self.cursor.fetchone()
        return result[0]

    def persist_data(self, device_name, object_name, data):
        with self:
            dateSample = datetime.strptime(data.pop(0), '%m/%d/%Y %H:%M:%S UTC%z')
            device_id = self.get_or_create("SELECT id FROM devices WHERE name = %s",
                                           "INSERT INTO devices (name) VALUES (%s)",
                                           (device_name,))
            object_id = self.get_or_create(
                "SELECT id FROM objects WHERE name = %s AND packet_timestamp = %s AND device_id = %s",
                "INSERT INTO objects (name, packet_timestamp, device_id) VALUES (%s, %s, %s)",
                (object_name, dateSample, device_id,))

            for object_name, object_value in data.items():
                self.cursor.execute(
                    "INSERT INTO object_values (name, value, object_id) VALUES (%s, %s, %s)",
                    (object_name, object_value, object_id))
            self.conn.commit()


class DataFetcher(BaseDatabaseHandler):
    def fetch_data(self, device_name: str):
        with self:
            self.cursor.execute(
                'SELECT o.packet_timestamp, ov.name, ov.value'
                ' FROM devices d'
                ' JOIN objects o ON d.id = o.device_id'
                ' JOIN object_values ov ON o.id = ov.object_id'
                ' WHERE d.name = %s'
                , (device_name,))
            result = self.cursor.fetchall()

        return {
            'packet_timestamp': result[0][0],
            'device_name': device_name,
            'data': {row[1]: float(row[2]) / 100 for row in result}  # Convert to float and adjust as necessary
        }

    def fetch_all_devices(self):
        with self:
            self.cursor.execute("SELECT name FROM devices ORDER BY id DESC LIMIT 10")
            result = self.cursor.fetchall()
        return [row[0] for row in result]

    def fetch_rtu_data(self):
        return {
            'packet_timestamp': '2021-01-01 00:00:00',
            'device_name': 'RTU',
            'data': {
                'internal_temperature': random.randint(10, 50),
            }
        }
