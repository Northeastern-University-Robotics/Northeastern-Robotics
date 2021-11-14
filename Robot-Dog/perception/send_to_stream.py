from streaming import Encoder, RTSPServer


if __name__ == '__main__':
    encoder = Encoder()
    server = RTSPServer()
    while True:
        data = encoder.read()
        server.send_data(data)
