# MITMsmtp
MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login credentials and mails sent over plain or SSL/TLS encrypted connections. The idea is to catch sensitive emails sent by clients which are not correctly verifying the SMTP servers identity in SSL/TLS mode. MITMsmtp will catch username and password as well as the message itself. This way you might gain access to a companies mail server or catch information like password reset tokens or verification links sent by applications. Using those information you might gain more and more access to a system.

MITMsmtp offers a command line tool as well as an open Python3 API which can be used to build own tools for automated pentesting of applications.

## Compatibility
MITMsmtp has been tested against the SMTP client of Thunderbird 60.5.3 and some other SMTP clients.

### Connection Security
MITMsmtp supports the following connection security modes:
* Plaintext
* SSL/TLS
* STARTTLS (under development, not yet working)

### Login Methods
MITMsmtp supports the following login methods:
* PLAIN
* LOGIN (under development, not yet working)

Other methods are not supported as we want to extract the cleartext password. As this might be a problem for restrictive clients, it is planned to add support for MD5 later. However NTLM or Kerberos can't be supported as these methods require the server to know the cleartext password.

## Setup
MITMsmtp requires Python3 and setuptools. You might want to install git as well. Use the following command on Debian:

`apt install python3 python3-setuptools git`

Now just clone the MITMsmtp repository:

`git clone https://github.com/RobinMeis/MITMsmtp.git`

Change into MITMsmtp directory and start the installation:

`sudo python3 setup.py install`

That's it!

### Updating
`git pull`

`sudo python3 setup.py install`

## Usage
*This section describes the command line usage. For the API reference, please refere to API section.*

Running `MITMsmtp --help` will give you an overview about the available command line switches:
```
usage: MITMsmtp [-h] [--server_address SERVER_ADDRESS] [--port PORT]
                [--SSL SSL] [--certfile CERTFILE] [--keyfile KEYFILE]
                [--log LOG]

MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login
credentials and mails sent over plain or SSL encrypted connections.

optional arguments:
  -h, --help            show this help message and exit
  --server_address SERVER_ADDRESS
                        IP Address to listen on (default: all)
  --port PORT           Port to listen on (default: 8587)
  --SSL SSL             Enables SSL Support (default: False)
  --certfile CERTFILE   Certfificate for SSL Mode
  --keyfile KEYFILE     Key for SSL Mode
  --log LOG             Directory for mails and credentials
```

When running `MITMsmtp` without any parameters it will start an unencrypted SMTP server on port 8587 on all interfaces.


To use mitm-smtp as a transparent SMTP Proxy, enable forwarding mode...
``sysctl -w net.ipv4.ip_forward=1``
...block ICMP redirects...
``sysctl -w net.ipv4.conf.all.send_redirects=0``
...and create a port forwarding.
``iptables -t nat -A PREROUTING -p tcp --destination-port 587 -j REDIRECT --to-port 8888``

## Reference
[1] https://tools.ietf.org/html/rfc5321

[2] http://www.samlogic.net/articles/smtp-commands-reference-auth.htm
