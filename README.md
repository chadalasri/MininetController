# MininetController
Network with Controller based on Mininet

NOTE: Because of a ‘Network Unreachable' error stemming from the untrusted host, the subnet mask had to be removed and the ip address had to be changed to ‘10.0.10.10’. 
NOTE: Also had to remove mac addresses.

Controller explanation:
	The controller works fairly simply:
Check the packet for IP and ARP traffic, non-IP traffic is flooded
If the packet is an IP packet, we assign it a port number to go out. The port number is based on the switch id (the switch the packet is received on) and the destination of the packet.
Once a port number has been computed, we check each of the IP protocols: ICMP, TCP and UDP traffic. We also keep track of each source and destination addresses.
Based on the protocol, the message is matched with different nw_protocols and then sent out the previously computed port number.
If the traffic is ICMP traffic, the source cannot be the untrusted host IP. Otherwise send.
If the traffic is TCP, if the source is the untrusted host IP then the destination cannot be the server 1 IP. Otherwise send.
If the traffic is UDP, if the source is the untrusted host IP then the destination cannot be the server 1 IP. Otherwise send.
