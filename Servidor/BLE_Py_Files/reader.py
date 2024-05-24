import asyncio
from bleak import BleakClient

from DB_Py_Files.db_handler import DataPersister
from DB_Py_Files.json_parser import parse

MODEL_NBR_UUID = "FE41"

def async_read_wrapper(client, device, stop):
    asyncio.run(async_read(client, device, stop))
    
async def async_read(client: BleakClient, device, stop):
    device_name = device[0]
    db_handler = DataPersister()
    id_cliente = db_handler.insert_client('cliente1')
    if id_cliente is None:
        id_cliente = db_handler.insert_client('cliente1')
    db_handler.insert_disp(device[0], device[1], id_cliente)
    while not stop():
        obj = await reader(client)
        objParse = parse(obj)
        db_handler.insert_datos(objParse, device_name)
    await client.disconnect()

async def getClient(address):
    client = BleakClient(address)
    await client.connect()
    return client
    
async def reader(client):
    return await client.read_gatt_char(MODEL_NBR_UUID)