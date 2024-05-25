import socket
import os
import subprocess

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024
DOWNLOAD_DIR = 'downloads/'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def request_list(client_socket):
    client_socket.send('LIST'.encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    print("Available applications:\n" + response)

def receive_file(client_socket, app_name):
    with open(os.path.join(DOWNLOAD_DIR, app_name), 'wb') as app_file:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if bytes_read.endswith(b'DONE'):
                app_file.write(bytes_read[:-4])  # fara DONE
                break
            app_file.write(bytes_read)

def download_app(client_socket, app_name):
    client_socket.send(f'DOWNLOAD {app_name}'.encode())
    size_response = client_socket.recv(BUFFER_SIZE).decode()
    if size_response.startswith("SIZE"):
        file_size = int(size_response.split()[1])
        client_socket.send(b"ACK")
        receive_file(client_socket, app_name)
        print(f'Downloaded {app_name}')
    else:
        print(size_response)

def update_app(client_socket, app_name):
    client_socket.send(f'UPDATE {app_name}'.encode())
    size_response = client_socket.recv(BUFFER_SIZE).decode()
    if size_response.startswith("SIZE"):
        file_size = int(size_response.split()[1])
        client_socket.send(b"ACK")
        receive_file(client_socket, app_name)
        print(f'Updated {app_name}')
    else:
        print(size_response)

def list_downloaded_apps():
    apps = os.listdir(DOWNLOAD_DIR)
    print("Downloaded applications:\n" + "\n".join(apps))

def execute_app(app_name):
    app_path = os.path.join(DOWNLOAD_DIR, app_name)
    if os.path.exists(app_path):
        subprocess.run(['python', app_path])
    else:
        print(f"Application {app_name} not found in downloads.")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    while True:
        command = input("Enter command (LIST, DOWNLOAD <app>, UPDATE <app>, MY_APPS, EXECUTE <app>, EXIT): ")
        if command == 'LIST':
            request_list(client_socket)
        elif command.startswith('DOWNLOAD'):
            _, app_name = command.split()
            download_app(client_socket, app_name)
        elif command.startswith('UPDATE'):
            _, app_name = command.split()
            update_app(client_socket, app_name)
        elif command == 'MY_APPS':
            list_downloaded_apps()
        elif command.startswith('EXECUTE'):
            _, app_name = command.split()
            execute_app(app_name)
        elif command == 'EXIT':
            client_socket.close()
            break
        else:
            print("Invalid command.")

if __name__ == '__main__':
    start_client()
