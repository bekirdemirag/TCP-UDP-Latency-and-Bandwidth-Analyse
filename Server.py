import socket
import threading

def tcp_server(host='0.0.0.0', port=5000, buffer_size=8192):
    
    #TCP sunucu: Gelen bağlantıları kabul eder, veri alışverişini sağlar ve hataları yönetir.
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Maksimum 5 bağlantıyı dinle
        print(f"TCP server listening on {host}:{port}")
        
        while True:
            try:
                conn, addr = server_socket.accept()
                print(f"TCP Connection established with {addr}")
                
                while True:
                    try:
                        data = conn.recv(buffer_size)  # Tampon boyutuna göre veri al
                        if not data:
                            print(f"TCP Connection closed by {addr}")
                            break
                        
                        print(f"TCP: Received {len(data)} bytes from {addr}")
                        conn.sendall(data)  # Gelen veriyi aynen geri gönder
                    except ConnectionResetError:
                        print(f"TCP Connection reset by client {addr}")
                        break
                    except Exception as e:
                        print(f"TCP Error during data handling with {addr}: {e}")
                        break
                conn.close()
            except Exception as e:
                print(f"TCP Error accepting connection: {e}")
    except Exception as e:
        print(f"TCP Error in server setup: {e}")
    finally:
        server_socket.close()
        print("TCP Server shutdown.")

def udp_server(host='0.0.0.0', port=5001, buffer_size=8192):
    
    #UDP sunucu: Gelen verileri alır, veri alışverişini sağlar ve hataları yönetir.
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host, port))
        print(f"UDP server listening on {host}:{port}")
        
        while True:
            try:
                data, addr = server_socket.recvfrom(buffer_size)  # Tampon boyutuna göre veri al
                print(f"UDP: Received {len(data)} bytes from {addr}")
                server_socket.sendto(data, addr)  # Gelen veriyi aynen geri gönder
            except Exception as e:
                print(f"UDP Error during data handling with {addr}: {e}")
    except Exception as e:
        print(f"UDP Error in server setup: {e}")
    finally:
        server_socket.close()
        print("UDP Server shutdown.")

if __name__ == "__main__":
    try:

        # TCP ve UDP sunucularını ayrı thread'lerde çalıştırma
        
        tcp_thread = threading.Thread(target=tcp_server, args=('0.0.0.0', 5000, 8192))
        udp_thread = threading.Thread(target=udp_server, args=('0.0.0.0', 5001, 8192))
        
        tcp_thread.start()
        udp_thread.start()
        
        print("TCP and UDP servers are running...")
        
        tcp_thread.join()
        udp_thread.join()
    except KeyboardInterrupt:
        print("\nServer interrupted by user.")
