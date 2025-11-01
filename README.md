

## DNS
DNS Client and Server Program in Python

### DNS Client & Server

This program contains a console-based DNS client and two DNS server programs.<br>
This program will mimic a simplified DNS system.<br>
Each of the programs will maintain its own resource record (RR) table, which is used to store DNS records.<br>
To send and receive records between programs UDP sockets are recommeded.<br>

### Program Details

 ***DNS Client:***<br>
`client.py`
```
The DNS client program allows users to look up info about hostnames/domains.
After receiving a hostname from users, it first checks its own RR table.
If the information is not found, the client asks the local DNS server.
When the client reveives a response from the local DNS server,
The result/record is stored/cached in the Clients RR table, then the updated table is displayed to the user console.
```

***Local DNS Server:***<br>
`localserver.p`<br>
`Port: 21000`
```
The local DNS server handles requests from the client.
It first checks its own RR table for the request.
If the information is not found, the Local DNS server quereries the Authoritative DNS server for the requested hostname/domain.
When the Local DNS server receives a response from the authoritative DNS server,
The result/record is stored in the Local RR table, sent to the client, and displays the updated table to the user console.
```

***Amazone DNS Server:***<br>
`amazoneserver.py`<br>
`Port: 22000`
```
The Amazone DNS server handles requests from the local DNS server for Amazone-related requests.
It is an Authoritative DNS server for Amazone. The Amazone DNS server checks its own RR table for the request.
The result/record is sent to the Local DNS server and displays its RR table to the user console.
```

##### Assume the user is at CSUSM campus

`The __Local DNS server__ is also the __Authoritative DNS server__ for **CSUSM**.`


## Sequence Diagram

![](./P2_DNSClientServer_SequenceDiaram.png)


### The Resource Record (RR) table contains 6 fields:

1. **Record number:** An integer starting from 0 and incrementing by 1 for each new record.
2. **Name:** The hostname or domain name.
3. **Type:** One of the 4 types (A, AAAA, CNAME, NS).
4. **Result:** The corresponding data for the given name and type.
5. **TTL** *(Time To Live)*: An integer for indicating how many more seconds this record will remain valid and stay in the RR table.
6. **Static:** This field indicates whether this record is
  - *Static (1)*: manually entered and remains valid, or
  - *Dynamic (0)*: automatically entered by the DNS program and will remain valid until the TTL reaches 0.
    - `This field is 0 for all entries in the client’s RR table in for this project`

#### The initial value for TTL should be 60 seconds.

```
- Every second, both the client and local DNS server decrement the TTL fields of all Dynamic records on their RR tables.
- Once the TTL reaches 0, the record will be removed from the RR table.
```
__Note:__ The `TTL field` of `Static fields` is always ***"None."***

Each time a program <u>responds to a request</u> or <u>receives a response</u>, it will <u>print its current RR table</u> to the display.

This should be a comma separated table like the following example:
```
record_no,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
```

### The structure of DNS query and response contain the following fields.

1. **Transaction_ID (32 bits):** The host assigns a unique Transaction ID to each DNS query, and temporarily stores the query until itreceives a response for it. The response should contain the same ID. When a host receives a DNS response, it fi rst checks whether its ID matches with the sent query and also the flags match the sent request. If yes, it removes the temporarily stored request and storesthe response in the RR table. We assume this fi eld is a 4-byte (32-bit) integer stored in binary format. Start from 0 and increment by 1for each new query.
2. **Flag (4 bits):** Query (0000) or Response (0001).
3. Question:
  * **(Name):** A string containing the requested name.
  * **Type (4 bits):** []A (1000), AAAA (0100), CNAME (0010), NS (0001).
4. Answer:
  * **(Name):** A string containing the requested name.
  * **Type (4 bits):** A (1000), AAAA (0100), CNAME (0010), NS (0001).
  * **TTL:** An integer indicating for how many more seconds this record will remain valid and stay in the RR table.
  * **Result:** A string containing the requested data.

#### If a record is not found:

Add **“Record not found”** in the result field.
The program receiving the response should not include the record in its RR table.

## Details of five test cases and the expected result for each test case.



- [x] <img src="./P2_DNSClientServer_Overview.png" alt="P2_DNSClientServer_Overview" style="zoom: 200%;" />






