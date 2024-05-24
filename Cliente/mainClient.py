import json
import socket

from DB_Client_Files.data_type import data_type
from DB_Client_Files.db_handler import *


def connect_to_server():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(('localhost', 12345))
    return cliente_socket
    
def getDevicesFromServer():
    client_socket = connect_to_server()
    client_socket.sendall(b"1")
    devices = client_socket.recv(1024)
    devicesD = devices.decode()
    lista_dispositivos = json.loads(devicesD)
    disconnect_from_server(client_socket)
    lista_nombres = []
    if lista_dispositivos is not None:
        for n in lista_dispositivos:
            lista_nombres.append(n[0])
    return lista_nombres

def swapDevices(device):
    client_socket = connect_to_server()
    client_socket.sendall(b"2")
    respuesta = client_socket.recv(1024)
    print(respuesta.decode())
    client_socket.sendall(device.encode())
    disconnect_from_server(client_socket)
    
def stopService():
    client_socket = connect_to_server()
    client_socket.sendall(b"3")
    disconnect_from_server(client_socket)
    
def refreshData(device_name):
    db_handler = DataPersister()
    obj = db_handler.select_info(device_name)
    # data = data_type(obj)
    return obj

def disconnect_from_server(socket):
    socket.close()
