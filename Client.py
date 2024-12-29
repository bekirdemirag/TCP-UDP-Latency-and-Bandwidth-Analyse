import socket
import time
import matplotlib.pyplot as plt

def measure_performance(protocol, host, port, message_sizes, repetitions=100):
    """
    Farklı veri boyutlarında gecikme ve bant genişliği ölçer.
    """
    results = {"sizes": [], "latencies": [], "bandwidths": []}
    
    for message_size in message_sizes:
        message = b'x' * message_size
        if protocol == 'tcp':
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((host, port))
            except ConnectionRefusedError as e:
                print(f"Connection refused for size {message_size}: {e}")
                continue
        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            start_time = time.time()
            for _ in range(repetitions):
                if protocol == 'tcp':
                    client_socket.sendall(message)
                    data = client_socket.recv(message_size)
                else:
                    client_socket.sendto(message, (host, port))
                    data, addr = client_socket.recvfrom(message_size)
                if not data:
                    print(f"No response from {protocol.upper()} server for size {message_size}.")
                    break
            end_time = time.time()
            
            elapsed_time = end_time - start_time
            latency = elapsed_time / repetitions  # Ortalama gecikme
            bandwidth = (message_size * repetitions) / elapsed_time / 1024 / 1024  # MB/s
            
            results["sizes"].append(message_size)
            results["latencies"].append(latency * 1000)  # ms cinsine çevir
            results["bandwidths"].append(bandwidth)
        except Exception as e:
            print(f"Error for {protocol.upper()} with size {message_size}: {e}")
        finally:
            client_socket.close()
    
    return results

def plot_results_by_size(results, protocol):
    """
    Farklı veri boyutlarındaki sonuçları görselleştirir.
    """
    sizes = results["sizes"]
    latencies = results["latencies"]
    bandwidths = results["bandwidths"]
    
    # Latency Plot
    plt.figure()
    plt.plot(sizes, latencies, marker='o')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Latency (ms)')
    plt.title(f'{protocol.upper()} - Latency by Message Size')
    plt.grid()
    plt.show()
    
    # Bandwidth Plot
    plt.figure()
    plt.plot(sizes, bandwidths, marker='o')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Bandwidth (MB/s)')
    plt.title(f'{protocol.upper()} - Bandwidth by Message Size')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    protocol = input("Enter protocol (tcp/udp): ").strip().lower()
    host = '127.0.0.1'
    port = 5000 if protocol == 'tcp' else 5001
    message_sizes = [128, 512, 1024, 4096, 8192]  # Veri boyutları (bayt cinsinden)

    results = measure_performance(protocol, host, port, message_sizes)
    
    if results["sizes"]:
        print(f"Results for {protocol.upper()}:")
        for size, latency, bandwidth in zip(results["sizes"], results["latencies"], results["bandwidths"]):
            print(f"Size: {size} bytes - Latency: {latency:.2f} ms, Bandwidth: {bandwidth:.2f} MB/s")
        
        plot_results_by_size(results, protocol)
