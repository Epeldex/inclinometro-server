import asyncio
import json
import socket
import threading

from BLE_Py_Files.discoverer import discover
from BLE_Py_Files.conector import connect_to_device
from BLE_Py_Files.reader import async_read_wrapper


async def main():
    thread = None
    devices = any
    conn: None
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(('localhost', 12345))
    servidor_socket.listen(1)
    while True:
        print('listening')
        conexion, direccion = servidor_socket.accept()
        print('client' + str(direccion) + 'accepted')
        stop = False
        election = conexion.recv(1024)
        option = election.decode()
        print(option)
        if option == "1":
            print('discovering')
            devices = await discoverer(conexion)
        if option == "2":
            conn = None
            if conn is not None:
                print('Stopping thread')
                await conn.disconnect()
                thread.join()
            conexion.sendall(b"ok")
            conn, device =  await swap_devices(conexion, devices)
            thread = threading.Thread(target=async_read_wrapper, args=(conn, device, lambda: stop))
            thread.start()
            print('reading' + str(device))
        if option == "3":
            print('Stopping thread')
            stop = True
            await conn.disconnect()
            thread.join()
        conexion.close()  
            
        
async def discoverer(conexion):
    devices = await discover()
    devices_json = json.dumps(devices)
    conexion.sendall(devices_json.encode())
    return devices

def swap_devices(conexion, devices):
    swap = conexion.recv(1024)
    swapD = swap.decode()
    return connect_to_device(swapD, devices)

if __name__ == '__main__':
    asyncio.run(main())