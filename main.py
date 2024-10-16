import socket


HOST = '127.0.0.1'
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Proxy server running on {HOST}:{PORT}")

def handle_client(client_socket):
    request = client_socket.recv(4096)

    try:
        request_lines = request.decode().splitlines()
        first_line = request_lines[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((webserver, port))

        proxy_socket.send(request)

        while True:
            response = proxy_socket.recv(4096)
            if len(response) > 0:
                client_socket.send(response)
            else:
                break

        proxy_socket.close()
        client_socket.close()
    except Exception as e:
        print(f"Error handling request: {e}")
        client_socket.close()


while True:

    client_socket, addr = server_socket.accept()
    print(f"Received connection from {addr}")
    handle_client(client_socket)