### Test your implementation
```
Before testing your implementation, ensure all programs are up and running.
Each program should only print its RR table when it handles a request or receives a response, as these tables wil be used to verfiy the test cases.
No other print statements are expected.

To the right are the initial states of the RR table for each program.
The user will interact with the client program throughout this process, and by default, the client program will send a type "A" query.
```
With the setup complete, here are the five test cases.


#### 1. Query www.csusm.edu for 1st time

**When the client requests info for www.csusm.edu, the local DNS should provide the correct response**.
To verify the test case, we will check the *RR tables* printed by the *client* and *local DNS server* after they handle the request.
If the client's RR table displays the correct information for www.csusm.edu in it's RR table, the query was completed successfully.
- [x] ***Does the client's RR table display the correct information for www.csusm.edu in the local DNS server's RR table?***


#### 2. Query www.csusm.edu for 2nd time

**Now that the client has cached the record for www.csusm.edu, if the user requests the same record again, the client should respond with the information it already has stored**.
Verify the test case by checking the *RR table* and observe the *TTL value* for the cached record has *decreased* over time.
This indicates that the information is being used from the cache, and the TTL coundown is in progress.
- [x] ***Has the TTL value for the cached record decreased over time?***


#### 3. Query shop.amazone.com for 1st time

**When the client requests info for shop.amazone.com, the local DNS will see it doesn't have the record.**
The *local DNS* wil parse the request to extract the *domain "amazone.com"* and find the *NS value* for that domain.
It will resoive the *IP address* for *dns.amazone.com* by finding its *'A'* record.
It will then use the *'A'* record to request the information from the *Amazone authoritative DNS server*.
When the response is received, the loca DNS will save the info and respond to the client.
- [x] ***Does the local DNS return the correct "shop.amazon.com" information?***


#### 4. Query shop.amazone.com after 60 sec

**When the client requests info for shop.amazone.com again after 60 seconds, the local DNS will see that it no longer has the record.**
The *local DNS* will need to repeat the process from the beginning.
After this process, both the *client* and *local DNS* will save the record with a valid *TTL*.
-	[x] ***Does the local DNS's record from shop.amazone.com time out after 60 seconds?***


#### 5. Query shop.amazone.com from client 2

**In the final test case, we are testing how the local DNS server handies requests from a new client.**
To simulate this, *start the client program again in a separate terminal* and make a request for *shop.amazone.com*.
Since the *local DNS* has already cached the record, it *should use the cached version* to respond to the *new client*.
- [x] *** Does the local DNS used the cached shop.amazone.com record to respond to the new client?***


### Final Comments

**The input prompt should be as follows:**

-  "Enter the hostname (or type 'quit' to exit):" <hostname> <query type>

```
Note that the text <hostname> and <query type> are placeholders.
They show the order in which users can enter data.
They should not be typed out literally in the prompt.
```

### Submission

Submit your report here.
In t

he report, please

- [x] detail your development process.
- [x] detail your testing results of 5 cases.

```
In case any of your program code is generated by GenAI tool, please specify them clearly in your code and report.
It is allowed to use GenAI tool in this project, but clear documentation is needed.
```

## Test Case Run Files

### clienttest.txt

```
Microsoft Windows [Version 10.0.26100.6899]
(c) Microsoft Corporation. All rights reserved.

S:\cs436\projects\p2\v8\runFolder>python3 client.py

Enter the hostname (or type 'quit' to exit): www.csusm.edu

[Client] Record found: www.csusm.edu ? 144.37.5.45

record_number, name, type, result, ttl,s tatic
0, www.csusm.edu, A, 144.37.5.45, 60, 0

Enter the hostname (or type 'quit' to exit): www.csusm.edu

[Client] Cached result: 144.37.5.45

record_number, name, type, result, ttl,s tatic
0, www.csusm.edu, A, 144.37.5.45, 53, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com

[Client] Record found: shop.amazone.com ? 3.33.147.88

record_number, name, type, result, ttl,s tatic
0, www.csusm.edu, A, 144.37.5.45, 38, 0
1, shop.amazone.com, A, 3.33.147.88, 60, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com

[Client] Cached result: 3.33.147.88

record_number, name, type, result, ttl,s tatic
0, www.csusm.edu, A, 144.37.5.45, 23, 0
1, shop.amazone.com, A, 3.33.147.88, 45, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com

[Client] Cached result: 3.33.147.88

record_number, name, type, result, ttl,s tatic
0, www.csusm.edu, A, 144.37.5.45, 17, 0
1, shop.amazone.com, A, 3.33.147.88, 39, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com

[Client] Cached result: 3.33.147.88

record_number, name, type, result, ttl,s tatic
1, shop.amazone.com, A, 3.33.147.88, 11, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com

[Client] Cached result: 3.33.147.88

record_number, name, type, result, ttl,s tatic
1, shop.amazone.com, A, 3.33.147.88, 4, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com


[Client] Record found: shop.amazone.com ? 3.33.147.88

record_number, name, type, result, ttl,s tatic
2, shop.amazone.com, A, 3.33.147.88, 60, 0

Enter the hostname (or type 'quit' to exit): shop.amazone.com

[Client] Record found: shop.amazone.com ? 3.33.147.88

record_number, name, type, result, ttl,s tatic
3, shop.amazone.com, A, 3.33.147.88, 60, 0

Enter the hostname (or type 'quit' to exit):
```


