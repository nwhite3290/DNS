
"""
CS436 - Project 2
DNS Client & Server
Due: Friday, October 31, 2025 @11:59pm
Section: 4
Group: 5
Author: Nathan White
Author: Riley Glance
"""

"""
client.py
DNS Client
Port: N/A
The DNS client program allows users to look up info about hostnames/domains.
After receiving a hostname from users, it first checks its own RR table.
If it’s not found, it asks the local DNS server.
When it gets a response, it saves the result/record in its RR table
and then prints out its RR table.
"""
import errno
import socket
import sys
import threading
import time
import json

# Check RR table for record
def handle_request(hostname, transaction_id, udp, rr_table):
    local_dns_address = ("127.0.0.1", 21000)
    query = {
        "transaction_id": transaction_id,
        "flag": "0000",
        "question_name": hostname,
        "question_type": "A"
    }
    # The format of the DNS query and response is in the project description
    udp.send_message(serialize(query), local_dns_address)
    response_data, _ = udp.receive_message()
    response = deserialize(response_data)
    if response["result"] != "\nRecord not found:\n":
        rr_table.add_record(response["answer_name"], "A", response["result"], 60, 0)
        print(f"[Client] Record found: {response['answer_name']} → {response['result']}\n")
    else:
        print(f"[Client] Record not found for {hostname}\n")
	# Display RR table
    rr_table.display_table()

# query_code = DNSTypes.get_type_code("A")
# For extra credit, let users decide the query type (e.g. A, AAAA, NS, CNAME)
# This means input_value will be two values separated by a space
def main():
    rr_table = RRTable()
    udp = UDPConnection()
    transaction_id = 0
    try:
        while True:
            input_value = input("\nEnter the hostname (or type 'quit' to exit): ")
            if input_value.lower() == "quit":
                break
            hostname = input_value.strip()
            cached = rr_table.get_record(hostname)
            if cached:
                print(f"[Client] Cached result: {cached['result']}\n")
                rr_table.display_table()
            else:
                handle_request(hostname, transaction_id, udp, rr_table)
                transaction_id += 1
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting...")
    finally:
		# Close UDP socket
        udp.close()

# serialize function helps prepare data to send through the socket
def serialize(obj):
    return json.dumps(obj)

# deserialize function helps prepare data to be received from the socket
def deserialize(data):
    return json.loads(data)

# self.records = ?
class RRTable:
	# initialize self
    def __init__(self):
		# create recors array
        self.records = []
        self.record_number = 0
        # Start the background thread
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.__decrement_ttl, daemon=True)
        self.thread.start()

	# initialize records array
    def add_record(self, name, type_, result, ttl, static):
        with self.lock:
            record = {
                "record_number": self.record_number,
                "name": name,
                "type": type_,
                "result": result,
                "ttl": ttl,
                "static": static
            }
            self.records.append(record)
            self.record_number += 1

    def get_record(self, name):
        with self.lock:
            for record in self.records:
                if record["name"] == name:
                    return record
        return None

	 # Display the table in the following format (include the column names):
    def display_table(self):
        with self.lock:
			 # record_number,name,type,result,ttl,static
            print("\nrecord_number, name, type, result, ttl,s tatic")
            for record in self.records:
                print(f"{record['record_number']}, {record['name']}, {record['type']}, {record['result']}, {record['ttl']}, {record['static']}\n")

	# Decrement ttl
    def __decrement_ttl(self):
        while True:
            with self.lock:
                for record in list(self.records):
                    if record["ttl"] is not None and record["static"] == 0:
                        record["ttl"] -= 1
                        if record["ttl"] <= 0:
							#remove expired records
                            self.records.remove(record)
            time.sleep(1)

# A class to handle UDP socket communication, capable of acting as both a client and a server
class UDPConnection:
	# Initializes the UDPConnection instance with a timeout. Defaults to 1
    def __init__(self, timeout: int = 1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        self.is_bound = False

	# Sends a message to the specified address
    def send_message(self, message: str, address: tuple[str, int]):
        self.socket.sendto(message.encode(), address)

	# Receives a message from the socket.
    def receive_message(self):
        while True:
            try:
                data, address = self.socket.recvfrom(4096)
                return data.decode(), address
            except socket.timeout:
                continue
            except OSError as e:
                if e.errno == errno.ECONNRESET:
                    print("Error: Unable to reach the other socket.\n")
                else:
                    print(f"Socket error: {e}")
                self.close()
                sys.exit(1)
            except KeyboardInterrupt:
                raise

	# Binds the socket to the given address. This means it will be a server
    def bind(self, address: tuple[str, int]):
        if not self.is_bound:
            self.socket.bind(address)
            self.is_bound = True

	# Closes the UDP socket
    def close(self):
        self.socket.close()

if __name__ == "__main__":
    main()







