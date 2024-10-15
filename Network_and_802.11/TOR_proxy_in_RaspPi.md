# A Tor Proxy in a Raspberry Pi


In this tutorial, I walk through all the steps to set up a Tor proxy in a Raspberry Pi (Model B). This work was based on some of the tutorials from Adafruit.

# Setting Up a Raspberry Pi

## Installing an Operating System in the SD card

[You can either install NOOBS and then choose your OS](http://www.raspberrypi.org/help/noobs-setup).

[Or you can download the Fedora ARM Installer and the OS image you prefer](http://fedoraproject.org/wiki/FedoraARMInstaller).

## Network Setup

The easiest way is to connect your Pi in the network is through an Ethernet interface. Connecting the cable should be allowed the connection directly as long as your network router enable DHCP.

Also, you can also set up wireless connect, which requires your router to be broadcasting the SSID. At Raspbian, there is a WiFi configuration icon. Type wlan0 adapter and scan. After connecting in your network you will also be able to see the IP of your Pi.

## Input/Output Setup

The easiest way to connect to your Pi is by an HDMI cable to a monitor and a USB keyboard. Another option is through a console cable or an SSH connection.

## Connection through a Console Cable (3.3V logic levels)

The connections are to the outside pin connections of the GPIO header:

```
The red lead should be connected to 5V.
The black lead to GND,
The white lead to TXD.
The green lead to RXD.
If the serial lead (red) is connected, do not attach the Pi's USB power adapter. 
```

In Linux you can use screen:
```
$ sudo apt-get install screen
$ sudo screen /dev/ttyUSB0 115200
```

In Windows, you can use a terminal emulation such as Putty and the drivers from this (link)[http://www.prolific.com.tw/US/ShowProduct.aspx?p_id=225&pcid=41]. Verify the number of the COM serial port in the Device manager and connect with speed 115200.

## SSH Connection

You need to enable SSH on the Pi:

```
$ sudo raspi-config
```

Find Pi's IP by:
```
$ sudo ifconfig
```

From your Linux PC (using "pi" as the user):
```
$ sudo PI-IP -l pi
```

You can (should) set RSA keys. In a terminal session on the Linux client enter:
```
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
$ ssh-keygen -t rsa
```

Now copy the public key over to the Pi by typing in the client:
```
$ ssh-copy-id <userid>@<hostname or ip address>
```

## Setting up a Wi-Fi Access Point

You need an ethernet cable and a WiFi adapter. First, check if you see the wlan0 (the WiFi) module:
```
$ ifconfig -a 
```

### DHCP Server Configuration

Install the software that will act as the hostap (host access point):
```
$ sudo apt-get install hostapd isc-dhcp-server
```

If the Pi cannot get the apt-get repositories:
```
$ sudo apt-get update 
```

Edit ```/etc/networks/interfaces```:
```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0

iface wlan0 inet static
 address 192.168.42.1
 netmask 255.255.255.0
```

Then edit the DHCP server configuration file, ```/etc/dhcp/dhcpd.conf```:
```
subnet 192.168.42.0 netmask 255.255.255.0 {
range 192.168.42.10 192.168.42.50;
option broadcast-address 192.168.42.255;
option routers 192.168.42.1;
default-lease-time 600;
max-lease-time 7200;
option domain-name "local";
option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```

Now, add the bellow line to ```/etc/default/isc-dhcp-server```:
```
INTERFACES="wlan0" 
```

Restart the network:
```
$ sudo /etc/init.d/networking restart
```

### IP Forwarding

Enable IP forwarding and setting up NAT to allow multiple clients to connect to the WiFi and have all the data 'tunneled' through the single Ethernet IP:
```
$ sudo echo 1 > /proc/sys/net/ipv4/ip_forward
$ sudo nano /etc/sysctl.conf
```
Uncomment the next line to enable packet forwarding for IPv4:
```
net.ipv4.ip_forward=1
```
And update:
```
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
```

### Firewall Configuration

We insert an iptables rule to allow NAT (network address translation):
```
$ iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
$ iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
$ iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

To make the above true in every reboot:
```
$ sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

For additional security (it blocks access from RFC 1918 subnets on your internet (eth0) interface as well as ICMP (ping) packets and ssh connections.):
```
$ sudo iptables -A INPUT -s 192.168.0.0/24 -i eth0 -j DROP
$ sudo iptables -A INPUT -s 10.0.0.0/8 -i eth0 -j DROP
$ sudo iptables -A INPUT -s 172.16.0.0/12 -i eth0 -j DROP
$ sudo iptables -A INPUT -s 224.0.0.0/4 -i eth0 -j DROP
$ sudo iptables -A INPUT -s 240.0.0.0/5 -i eth0 -j DROP
$ sudo iptables -A INPUT -s 127.0.0.0/8 -i eth0 -j DROP
$ sudo iptables -A INPUT -i eth0 -p tcp -m tcp --dport 22 -j DROP
$ sudo iptables -A INPUT -i eth0 -p icmp -m icmp --icmp-type 8 -j DROP
$ sudo iptables-save > /etc/iptables.up.rules
```

If you want to see how many packets your firewall is blocking:
```
$ iptables -L -n -v
```
If your eth0 still shows a private address, it probably didn't renew when you moved it to your modem. Fix this by running:
```
$ sudo ifdown eth0 && sudo ifup eth0
```

## Access Point Configuration

Configure Access Point with hostpad, editing ```/etc/hostapd/hostapd.conf```:
```
interface=wlan0
driver=rtl871xdrv
ssid=Pi_AP
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=Raspberry
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Now we will tell the Pi where to find this configuration file in /etc/default/hostapd:
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

And start the access point by running hostpad:
```
$ hostapd -d /etc/hostapd/hostapd.conf
```

To start automatically, add the command to ```/etc/rc.local```:
```
$ hostapd -B /etc/hostapd/hostapd.conf
```

### Logs and Status

To see the system log data, run in the Pi:
```
$ tail -f /var/log/syslog
```

You can always check the status of the host AP server and the DHCP server with:
```
$ sudo service hostapd status
$ sudo service isc-dhcp-server status
```

### Setting up a Daemon

Now that we know it works, we can set it up as a 'daemon' (a program that will start when the Pi boots):
```
$ sudo service hostapd start 
$ sudo service isc-dhcp-server start
```

To start the daemon services. Verify that they both start successfully (no 'failure' or 'errors')
```
$ sudo update-rc.d hostapd enable 
$ sudo update-rc.d isc-dhcp-server enable
```

### Removing WPA-Supplicant

Depending on your distribution, you may need to remove WPASupplicant. Do so by running this command:
```
sudo mv /usr/share/dbus-1/system-services/fi.epitest.hostap.WPASupplicant.service ~/
```

## Setting up the Tor Proxy

You now have a wirelesses access point in your Pi. To make it a Tor proxy, first install Tor:
```
$ sudo apt-get install tor
```
Then edit the Tor config file at ```/etc/tor/torrc```:

```
Log notice file /var/log/tor/notices.log
VirtualAddrNetwork 10.192.0.0/10
AutomapHostsSuffixes .onion,.exit
AutomapHostsOnResolve 1
TransPort 9040
TransListenAddress 192.168.42.1
DNSPort 53
DNSListenAddress 192.168.42.1
```

Change the IP routing tables so that connections via the WiFi interface (wlan0) will be routed through the Tor software. To flush the old rules from the IP NAT table do:
```
$ sudo iptables -F
$ sudo iptables -t nat -F
```

Add the iptables, to be able to ssh:
```
$ sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 22 -j REDIRECT --to-ports 22 
```

To route all DNS (UDP port 53) from interface wlan0 to internal port 53 (DNSPort in our torrc):
```
$ sudo iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j REDIRECT --to-ports 53
```

To route all TCP traffic from interface wlan0 to port 9040 (TransPort in our torrc):
```
$ sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --syn -j REDIRECT --to-ports 9040 
```

Check that the iptables is right with:
```
$ sudo iptables -t nat -L
```

If everything is good, we'll save it to our old NAT save file:
```
$ sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

Next we'll create our log file (handy for debugging) with:
```
$ sudo touch /var/log/tor/notices.log
$ sudo chown debian-tor /var/log/tor/notices.log
$ sudo chmod 644 /var/log/tor/notices.log
```

Check it with:
```
$ ls -l /var/log/tor
```

Finally, you can start the Tor service manually:
```
$ sudo service tor start
```

And make it start on boot:
```
$ sudo update-rc.d tor enable
```

That's it! Browser safe!

---
Enjoy! This article was originally posted [here](https://coderwall.com/p/m3excg/a-tor-proxy-in-a-raspberry-pi).
