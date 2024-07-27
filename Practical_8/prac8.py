import os
import hashlib
import time
import socket

FTP_PORT = 21

def calculate_hash(file_path):
    with open(file_path, 'rb') as file:  
        file_hash = hashlib.md5()  
        while chunk := file.read(8192):  
            file_hash.update(chunk)  
    return file_hash.hexdigest()

def ftp_connect(host):
    ftp_socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    ftp_socket_connection.connect((host, FTP_PORT))  # Connect to the FTP server on the default port
    return ftp_socket_connection

def send_ftp_command(ftp_socket, command):
    ftp_socket.write(command + '\r\n')
    response = ftp_socket.readline().decode('utf-8')
    return response

def download_file_from_ftp(host, user, ftp_pass, remote_path, local_path):
    with ftp_connect(host) as ftp_socket:  # Establish FTP connection commands
        ftp_socket.sendall(('USER ' + user + '\r\n').encode('utf-8'))
        response = ftp_socket.recv(4096).decode('utf-8')
        print("Response after USER command:", response)
        ftp_socket.sendall(('PASS ' + ftp_pass + '\r\n').encode('utf-8'))
        response = ftp_socket.recv(4096).decode('utf-8')
        print("Response after PASS command:", response)
        ftp_socket.sendall(('TYPE I\r\n').encode('utf-8'))
        response = ftp_socket.recv(4096).decode('utf-8')
        print("Response after setting binary mode:", response)
        

        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new TCP socket for data transfer
        data_socket.bind(('127.0.0.1', 0))  # Binding
        data_socket.listen(1)  # Listen
        

        data_host, data_port = data_socket.getsockname()  # Get the host and port for the data socket
        port_cmd = 'PORT ' + ','.join(data_host.split('.')) + ',' + str(data_port // 256) + ',' + str(data_port % 256)
        ftp_socket.sendall((port_cmd + '\r\n').encode('utf-8'))  # Send command
        response = ftp_socket.recv(4096).decode('utf-8')
        print("Response after PORT command:", response)
        ftp_socket.sendall(('RETR ' + remote_path + '\r\n').encode('utf-8'))
        response = ftp_socket.recv(4096).decode('utf-8')
        print("Response after RETR command:", response)
        data_conn, _ = data_socket.accept()
        with open(local_path, 'wb') as local_file: 
            while True:
                data = data_conn.recv(8192)
                if not data: 
                    break
                local_file.write(data) 
        data_conn.close()
        data_socket.close()
        response = ftp_socket.recv(4096).decode('utf-8')
        print("Final response:", response)
        ftp_socket.sendall(('QUIT\r\n').encode('utf-8'))

def monitor_file(host, user, password, remote_path, local_path):
    while True:
        local_hash = calculate_hash(local_path)  # hash of the local file
        download_file_from_ftp(host, user, password, remote_path, local_path)  # Download 
        downloaded_hash = calculate_hash(local_path)  # hash of the downloaded file
        
        if local_hash != downloaded_hash:  # Check if the hashes are different
            print("Local file modified. Restoring known-good version...") 
        else:
            print("Local file is unchanged.")  

        time.sleep(10)  

def main():
    ftp_host = '127.0.0.1' 
    ftp_user = 'jarod' 
    ftp_pass = 'nbuser' 
    remote_path = '/help.txt' 
    local_path = 'help.txt'
    monitor_file(ftp_host, ftp_user, ftp_pass, remote_path, local_path) 

if __name__ == "__main__":
    main()  # Execute the main function
