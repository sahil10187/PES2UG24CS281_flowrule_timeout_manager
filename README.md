
---

# SDN Flow Rule Timeout Manager using POX and Mininet

![Python](https://img.shields.io/badge/Python-3-blue)
![Mininet](https://img.shields.io/badge/Mininet-Network%20Emulator-orange)
![POX](https://img.shields.io/badge/Controller-POX-green)
![OpenFlow](https://img.shields.io/badge/OpenFlow-1.0-red)

---

## Problem Statement

This project demonstrates flow rule lifecycle in Software Defined Networking (SDN) using a POX controller and Mininet.

The controller dynamically installs a drop rule with timeout, blocks traffic initially, and automatically restores communication after the rule expires.

---

## Objectives

* Demonstrate controller–switch interaction
* Implement match–action flow rules
* Show blocking and recovery behavior
* Observe flow lifecycle using timeout
* Analyze network performance using ping and iperf

---

## Topology

```
h1 ----\
        >---- s1 ---- Controller (POX)
h2 ----/
```

* Hosts: h1, h2
* Switch: s1 (Open vSwitch)
* Controller: POX
* Protocol: OpenFlow 1.0

---

## Setup Requirements

* Ubuntu (VM)
* Python 3
* Mininet
* POX Controller
* Open vSwitch

---

## Execution Steps

### 1. Start POX Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG timeout_manager
```

---

### 2. Start Mininet

```bash
sudo mn -c
sudo mn --topo single,2 --controller remote --switch ovsk
```

---

### 3. (Optional) Clear Previous Flows

```bash
mininet> dpctl del-flows
```

---

## Testing & Demonstration

### Scenario 1: Blocking Traffic

```bash
mininet> h1 ping -c 2 h2
```

Output:

* Destination Host Unreachable
* Controller log:

```
BLOCKING h1 TRAFFIC
```

---

### iperf during Blocking

```bash
mininet> h2 iperf -s &
mininet> h1 iperf -c h2
```

Observation:

* Connection fails or throughput is zero
* Traffic is blocked

---

## Wait for Timeout (~10 seconds)

Controller log:

```
FLOW EXPIRED
```

---

## Scenario 2: Recovery After Timeout

```bash
mininet> h1 ping -c 2 h2
```

Output:

* Successful ping (0% packet loss)

---

### iperf after Timeout

```bash
mininet> h2 iperf -s &
mininet> h1 iperf -c h2
```

Output:

* Non-zero throughput (~20+ Mbits/sec)

---

## Regression Test

```bash
mininet> dpctl del-flows
mininet> h1 ping -c 2 h2
(wait)
mininet> h1 ping -c 2 h2
```

---

## Flow Table Inspection

```bash
mininet> dpctl dump-flows
```

* Before timeout → drop rule present
* After timeout → rule removed

---

## Wireshark Analysis (Optional)

Filter:

```
icmp
```

* During blocking → request only
* After timeout → request + reply

---

## Key Concepts Used

* Software Defined Networking (SDN)
* OpenFlow Protocol
* Match–Action Flow Rules
* PacketIn / PacketOut
* Hard Timeout
* Flow Rule Lifecycle

---

## Conclusion

The project demonstrates how SDN controllers dynamically manage flow rules using timeout mechanisms. It shows how traffic can be controlled and restored automatically, improving network efficiency.

---

## Author

**Mohammed Sahil S**

---
