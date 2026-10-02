---
type: concept
created: 2026-09-27
topic: Networking
confidence: 1
tags: [networking, ip, subnetting, addressing]
aliases: [Subnetting, CIDR, Subnet mask, IPv4 address, VLSM, Route summarization]
---
# IP addressing and subnetting

> [!abstract] In one sentence
> An IPv4 address is **32 bits** split in two: a **network** part (which network am I on?) and a **host** part (which machine on it?). The **prefix length** (`/24`) or **subnet mask** (`255.255.255.0`) says where the split is. **Subnetting** is moving that split to cut a network into smaller ones, and everything else (routing, ARP vs gateway, firewall rules, cloud VPCs) depends on getting it right.

## The misconceptions I had

| I thought | Actually |
|---|---|
| An IP address identifies a machine | It identifies an **interface on a network**. A server with two NICs, a VPN and Docker has four or five IPs (see [[Network interfaces]]) |
| The mask is extra config next to the IP | The mask is **half the address's meaning**: `10.0.0.77/24` and `10.0.0.77/26` are on different networks, reach different neighbors directly, and send different traffic to the gateway |
| A `/24` gives me 256 machines | 254: the first address is the **network** and the last is the **broadcast** (and clouds keep a few more) |
| Any block can start anywhere | A block must start on a **multiple of its own size**. `10.0.0.64/25` isn't a valid network |

## What an address is

`192.168.10.77` is just a readable way to write 32 bits, 8 per number (an **octet**, 0–255):

```
192      .168      .10       .77
11000000 .10101000 .00001010 .01001101
```

Converting an octet: each bit is worth `128 64 32 16 8 4 2 1`. `77 = 64 + 8 + 4 + 1 = 01001101`. That table is the only thing I need to memorize, everything in subnetting comes back to it.

### Network part and host part

With `/26`, the first 26 bits are the **network**, the last 6 the **host**. The mask is 26 ones followed by 6 zeros:

```
address   11000000.10101000.00001010.01|001101   192.168.10.77
mask      11111111.11111111.11111111.11|000000   255.255.255.192   (/26)
          ─────────── network (26 bits) ───────┘└ host (6 bits)

AND       11000000.10101000.00001010.01|000000   192.168.10.64  → network address
host bits all 1s                    01|111111   192.168.10.127 → broadcast address
```

- **Network address** = address AND mask (host bits all 0): names the network, not assignable to a machine
- **Broadcast address** = host bits all 1: "everyone on this network"
- **Usable hosts** = 2^(host bits) − 2 = 2^6 − 2 = **62**, from `.65` to `.126`

## Why it works this way: a short history, one problem at a time

### 1. Classful addressing (1981): the split was fixed

The first byte decided the class, and the class decided the mask:

| Class | First bits | First octet | Default mask | Networks × hosts |
|---|---|---|---|---|
| A | `0` | 1–126 | `/8` | 126 × 16.7 M |
| B | `10` | 128–191 | `/16` | 16 k × 65 k |
| C | `110` | 192–223 | `/24` | 2 M × 254 |
| D | `1110` | 224–239 | — | Multicast |
| E | `1111` | 240–255 | — | Reserved |

**Problem:** a company with 300 machines is too big for a class C (254) and gets a class B: **65 534 addresses for 300 machines**. Addresses ran out fast, and every network needed its own route on the internet.

### 2. Subnetting and CIDR (1993): the split can go anywhere

**CIDR** (Classless Inter-Domain Routing) dropped classes: the prefix length is written explicitly and can be anything from `/0` to `/32`. The 300-machine company gets a `/23` (510 hosts). "Class C" survives only as slang for "a /24".

### 3. VLSM: different sizes inside one network

**Variable Length Subnet Masking**: cut one block into subnets of **different** sizes (a /25 for a big LAN, /30s for router links), instead of equal slices that waste space. See the design exercise below.

### 4. Summarization: fewer routes

If the subnets are **contiguous and aligned**, a router can advertise them as one bigger prefix. This is what keeps internet routing tables at ~1 million routes instead of billions (see [[AS and BGP]]).

### 5. Still not enough: private addresses and NAT, then IPv6

CIDR slowed the exhaustion but didn't stop it: private ranges + [[NAT and PAT|NAT]] became the norm, and IPv6 (128-bit addresses) is the long-term fix.

## Addresses with special meaning

