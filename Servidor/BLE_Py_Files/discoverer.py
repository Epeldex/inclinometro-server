from bleak import BleakScanner
from DB_Py_Files.json_parser import parse_devices

async def discover_devices():
    return await BleakScanner.discover()

async def discover():
    
        parsed_devices =  parse_devices(await discover_devices())
        if parsed_devices:
            return parsed_devices