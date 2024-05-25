import socket
import threading
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024
APPS_DIR = 'apps/'

applications = {app: os.path.join(APPS_DIR, app) for app in os.listdir(APPS_DIR) if app.endswith('.py')}

client_downloads = {}

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    while True:
        try:
            request = client_socket.recv(BUFFER_SIZE).decode()
            if not request:
                break

            command = request.split()[0]

            if command == 'LIST':
                app_list = "\n".join(applications.keys())
                client_socket.send(app_list.encode())

            elif command == 'DOWNLOAD':
                _, app_name = request.split()
                if app_name in applications:
                    file_path = applications[app_name]
                    file_size = os.path.getsize(file_path)
                    client_socket.send(f"SIZE {file_size}".encode())
                    client_socket.recv(BUFFER_SIZE)
                    with open(file_path, 'rb') as app_file:
                        while (chunk := app_file.read(BUFFER_SIZE)):
                            client_socket.send(chunk)
                    client_socket.send(b"DONE")
                    client_downloads.setdefault(client_address, []).append(app_name)
                else:
                    client_socket.send(f'ERROR: {app_name} not found.'.encode())

            elif command == 'UPDATE':
                _, app_name = request.split()
                if app_name in client_downloads.get(client_address, []):
                    file_path = applications[app_name]
                    file_size = os.path.getsize(file_path)
                    client_socket.send(f"SIZE {file_size}".encode())
                    client_socket.recv(BUFFER_SIZE)
                    with open(file_path, 'rb') as app_file:
                        while (chunk := app_file.read(BUFFER_SIZE)):
                            client_socket.send(chunk)
                    client_socket.send(b"DONE")
                else:
                    client_socket.send(f'ERROR: {app_name} not downloaded.'.encode())

            elif command == 'MY_APPS':
                downloaded_apps = client_downloads.get(client_address, [])
                app_list = "\n".join(downloaded_apps)
                client_socket.send(app_list.encode())

            else:
                client_socket.send('ERROR: Invalid command.'.encode())

        except Exception as e:
            print(f"[ERROR] {client_address} - {e}")
            break

    client_socket.close()
    print(f"[DISCONNECTED] {client_address} disconnected.")

def notify_clients(app_name):
    for client, apps in client_downloads.items():
        if app_name in apps:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(client)
                client_socket.send(f"UPDATE {app_name}".encode())
                file_path = applications[app_name]
                file_size = os.path.getsize(file_path)
                client_socket.send(f"SIZE {file_size}".encode())
                client_socket.recv(BUFFER_SIZE) 
                with open(file_path, 'rb') as app_file:
                    while (chunk := app_file.read(BUFFER_SIZE)):
                        client_socket.send(chunk)
                client_socket.send(b"DONE") 
                client_socket.close()
            except Exception as e:
                print(f"[ERROR] Notifying client {client}: {e}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == '__main__':
    threading.Thread(target=start_server).start()
