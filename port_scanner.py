# This program scans a specific range of TCP ports on a target PC and displays which ports accept connection(s).

import socket  # Allows applications to communicate on network interface via UDP or TCP
import concurrent.futures  # Asynchronously executes multiple tasks using pool of threads
import time  # Provides time-related functions (e.g., delays, time unit handling, clocks)

# Configuration
TARGET = "localhost"  # Target IP or domain (e.g., "127.0.0.1" or "website.com")
PORT_START = 1  # Starting port range
PORT_END = 1024  # Ending port range (e.g., 1024 for common ports, 65535 for all)
TIMEOUT = 1.0  # Timeout in seconds for each connection attempt
MAX_THREADS = 100  # Number of concurrent threads


def scan_port(target_ip, port):
    # Attempts to connect to a specific port on the target IP
    # Create a TCP socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)  # Sets socket to wait 1 sec before ending attempt
        # connect_ex returns 0 if the connection was successful
        result = s.connect_ex((target_ip, port))  # Creates var of result from TCP connection to IP and port
        if result == 0:  # Checks if connection was successful
            return port  # Returns port number if port is open
    return None  # Returns None if port not open


def main():
    try:
        # Resolve target hostname to IPv4 address
        target_ip = socket.gethostbyname(TARGET)  # Gets address of IP or domain
    except socket.gaierror:  # Error message in case address can't be found
        print(f"Error: Could not resolve hostname {TARGET}")  # Displays error message if invalid hostname input
        return  # Stops program if hostname can't be found

    print("-" * 50)  # Just a divider (purely aesthetic)
    print(f"Scanning Target: {target_ip} ({TARGET})")  # Displays IP and hostname of target
    print(f"Port Range     : {PORT_START} - {PORT_END}")  # Displays scanned port range
    print(f"Threads        : {MAX_THREADS}")  # Displays max number of worker threads
    print("-" * 50)  # Another divider

    start_time = time.time()  # Beginning time value = start time
    open_ports = []  # Creates list for found ports

    # Use ThreadPoolExecutor to run connection attempts concurrently
    ports_to_scan = range(PORT_START, PORT_END + 1)  # Creates a range containing every port to scan
    # Allows scanning of multiple ports concurrently from a pool of worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Maps the scan_port function across the target port range
        futures = {executor.submit(scan_port, target_ip, port): port for port in ports_to_scan}

        for future in concurrent.futures.as_completed(futures):  # Goes through each completed task (futures)
            port = future.result()  # Will be a port number if port is open
            if port is not None:  # If port is found - print message (just a double negative to say "if found")
                print(f"[+] Port {port} is OPEN")  # Displays open ports
                open_ports.append(port)  # Adds found open ports to list

    end_time = time.time()  # Gets ending time value from execution process
    duration = end_time - start_time  # Duration made from difference of end and start times

    print("-" * 50)  # Nothing important, just a divider
    print(f"Scan complete in {duration:.2f} seconds.")  # Displays time taken to execute port scan
    print(f"Total open ports found: {len(open_ports)}")  # Displays found open ports
    print("-" * 50)  # Another divider


# This format is used so the program isn't automatically ran when imported
if __name__ == "__main__":
    main()
