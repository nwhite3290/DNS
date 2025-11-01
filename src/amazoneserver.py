
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
amazoneserver.py
Amazone DNS Server
Port: 22000
The Amazone DNS server handles requests from the local DNS server for Amazone-related requests.
This means it's an authoritative DNS server for Amazone.
It checks its own RR table for the request and sends the result/record to the local DNS server.
Then, it prints out its RR table.
"""

import errno
import socket
import sys
import json

# Wait for query
def listen():
    try:
		# Check RR table for record
        rr_table = RRTable()
        rr_table.add_record("shop.amazone.com", "A", "3.33.147.88", None, 1)
        rr_table.add_record("cloud.amazone.com", "A", "15.197.140.28", None, 1)
        amazone_dns_address = ("127.0.0.1", 22000)
        udp = UDPConnection()
        # bind socket
        udp.bind(amazone_dns_address)
        print("[AmazoneDNS] Server listening on port 22000")
        while True:
            data, address = udp.receive_message()
            query = deserialize(data)
            name = query["question_name"]
            record = rr_table.get_record(name)
            if record:
                response = {
                    "transaction_id": query["transaction_id"],
                    "flag": "0001",
                    "answer_name": name,
                    "answer_type": "A",
                    "ttl": 60,
                    "result": record["result"]
                }
            else:
                response = {
                    "transaction_id": query["transaction_id"],
                    "flag": "0001",
                    "answer_name": name,
                    "answer_type": "A",
                    "ttl": 0,
                    "result": "Record not found"
                }
            udp.send_message(serialize(response), address)
            # Display RR table
            rr_table.display_table()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting...")
    finally:
		# Close UDP socket
        udp.close()

# Bind address to UDP socket
def main():
    amazone_dns_address = ("127.0.0.1", 22000)
    listen()

# serialize function helps prepare data to send through the socket
def serialize(obj):
    return json.dumps(obj)
    
# deserialize function helps prepare data to be received from the socket
def deserialize(data):
    return json.loads(data)

# self.records = ?
class RRTable:
    def __init__(self):
		# create recors array
        self.records = []
        self.record_number = 0

	# initialize records array
    def add_record(self, name, type_, result, ttl, static):
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
        for record in self.records:
            if record["name"] == name:
                return record
        return None

	# Display the table in the following format (include the column names):
    def display_table(self):
		# record_number,name,type,result,ttl,static
        print("\nrecord_number,name,type,result,ttl,static")
        for record in self.records:
            print(f"{record['record_number']},{record['name']},{record['type']},{record['result']},{record['ttl']},{record['static']}")

#A class to manage DNS query types and their corresponding codes.
class DNSTypes:
    name_to_code = {
        "A": 0b1000,
        "AAAA": 0b0100,
        "CNAME": 0b0010,
        "NS": 0b0001,
    }
    code_to_name = {code: name for name, code in name_to_code.items()}

    @staticmethod
    # Gets the code for the given DNS query type name, or None
    def get_type_code(type_name: str):
        return DNSTypes.name_to_code.get(type_name, None)

    @staticmethod
    #Gets the DNS query type name for the given code, or Non
    def get_type_name(type_code: int):
        return DNSTypes.code_to_name.get(type_code, None)

#A class to handle UDP socket communication, capable of acting as both a client and a server
class UDPConnection:
	#Initializes the UDPConnection instance with a timeout. Defaults to 1
    def __init__(self, timeout: int = 1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        self.is_bound = False

	# Sends a message to the specified address
    def send_message(self, message: str, address: tuple[str, int]):
        self.socket.sendto(message.encode(), address)

	#Receives a message from the socket.
    def receive_message(self):
        while True:
            try:
                data, address = self.socket.recvfrom(4096)
                return data.decode(), address
            except socket.timeout:
                continue
            except OSError as e:
                if e.errno == errno.ECONNRESET:
                    print("Error: Unable to reach the other socket.")
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
