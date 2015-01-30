#-------------------------------------------------------------------------------
# Name:         nmap.py
# Purpose:      Replicates limited nmap functionality using python
# Author:       phillipsme
# Created:      12/08/2014
# Copyright:    (c) phillipsme 2014
# Licence:      Free to use, free to have fun!
# Version:      beta!!! (0.2)
# ToDo:         add threading
#-------------------------------------------------------------------------------
import socket
import argparse
import sys
import time

def main():
    # Output command line args to screen
    if args.verbose: printmsg("Arguments used:"); print args ;

    starttime=time.time()
    # Start Scanning
    results={}
    for target in targets:
        results[target]= portscan(target,ports,args.tcpscan,args.udpscan,args.verbose)
    printmsg(("Total scantime %.2f seconds") % (time.time()-starttime))

    for target in results:
        print "%s TCP:%s  UDP:%s" % (target,results[target][0],results[target][1])
    return results

def portscan(target,ports,tcp,udp,verbose):
    #target=IPaddr,ports=list of ports,tcp=true/false,udp=true/false,verbose=true/false
    tcpports=[]
    udpports=[]
    targetstarttime=time.time()
    if tcp:
        for portnum in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.01)
                s.connect((target, portnum))
            except Exception:
                failvar = 0
                if verbose: print "%d/tcp \tclosed" % (portnum)
            else:
                if verbose: print "%d/tcp \topen"% (portnum)
                tcpports.append(portnum)
            s.close()
    if udp:
        for portnum in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(0.1)
                s.sendto("--TEST LINE--", (target, portnum))
                recv, svr = s.recvfrom(255)
            except Exception, e:
                try: errno, errtxt = e
                except ValueError:
                    if verbose: print "%d/udp \topen"% (portnum)
                    udpports.append(portnum)
                else:
                    if verbose: print "%d/udp \tclosed" % (portnum)
            s.close()
    printmsg(("Scanned %s in %.2f seconds - Open: %iTCP, %iUDP" % \
                (target,time.time()-targetstarttime,len(tcpports),len(udpports))))
    return tcpports, udpports

def errormsg(msg): print "[!] Error: %s" % (msg) ; sys.exit(1)
def printmsg(msg): print "[+] nmap.py: %s" % (msg)

def iprange(addressrange): # converts a ip range into a list
    list=[]
    first3octets = '.'.join(addressrange.split('-')[0].split('.')[:3]) + '.'
    for i in range(int(addressrange.split('-')[0].split('.')[3]),int(addressrange.split('-')[1])+1):
        list.append(first3octets+str(i))
    return list

def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "": b += dec2bin(int(q),8); outQuads -= 1
    while outQuads > 0: b += "00000000"; outQuads -= 1
    return b

def dec2bin(n,d=None):
    s = ""
    while n>0:
        if n&1: s = "1"+s
        else: s = "0"+s
        n >>= 1
    if d is not None:
        while len(s)<d: s = "0"+s
    if s == "": s = "0"
    return s

def bin2ip(b):
    ip = ""
    for i in range(0,len(b),8):
        ip += str(int(b[i:i+8],2))+"."
    return ip[:-1]

def returnCIDR(c):
    parts = c.split("/")
    baseIP = ip2bin(parts[0])
    subnet = int(parts[1])
    ips=[]
    if subnet == 32: return bin2ip(baseIP)
    else:
        ipPrefix = baseIP[:-(32-subnet)]
        for i in range(2**(32-subnet)): ips.append(bin2ip(ipPrefix+dec2bin(i, (32-subnet))))
        return ips

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='nmap.py - Replicates limited nmap functionality in python')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable this for full output')
    parser.add_argument('-sS', '--tcpscan', action='store_true', help='Enable this for TCP scans')
    parser.add_argument('-sU', '--udpscan', action='store_true', help='Enable this for UDP scans')
    parser.add_argument('-p', '--ports', default='1-1024', help='The ports you want to scan (21,22,80,135-139,443,445)')
    parser.add_argument('-t', '--targets', help='The target(s) you want to scan (192.168.0.1)')
    if len(sys.argv)==1: parser.print_help(); sys.exit(0)
    args = parser.parse_args()

    # Set target (and convert for FQDN)
    targets=[]
    if args.targets:
        if '/' in args.targets: #found cidr target
            targets = returnCIDR(args.targets)
        elif '-' in args.targets:
            targets = iprange(args.targets)
        else:
            try: targets.append(socket.gethostbyname(args.targets)) # get IP from FQDN
            except: errormsg("Failed to translate hostname to IP address")
    else: parser.print_help(); errormsg("You need to set a hostname")

    # Set ports
    if args.ports == '-': args.ports = '1-65535'
    ranges = (x.split("-") for x in args.ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    main()