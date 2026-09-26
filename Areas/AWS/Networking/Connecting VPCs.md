---
type: procedure
created: 2026-09-20
topic: AWS
confidence: 2
tags: [aws, networking]
---
# Connecting VPCs

> [!abstract] What this achieves
> Letting resources in two or more [[VPC]]s talk to each other over private IPs, either with **peering** (a direct link between two VPCs) or a **transit gateway** (a central hub).

**Needed first:** knowing how VPCs, subnets and route tables work → [[VPC]]

## Option 1: VPC peering

![[Pasted image 20260920155305.png]]

In the VPC console → **Peering connections** → Create. A simple form where I pick my VPC and the VPC to peer with:

![[Pasted image 20260920155420.png]]

> [!note] The other side has to **accept** the peering request (even if it's my own account).

![[Pasted image 20260920155716.png]]

![[Pasted image 20260920155819.png]]

**Then the part people forget: route tables.** The peering only creates the "cable". Each side still needs a route. Starting with VPC 1's route table:

![[Pasted image 20260920155931.png]]

![[Pasted image 20260920160057.png]]

> Add a route: **destination** = the other VPC's CIDR, **target** = Peering connection → pick the right one from the dropdown.

And the same on VPC 2's route table, with VPC 1's CIDR as the destination:

![[Pasted image 20260920160254.png]]

## Option 2: transit gateway

The more scalable way: a **transit gateway (TGW)**, a central router that all VPCs plug into.

VPC console → **Transit gateways** → Create:

![[Pasted image 20260920161731.png]]

<span style="color:rgb(255, 192, 0)"><b>ASN (Autonomous System Number):</b></span> a number that identifies an ==Autonomous System== (**AS**) on a network. Autonomous systems exchange routes with each other using **BGP** (Border Gateway Protocol). More in [[AS and BGP]].

> If I leave it blank, AWS picks a default private ASN (64512).

![[Pasted image 20260920184519.png]]

The transit gateway CIDR block is optional, and I can leave it blank.

### Attachments
> After creating the TGW, I have to **attach** each network to it: **Transit gateway attachments** tab in the VPC console.

![[Pasted image 20260920184844.png]]

The attachment creation form:
![[Pasted image 20260920185011.png]]

Attachment types: not just VPCs, but also VPNs, peering with other TGWs, Direct Connect, and <span style="color:rgb(192, 0, 0)">Connect</span>.

> [!question] What's a "Connect" attachment?
> From what I read: it's for plugging **SD-WAN / third-party network appliances** into the TGW, using GRE tunnels + BGP on top of an existing VPC or Direct Connect attachment. <span style="color:rgb(192, 0, 0)">Not studied yet.</span>

![[Pasted image 20260920185116.png]]

With the VPC type, I choose the VPC and the subnets (one per AZ) where the TGW gets a network interface:
![[Pasted image 20260920185421.png]]

> [!note] One attachment per network
> 3 VPCs connected to one transit gateway → **3 attachments**.

Then, again, **the route tables**. The attachment makes the connection possible, but each VPC still needs routes to the others, with target = **Transit gateway**:

![[Pasted image 20260920191008.png]]

## Peering vs transit gateway

| Feature | VPC peering | Transit gateway |
|---|---|---|
| Architecture | Direct 1-to-1 link | Central hub |
| Main purpose | Connect two VPCs | Connect many VPCs + on-prem networks |
| Transitive routing | ❌ No | ✅ Yes, through the TGW |
| Number of VPCs | A handful | Dozens to thousands |
| Management | One connection per pair | Central |
| Cross-region | ✅ Inter-region peering | ✅ TGW peering |
| On-premises | Needs extra architecture | VPN / Direct Connect attachments |
| Pricing | No hourly fee, only data transfer | Hourly per attachment + data processed |
| Routing control | VPC route tables | VPC route tables + TGW route tables |
| Complexity | Simple for a few VPCs | More pieces, but scales much better |

> [!important] The big difference: transitive routing
> <span style="color:rgb(255, 192, 0)">The most important concept here for the AWS Solutions Architect exam.</span>

### Peering is NOT transitive

```
VPC A ◄──────► VPC B ◄──────► VPC C
```

A↔B peered, B↔C peered. <span style="color:rgb(255, 192, 0)">Can A talk to C through B?</span> **No.**

A and C need their own peering:
```
VPC A ◄──────► VPC B
  ▲             │
  │             │
  └──► VPC C ◄──┘
```
With N VPCs, full mesh = N×(N-1)/2 peerings. With 10 VPCs that's 45! That's where the transit gateway wins.

## What if the VPCs have overlapping IP ranges?

| Situation | Possible solution |
|---|---|
| I control both VPCs and can redesign | Change the CIDR ranges (the real fix) |
| I only need access to one specific service | AWS PrivateLink |
| I need outbound access to an overlapping network | Private NAT gateway |
| HTTP/HTTPS only | An application proxy / gateway |
| Merging networks | A NAT / address-translation setup |
| Full two-way connectivity | Redesign the IPs, or a carefully engineered translation layer |

## Exam traps

**"A transit gateway automatically connects every VPC."**
<span style="color:rgb(255, 192, 0)">Not necessarily.</span> I still need VPC route tables, TGW route tables (propagation or static routes), and security groups / NACLs that allow the traffic.

**"VPC peering needs an internet gateway."**
<span style="color:rgb(255, 192, 0)">No.</span> Peering goes over AWS's private network. No IGW or NAT needed.

**"A transit gateway replaces the VPC route tables."**
<span style="color:rgb(255, 192, 0)">No.</span> Subnets still need a route pointing to the TGW:
```
Private subnet route table
──────────────────────────
10.2.0.0/16 → tgw-xxxxxxxx
```
The subnet sends traffic to the TGW, and the TGW uses its own route table to decide where it goes next.

**"Overlapping CIDRs are fine."**
<span style="color:rgb(255, 192, 0)">No.</span> Peering and TGW VPC attachments need **non-overlapping** ranges:
```
VPC A: 10.0.0.0/16
VPC B: 10.0.0.0/16   ← which 10.0.1.5 do you mean?
```

## Connects to
- [[VPC]]: route tables, CIDRs, subnets
- [[AS and BGP]]: the ASN on the transit gateway
- [[Lightsail]]: Lightsail's "VPC peering" checkbox is this same idea, done for me
- [[AWS Organizations]]: in multi-account setups, the TGW is usually shared across accounts
- Big picture → [[How AWS services connect]]

## Flashcards
#flashcards

Is VPC peering transitive? :: No. A↔B and B↔C does not give A↔C
What creates the peering "cable" vs what makes traffic flow? :: The peering connection is the cable. Routes in both VPCs' route tables make traffic flow
How many TGW attachments for 3 VPCs? :: 3, one per VPC
Can you peer VPCs with overlapping CIDRs? :: No
Does VPC peering need an internet gateway? :: No, it uses AWS's private network
Peering vs TGW pricing? :: Peering has no hourly fee (data transfer only). TGW charges per attachment-hour + per GB processed