### localtest.txt

```
Microsoft Windows [Version 10.0.26100.6899]
(c) Microsoft Corporation. All rights reserved.

S:\cs436\projects\p2\v8\runFolder>python3 amazoneserver.py
[AmazoneDNS] Server listening on port 22000

record_number,name,type,result,ttl,static
0,shop.amazone.com,A,3.33.147.88,None,1
1,cloud.amazone.com,A,15.197.140.28,None,1

record_number,name,type,result,ttl,static
0,shop.amazone.com,A,3.33.147.88,None,1
1,cloud.amazone.com,A,15.197.140.28,None,1

record_number,name,type,result,ttl,static
0,shop.amazone.com,A,3.33.147.88,None,1
1,cloud.amazone.com,A,15.197.140.28,None,1
```


### amazonetest.txt

```
Microsoft Windows [Version 10.0.26100.6899]
(c) Microsoft Corporation. All rights reserved.

S:\cs436\projects\p2\v8\runFolder>python3 localserver.py
[LocalDNS] Server listening on port 21000

record_number,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
1,my.csusm.edu,A,144.37.5.150,None,1
2,amazone.com,NS,dns.amazone.com,None,1
3,dns.amazone.com,A,127.0.0.1,None,1
4,www.csusm.edu,A,144.37.5.45,None,1

record_number,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
1,my.csusm.edu,A,144.37.5.150,None,1
2,amazone.com,NS,dns.amazone.com,None,1
3,dns.amazone.com,A,127.0.0.1,None,1
4,www.csusm.edu,A,144.37.5.45,None,1
5,shop.amazone.com,A,3.33.147.88,60,0

record_number,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
1,my.csusm.edu,A,144.37.5.150,None,1
2,amazone.com,NS,dns.amazone.com,None,1
3,dns.amazone.com,A,127.0.0.1,None,1
4,www.csusm.edu,A,144.37.5.45,None,1
6,shop.amazone.com,A,3.33.147.88,60,0

record_number,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
1,my.csusm.edu,A,144.37.5.150,None,1
2,amazone.com,NS,dns.amazone.com,None,1
3,dns.amazone.com,A,127.0.0.1,None,1
4,www.csusm.edu,A,144.37.5.45,None,1
6,shop.amazone.com,A,3.33.147.88,10,0

record_number,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
1,my.csusm.edu,A,144.37.5.150,None,1
2,amazone.com,NS,dns.amazone.com,None,1
3,dns.amazone.com,A,127.0.0.1,None,1
4,www.csusm.edu,A,144.37.5.45,None,1
7,shop.amazone.com,A,3.33.147.88,60,0

```


### Client2test.txt

```
Microsoft Windows [Version 10.0.26100.6899]
(c) Microsoft Corporation. All rights reserved.

S:\cs436\projects\p2\v8\runFolder>python3 client2.py

Enter the hostname (or type 'quit' to exit): shop.amazone.com
[Client] Record found: shop.amazone.com ? 3.33.147.88
record_number, name, type, result, ttl,s tatic
0, shop.amazone.com, A, 3.33.147.88, 60, 0

Enter the hostname (or type 'quit' to exit):

```




## Python Source Code Files

### client.py


```python
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

```



### localserver.py


```python
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

```



### amazoneserver.sh


```python
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

```

