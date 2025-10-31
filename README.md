# DNS
DNS Client and Server Program in Python

## DNS Client & Server

This program contains a console-based DNS client and two DNS server programs.<br>
This program will mimic a simplified DNS system.<br>
Each of the programs will maintain its own resource record (RR) table, which is used to store DNS records.<br>
To send and receive records between programs UDP sockets are recommeded.<br>

## Program Details

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

In this project, we assume the user is at CSUSM campus.
This means the local DNS server is also the authoritative DNS server forCSUSM.
The Resource Record (RR) table contains 6 fields:
1. **Record number:** An integer starting from 0 and incrementing by 1 for each new record.
2. **Name:** The hostname or domain name.
3. **Type:** One of the 4 types (A, AAAA, CNAME, NS).
4. **Result:** The corresponding data for the given name and type.
5. **TTL** *(Time To Live)*: An integer for indicating how many more seconds this record will remain valid and stay in the RR table.
6. **Static:** This field indicates whether this record is
  - *Static (1)*: manually entered and remains valid, or
  - *Dynamic (0)*: automatically entered by the DNS program and will remain valid until the TTL reaches 0.
    - `This field is 0 for all entries in the client’s RR table in for this project`

The initial value for TTL should be 60 seconds.
Every second, both the client and local DNS server decrement the TTL fields of all Dynamic records on their RR tables.
Once the TTL reaches 0, the record will be removed from the RR table.
  Note that the TTL field of Static fields is always "None."
Each time a program responds to a request or receives a response, it will print its current RR table to the display.

This should be a comma separated table like the following example:
```
record_no,name,type,result,ttl,static
0,www.csusm.edu,A,144.37.5.45,None,1
```

The structure of DNS query and response contain the following fields.
1. Transaction_ID: (32 bits) The host assigns a unique Transaction ID to each DNS query, and temporarily stores the query until itreceives a response for it. The response should contain the same ID. When a host receives a DNS response, it fi rst checks whether itsID matches with the sent query and also the fl ags match the sent request. If yes, it removes the temporarily stored request and storesthe response in the RR table. We assume this fi eld is a 4-byte (32-bit) integer stored in binary format. Start from 0 and increment by 1for each new query.
2. Flag: (4 bits) Query (0000) or Response (0001).
3. Question:
  - (Name) A string containing the requested name.
  - Type: (4 bits) A (1000), AAAA (0100), CNAME (0010), NS (0001).
4. Answer:
  - (Name) A string containing the requested name.
  - Type: (4 bits) A (1000), AAAA (0100), CNAME (0010), NS (0001).
  - TTL: An integer indicating for how many more seconds this record will remain valid and stay in the RR table.
  - Result: A string containing the requested data.

If a record is not found, add “Record not found” in the result field.

The program receiving the response should handle this case by not including the record in its RR table.
The following shows the details of five test cases and the expected result for each test case.

The input prompt should be as follows:
Enter the hostname (or type 'quit' to exit) <hostname> <query type>
Note that the text <hostname> and <query type> are placeholders to show the order in which users can enter data and should not betyped out literally in the prompt.
Submission: Submit your report here. In the report, please detail your development process and testing results of 5 cases.
In case any ofyour program code is generated by GenAI tool, please specify them clearly in your code and report.
It is allowed to use GenAI tool in thisproject, but clear documentation is needed.




