from BLE_Py_Files.reader import getClient


async def connect_to_device(device_name, devices):
    for i in range(len(devices)):
        if devices[i][0] == device_name:
            return await getClient(devices[i][1]), devices[i]