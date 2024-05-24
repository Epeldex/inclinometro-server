
import json
from DB_Py_Files.data_type import data_type

def parse(byte_data):
    try:
        byte_string = byte_data.decode('latin1')
    except UnicodeDecodeError:
        print("Decodificación fallida. Intentando con otra codificación...")
        byte_string = byte_data.decode('cp1252')  # Otra codificación que puedes probar

    return assign_to_object(load_multi_json(byte_string)[0])
    
def parse_devices(devices):
    dispositivos = []
    for d in devices:
        nombre = d.name
        if nombre is not None and nombre[:3] == "LAN":
            address = d.address
            dispositivos.append((nombre, address))
    return dispositivos

def load_multi_json(line: str):
    if not line.strip():  # Verifica si la línea está vacía
        return []
    try:
        return [json.loads(line)]
    except json.JSONDecodeError as err:
        if err.msg == 'Extra data':
            pos = err.pos
            head = json.loads(line[:pos])
            tail = load_multi_json(line[pos:]) 
            return [head] + tail
        elif err.msg == 'Expecting value':
            return []
        else:
            raise err

def assign_to_object(obj):
    return data_type(obj.get('display'), obj.get('real'), obj.get('bat'), obj.get('vfw'), obj.get('hold'), obj.get('abs'), obj.get('date'))