| Range | Meaning | When I'll see it |
|---|---|---|
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | **Private** (RFC 1918), not routed on the internet | Every LAN, cloud network, container network |
| `100.64.0.0/10` | Shared space for **carrier-grade NAT** | Between an ISP and my router, Tailscale |
| `127.0.0.0/8` | **Loopback**, never leaves the machine | `127.0.0.1` = localhost |
| `169.254.0.0/16` | **Link-local** (APIPA): self-assigned when **DHCP failed** | A machine with `169.254.x.x` = "DHCP didn't answer". Clouds also put metadata services here (`169.254.169.254`) |
| `0.0.0.0/8` | "This network". `0.0.0.0` = "any address" when listening, "no address yet" in DHCP | `0.0.0.0:80` in `ss -tln` = listening on every interface |
| `0.0.0.0/0` | The **default route**: matches everything | Route tables, firewall rules |
| `224.0.0.0/4` | **Multicast** | Routing protocols, streaming, mDNS |
| `255.255.255.255` | Limited broadcast (this network only) | DHCP discovery |
| `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` | **Documentation** ranges, never used for real | Examples in docs (and in my notes) |
| `240.0.0.0/4` | Reserved (old class E) | Nowhere, in theory |

Two prefix lengths that break the "−2" rule:
- **`/31`**: 2 addresses, both usable, no network/broadcast. Made for **point-to-point links** between routers (RFC 3021)
- **`/32`**: a single address. Used for **host routes** ("route to exactly this IP") and in firewall rules ("only this IP")

## The prefix cheat sheet

| Prefix | Mask | Addresses | Usable hosts | Block size in the "interesting" octet |
|---|---|---|---|---|
| `/8` | `255.0.0.0` | 16 777 216 | 16 777 214 | 1st octet |
| `/16` | `255.255.0.0` | 65 536 | 65 534 | 2nd octet |
| `/20` | `255.255.240.0` | 4 096 | 4 094 | 16 (3rd octet) |
| `/21` | `255.255.248.0` | 2 048 | 2 046 | 8 (3rd) |
| `/22` | `255.255.252.0` | 1 024 | 1 022 | 4 (3rd) |
| `/23` | `255.255.254.0` | 512 | 510 | 2 (3rd) |
| `/24` | `255.255.255.0` | 256 | 254 | 1 (3rd) |
| `/25` | `255.255.255.128` | 128 | 126 | 128 (4th) |
| `/26` | `255.255.255.192` | 64 | 62 | 64 (4th) |
| `/27` | `255.255.255.224` | 32 | 30 | 32 (4th) |
| `/28` | `255.255.255.240` | 16 | 14 | 16 (4th) |
| `/29` | `255.255.255.248` | 8 | 6 | 8 (4th) |
| `/30` | `255.255.255.252` | 4 | 2 | 4 (4th) |
| `/31` | `255.255.255.254` | 2 | 2 (point-to-point) | 2 (4th) |
| `/32` | `255.255.255.255` | 1 | 1 (host route) | — |

Shortcuts: each +1 on the prefix **halves** the block. Mask octet values are only ever `0 128 192 224 240 248 252 254 255`.

## The method: subnetting in my head

For any `address/prefix`:
1. **Find the interesting octet**: the one where the mask isn't 255 or 0 (for `/20`: the 3rd)
2. **Block size** = 256 − mask value in that octet (`/20` → 256 − 240 = **16**)
3. **Network** = the largest multiple of the block size ≤ the address's value in that octet, all later octets 0
4. **Broadcast** = next network − 1 (later octets 255)
5. **Hosts** = network + 1 → broadcast − 1

**Worked example: `172.16.45.200/20`**
1. Interesting octet: 3rd (`255.255.240.0`)
2. Block: 256 − 240 = 16
3. Multiples of 16: 0, 16, 32, **48**… 45 falls in **32–47** → network `172.16.32.0`
4. Next network `172.16.48.0` → broadcast `172.16.47.255`
5. Hosts `172.16.32.1` → `172.16.47.254`, 4 094 of them

**Another: `10.0.0.77/27`** → 4th octet, block 32 → 64–95 → network `10.0.0.64`, broadcast `10.0.0.95`, hosts `.65`–`.94`.

## Why the mask decides where packets go

