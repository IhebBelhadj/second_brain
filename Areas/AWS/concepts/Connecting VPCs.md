---
type: note
created: 2026-09-20
topic:
tags: []
---
# How to connect multiple VPCs

### The standard Peering connection option in the VPC service

![[Pasted image 20260920155305.png]]

In the VPC service on AWS there is the option for ==Peering connections== , you'll be prompted with this form : 

![[Pasted image 20260920155420.png]]

its a simple form where you select the local vpc and the other VPC to peer with (nothing fancy here)

> Note: in this case the VPC to peer with should accept the peering connection request

![[Pasted image 20260920155716.png]]

![[Pasted image 20260920155819.png]]

after that you would need to udate the route table lets pick the route table for VPC 1 to do the setup : 
![[Pasted image 20260920155931.png]]

![[Pasted image 20260920160057.png]]

> we need to add a new connection to the route table with the destination being the other VPC's IP range with the connection type being a peering connection and select the adequate peering connection from the dropdown

we will do the same with the VPC-2 route table where we will put a destination with the first VPC's IP range with the adequate peering connection as well 

![[Pasted image 20260920160254.png]]

### Transitive routing
Here is another more robust way to connect VPCs toghether which is to use a ==transitive gateway==

In the VPC service you will find the transit gateways section where you can create a transit gateway. Here is the transit gateway creation form : 

![[Pasted image 20260920161731.png]]

<span style="color:rgb(255, 192, 0)"><b>ASN (Amazon Autonomous System Number):</b> </span> 



## Comparision VPC peering VS transit routing 

| Feature                   | VPC Peering                                           | Transit Gateway                                             |
| ------------------------- | ----------------------------------------------------- | ----------------------------------------------------------- |
| Architecture              | Direct connection                                     | Centralized hub                                             |
| Main purpose              | Connect two VPCs                                      | Connect multiple VPCs and networks                          |
| Transitive routing        | ❌ No                                                  | ✅ Yes, through the TGW                                      |
| Number of VPCs            | Suitable for a small number                           | Suitable for larger networks                                |
| Management                | Configure each peering connection                     | Centralized routing management                              |
| Cross-Region connectivity | ✅ Yes, using inter-Region peering                     | ✅ Yes, using supported inter-Region TGW peering             |
| On-premises connectivity  | Requires additional networking architecture           | Can connect through VPN or Direct Connect attachments       |
| Pricing                   | No hourly peering charge; data transfer charges apply | Hourly attachment charges and data processing charges apply |
| Routing control           | VPC route tables                                      | VPC route tables + TGW route tables                         |
| Network isolation         | Through VPC routing and security controls             | Through routing domains and TGW route tables                |
| Complexity                | Simple for a few VPCs                                 | More components, but easier to scale                        |

## What would you do in the case you want to connect overlapping IP ranges of VPCs

| Situation                                                              | Potential solution                                                            |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| You control both VPCs and can redesign them                            | Change CIDR ranges                                                            |
| You only need access to a specific service                             | AWS PrivateLink                                                               |
| You need outbound connectivity to an overlapping network               | Private NAT Gateway, if the architecture supports it                          |
| You need HTTP/HTTPS communication                                      | Application proxy or gateway                                                  |
| You are merging networks with overlapping addresses                    | NAT appliance or address-translation architecture                             |
| You need full, bidirectional connectivity between overlapping networks | Redesign the IP ranges or use a carefully engineered translation architecture |