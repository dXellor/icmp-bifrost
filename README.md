```
_ ____ _   _ ___     ___  _ ____ ____ ____ ____ ___
| |    |\_/| |__] __ |__] | |___ |__/ |  | [__   |
| |___ |   | |       |__] | |    |  \ |__| ___]  |
                                                by dXellor
```

## About

Icmp-bifrost is a utility software that uses ICMP tunneling to bypass network limitations and firewall rules.

![icmp-bifrost example diagram](/docs/example-diagram.png)

## Requirements

- Client and server machine (everything below applies for both of the machines). This setup assumes client and server are on the same network.
- Access to the user with administrative privilages on the GNU/Linux operative system with `libnfnetlink` installed and a kernel version 2.6.14+
- Installed `python 3.x`
- Installed `iptables`

## How to run?

0. (Optional) Create python virtual environment with command `python -m venv env_name` or the tool of your choice. Activate the environment.

1. On the client machine set **net.ipv4.icmp_echo_ignore_all=1** by editing `/etc/sysctl.conf`. After that refresh configuration with `sysctl -p`

2. On the server machine set **net.ipv4.icmp_echo_ignore_all=1** and **net.ipv4.ip_forward=1** by editing `/etc/sysctl.conf`. After that refresh configuration with `sysctl -p`

3. Install requirements with command `pip install -r requirements.txt`. If you encounter problems with the NetfilterQueue package check installation steps on its [README](https://github.com/oremanj/python-netfilterqueue)

4. Run the program with these commands:

- Client:
  ```bash
  sudo -E env PATH=$PATH python main.py -c -d server_address
  ```
- Server:
  ```bash
  sudo -E env PATH=$PATH python main.py -s -d client_address -i default_gateway_interface
  ```
- If you skipped **step 0** you can run script without passing the path environment variable (remove `-E env PATH=$PATH`)

## Licence

This project is [GPLv3 licenced](/LICENCE)