Every host makes one decision per packet (see [[Hubs, switches and routers#Stage 3: how a machine finds a MAC in the first place (ARP)]]):
- Destination **inside my subnet** (same network address with *my* mask) → ARP for it and send **directly**
- **Outside** → send to my **default gateway**

And routers pick the **most specific** matching prefix: a `/26` beats a `/24` beats `/0` ([[Routing tables|longest prefix match]]). So the mask isn't cosmetic: it's the input to both decisions.

### Advanced problem: two hosts, two different masks

Host A `192.168.1.10/24`, host B `192.168.1.200/25` (someone typed the wrong mask), gateway `192.168.1.254` for both.

- **A → B**: A computes `192.168.1.0/24`, B is inside → ARP, direct. ✅
- **B → A**: B computes its network as `192.168.1.128/25` (`.128`–`.255`). `.10` is **outside** → sends to the gateway, which sends it back onto the same LAN to A
- Result: requests go direct, replies go through the router. **Asymmetric routing.** Pings may work, but a stateful firewall on the gateway sees only half of each TCP conversation and drops it. Symptoms: "some things work from some machines", the worst kind of bug

Lesson: when connectivity is weird and partial, **check the masks on both ends** before anything else.

## Designing an address plan (VLSM)

**Task:** I have `192.168.10.0/24` and need: LAN A with 100 hosts, LAN B with 50, LAN C with 20, and 3 router-to-router links.

**Rule: allocate the biggest first.** Blocks must start on a multiple of their size, so placing big blocks first keeps them aligned without gaps.

| Need | Smallest fit | Subnet | Hosts range | Broadcast |
|---|---|---|---|---|
| LAN A, 100 hosts | `/25` (126) | `192.168.10.0/25` | `.1`–`.126` | `.127` |
| LAN B, 50 hosts | `/26` (62) | `192.168.10.128/26` | `.129`–`.190` | `.191` |
| LAN C, 20 hosts | `/27` (30) | `192.168.10.192/27` | `.193`–`.222` | `.223` |
| Link 1 | `/30` (2) | `192.168.10.224/30` | `.225`–`.226` | `.227` |
| Link 2 | `/30` | `192.168.10.228/30` | `.229`–`.230` | `.231` |
| Link 3 | `/30` | `192.168.10.232/30` | `.233`–`.234` | `.235` |
| Free | | `192.168.10.236` → `.255` | | |

If I'd placed LAN C first at `.0/27`, LAN A's `/25` could no longer start at `.0`, and would have to go to `.128`, leaving awkward holes.

### Summarization

Four branch networks `10.4.8.0/24`, `10.4.9.0/24`, `10.4.10.0/24`, `10.4.11.0/24`:
- In binary the 3rd octet is `000010|00`, `000010|01`, `000010|10`, `000010|11`: the first 22 bits are identical
- → one route: **`10.4.8.0/22`**

Conditions: the block count is a power of 2, and the first one is **aligned** (8 is a multiple of 4). `10.4.9.0`–`10.4.12.0` can't be summarized as one `/22`.

Over-summarizing is a real bug: advertising `10.4.0.0/16` when only `10.4.8.0/22` exists attracts traffic for addresses that don't exist, and the router drops it (a **blackhole**).

## Planning addresses in real life

What I'd keep in mind as a systems engineer, beyond the arithmetic:
- **Leave room**: a subnet that's full can't grow in place. Renumbering later is painful. Size for 2–3× today
- **Encode meaning** in the plan: e.g. `10.<site>.<vlan>.0/24`, so an address tells me where it is (see [[VLAN]])
- **Avoid the defaults everyone uses**: `192.168.0.0/24`, `192.168.1.0/24` (home routers), `10.0.0.0/16` (every tutorial), `172.17.0.0/16` (Docker). They collide the moment a VPN or a merger happens → [[Overlapping address spaces]]
- **Reserve ranges** for VPN client pools, future sites, container networks, and point-to-point links
- **Plan for summarization**: give each site a contiguous, aligned block so it's one route everywhere else
- **Document it** in an IPAM (IP address management) tool or at least one maintained file. Two teams picking "a free /24" from memory is how overlaps happen

## Tools

```bash
ipcalc 172.16.45.200/20          # network, broadcast, host range, mask
ip -4 addr show                  # my interfaces and their prefixes
ip route get 10.0.0.77           # which route and interface this destination uses
python3 -c "import ipaddress as i; n=i.ip_network('172.16.45.200/20', strict=False); print(n, n.broadcast_address, n.num_addresses)"
python3 -c "import ipaddress as i; print(list(i.collapse_addresses([i.ip_network(f'10.4.{x}.0/24') for x in range(8,12)])))"   # summarize
```

## In the cloud

Same arithmetic, a few extra rules. In AWS (see [[VPC]]):
- A VPC gets a CIDR between `/16` and `/28`, cut into subnets that each live in **one** availability zone
- AWS **reserves 5 addresses per subnet**: network, `+1` VPC router, `+2` DNS, `+3` reserved for future use, and the last one. A `/24` has **251** usable addresses, a `/28` only **11**
- VPCs that need to be connected (peering, transit gateway, VPN to an office) **must not overlap**, so the planning advice above applies across all accounts ([[Connecting VPCs]])
- Other clouds do similar things (Azure also reserves 5 per subnet, GCP 4), so check before sizing small subnets

## Practice

> [!example]- 1. `192.168.5.130/26`: network, broadcast, host range?
> Block 64 in the 4th octet → 128–191. Network `192.168.5.128`, broadcast `192.168.5.191`, hosts `.129`–`.190` (62).

> [!example]- 2. `10.10.77.5/21`: network, broadcast, number of hosts?
> `/21` = `255.255.248.0`, block 8 in the 3rd octet → 72–79. Network `10.10.72.0`, broadcast `10.10.79.255`, 2 046 hosts.

> [!example]- 3. Are `172.16.5.10/23` and `172.16.4.200/23` on the same subnet?
> `/23` = block 2 in the 3rd octet → 4–5. Both are in `172.16.4.0/23`: yes, they talk directly.

> [!example]- 4. Smallest prefix for 500 hosts? For 2 hosts on a router link?
> 500 → `/23` (510). A `/24` has only 254. Router link → `/30` (2 usable), or `/31` if both routers support it.

> [!example]- 5. Summarize `10.4.8.0/24` to `10.4.11.0/24`
> `10.4.8.0/22`: 4 networks (a power of 2), starting at 8 (a multiple of 4).

> [!example]- 6. A machine shows `169.254.33.7`. What happened?
> It asked for an address with DHCP, nobody answered, and it gave itself a link-local address. Check the DHCP server, the VLAN of the port, the cable.

> [!example]- 7. How many usable addresses in an AWS subnet `10.0.1.0/26`?
> 64 − 5 reserved = 59.

## Easy to get wrong
- Counting 256 hosts in a `/24` (254, or 251 in AWS)
- Writing a network with host bits set (`10.0.0.64/25`): the real network is `10.0.0.0/25`
- Forgetting that both ends must agree on the mask: a wrong mask on one host gives asymmetric, half-working connectivity
- Allocating small subnets first and leaving holes big blocks can't fit into
- Summarizing blocks that aren't aligned, or summarizing too wide and creating a blackhole
- Using `192.168.1.0/24` or `10.0.0.0/16` for anything that might ever connect to something else

## Related
- Foundation:: [[Network layers]], [[Number base conversion]] (binary, hex)
- Uses the mask:: [[Hubs, switches and routers]] (direct vs gateway), [[Routing tables]] (longest prefix match), [[ACL]]
- Running out of addresses:: [[NAT and PAT]], *[[IPv6]]*
- Planning problems:: [[Overlapping address spaces]], [[VLAN]]
- Applied:: [[VPC]], [[Connecting VPCs]], [[AS and BGP]] (summarization)

## Flashcards
#flashcards

What does the prefix length (/24) say? :: How many leading bits are the network part, the rest identify the host
How do you get the network address from an IP and a mask? :: Bitwise AND: all host bits set to 0
Broadcast address? :: All host bits set to 1
Usable hosts in a subnet? :: 2^(host bits) − 2 (network and broadcast)
Bit values of an octet? :: 128 64 32 16 8 4 2 1
Possible values of a mask octet? :: 0, 128, 192, 224, 240, 248, 252, 254, 255
Block size shortcut? :: 256 − the mask value in the interesting octet
Mask and hosts for /26, /27, /28, /29, /30? :: .192 (62), .224 (30), .240 (14), .248 (6), .252 (2)
Mask for /20, /21, /22, /23? :: 255.255.240.0, .248.0, .252.0, .254.0
What problem did CIDR solve? :: Classful masks wasted addresses (300 hosts got a class B of 65k), CIDR allows any prefix length
What is VLSM? :: Cutting one block into subnets of different sizes
Why allocate the largest subnets first? :: Blocks must start on a multiple of their size, big ones first keeps everything aligned without holes
Condition to summarize networks into one route? :: Contiguous, a power-of-2 count, and the first one aligned on the summary's block size
Risk of over-summarizing? :: Attracting traffic for addresses that don't exist → blackhole
What does a 169.254.x.x address mean? :: Link-local: DHCP failed and the machine assigned itself an address
What's special about /31 and /32? :: /31: 2 usable addresses for point-to-point links. /32: a single host (host routes, firewall rules)
What does 0.0.0.0/0 mean? :: The default route: matches every destination
Documentation IP ranges? :: 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24
How does a host decide between ARP and the gateway? :: Destination in my subnet (with my mask) → ARP directly. Otherwise → default gateway
Symptom of a wrong mask on one host? :: Asymmetric routing: requests direct, replies via the gateway, stateful firewalls drop, partial connectivity
How many addresses does AWS reserve per subnet? :: 5 (network, router, DNS, future, last)
Address ranges to avoid in a plan? :: 192.168.0/1.x, 10.0.0.0/16, 172.17.0.0/16: defaults that collide with homes, tutorials, Docker
