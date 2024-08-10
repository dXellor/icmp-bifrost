```
_ ____ _   _ ___     ___  _ ____ ____ ____ ____ ___
| |    |\_/| |__] __ |__] | |___ |__/ |  | [__   |
| |___ |   | |       |__] | |    |  \ |__| ___]  |
                                                by dXellor
```

## About

Icmp-bifrost is a utility software that uses ICMP tunneling to bypass network limitations and firewall rules.

First, the network traffic of the **client** (runs the program in client mode) is encapsulated into the ICMP echo packet and then sent to the **server** (runs the program in server mode). There, the original packet is unwrapped from the ICMP data field and sent as **servers** own packet over the internet. The response is then encapsulated into the ICMP echo reply and sent to the **client**. The response is unwrapped and **client** receives it which completes the communication.

This software is part of my Bachelor's Thesis.

## Requirements

- Client and server machine on the same network (everything below applies for both of the machines)
- Access to the user with administrative privilages on the GNU/Linux operative system with `libnfnetlink` installed and a kernel version 2.6.14+
- Installed `python 3.x`
- Installed `iptables`

## How to run?

0. (Optional) Create python virtual environment with command `python -m venv env_name` or the tool of your choice. Activate the environment.

1. Install requirements with command `pip install -r requirements.txt`. If you encounter problems with the NetfilterQueue package check installation steps on its [README](https://github.com/oremanj/python-netfilterqueue)

2. Run the program with these commands:

- Client:
  ```bash
  sudo -E env PATH=$PATH python main.py -c -d server_address
  ```
- Server:
  ```bash
  sudo -E env PATH=$PATH python main.py -s -d client_address
  ```
- If you skipped **step 0** you can run script without passing the path environment variable (remove `-E env PATH=$PATH`)

## Licence

This project is [GPLv3 licenced](/LICENCE)
