
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
localserver.py
Local DNS Server
Port: 21000
The local DNS server handles requests from the client.
It first checks its own RR table for the request.
If it’s not found, it asks the authoritative DNS server for the requested hostname/domain.
When it gets a response, the local DNS server saves the result/record in its RR table
and sends it to the client.
Then, it prints out its RR table.
"""

import errno
import socket
import sys
import threading
import time
import json

# Wait for query
def listen():
    try:
		# Check RR table for record
        rr_table = RRTable()
        rr_table.add_record("www.csusm.edu", "A", "144.37.5.45", None, 1)
		# When sending a query to the authoritative DNS server, use port 22000
        local_dns_address = ("127.0.0.1", 21000)
        amazone_dns_address = ("127.0.0.1", 22000)
        udp = UDPConnection()
        # Bind address to UDP socket called from main
        udp.bind(local_dns_address)
        print("[LocalDNS] Server listening on port 21000")
        while True:
            data, address = udp.receive_message()
            query = deserialize(data)
            hostname = query["question_name"]
            record = rr_table.get_record(hostname)
            # If record in table, respond immediately
            if record:
                response = {
                    "transaction_id": query["transaction_id"],
                    "flag": "0001",
                    "answer_name": hostname,
                    "answer_type": "A",
                    "ttl": record["ttl"] if record["ttl"] else 60,
                    "result": record["result"]
                }
            else:
                # Forward to authoritative server (amazone DNS)
                forward = UDPConnection()
                forward.send_message(data, amazone_dns_address)
                response_data, _ = forward.receive_message()
                response = deserialize(response_data)
                # Cache if found
                if response["result"] != "Record not found":
                    rr_table.add_record(response["answer_name"], "A", response["result"], 60, 0)
                forward.close()
            # Send back to client
            udp.send_message(serialize(response), address)
            rr_table.display_table()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting...")
    finally:
		# Close UDP socket
        udp.close()

# Add initial records found in the test cases diagram
def main():
	# Bind address to UDP socket
    listen()

# serialize function helps prepare data to send through the socket
def serialize(data):
    return json.dumps(data)

# deserialize function helps prepare data to be received from the socket
def deserialize(data):
    return json.loads(data)

# self.records = ?
class RRTable:
    def __init__(self):
		# create records array
        self.records = [
            {"record_number": 0, "name": "www.csusm.edu", "type": "A", "result": "144.37.5.45", "ttl": None, "static": 1},
            {"record_number": 1, "name": "my.csusm.edu", "type": "A", "result": "144.37.5.150", "ttl": None, "static": 1},
            {"record_number": 2, "name": "amazone.com", "type": "NS", "result": "dns.amazone.com", "ttl": None, "static": 1},
            {"record_number": 3, "name": "dns.amazone.com", "type": "A", "result": "127.0.0.1", "ttl": None, "static": 1},
        ]
        # create record_number object
        self.record_number = len(self.records)
        # Start the background thread
        self.lock = threading.Lock()
        threading.Thread(target=self.__decrement_ttl, daemon=True).start()

    def add_record(self, name, type_, result, ttl, static):
        with self.lock:
            self.records.append({
                "record_number": self.record_number,
                "name": name,
                "type": type_,
                "result": result,
                "ttl": ttl,
                "static": static
            })
            # record_number ++
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
            print("\nrecord_number,name,type,result,ttl,static")
            for record in self.records:
                print(f"{record['record_number']},{record['name']},{record['type']},{record['result']},{record['ttl']},{record['static']}")

	# This method is only called within a locked context
    def __decrement_ttl(self):
        while True:
            with self.lock:
                for record in list(self.records):
                    if record["static"] == 0 and record["ttl"] is not None:
						# Decrement ttl
                        record["ttl"] -= 1
                        if record["ttl"] <= 0:
							# Remove expired records
                            self.records.remove(record)
            time.sleep(1)

# A class to manage DNS query types and their corresponding codes.
class DNSTypes:
    name_to_code = {"A": 0b1000, "AAAA": 0b0100, "CNAME": 0b0010, "NS": 0b0001}
    code_to_name = {code: name for name, code in name_to_code.items()}

    @staticmethod
    # Gets the code for the given DNS query type name, or None
    def get_type_code(type_name: str):
        return DNSTypes.name_to_code.get(type_name, None)

    @staticmethod
	# Gets the DNS query type name for the given code, or None
    def get_type_name(type_code: int):
        return DNSTypes.code_to_name.get(type_code, None)

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
