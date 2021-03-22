#!/usr/bin/env python3
import socket
import subprocess
import requests
import json
import urllib
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os
import getpass
import ifcfg
from ipaddress import ip_network, ip_address
import keyring

# set password
service_id = "rdp_test_tool"
username = input("Enter your ADM username: ")
keyring.set_password(service_id, username, password = getpass.getpass(prompt="Enter your Big Fix password: "))
# get password
password = keyring.get_password(service_id, username)

def test_vpn_status():
    if os.name == 'posix':
        unix_response = subprocess.Popen(['ping', 'REMOVEDFORSECURITY', '-c', '1', '-W', '2'])
        unix_response.wait()
        if unix_response.poll() == 0:
            print('\n...VPN Connection Confirmed...')
            connected = True
        else:
            print('\nYou are not connected to the VPN.')
            connected = False
    elif os.name == 'nt':
        response = subprocess.Popen('ping REMOVEDFORSECURITY')
        response.wait()
        if response.poll() == 0:
            print('\n...VPN Connection Confirmed...')
            connected = True
        else:
            print('\nYou are not connected to the VPN.')
            connected = False
    
    return connected

def authenticate_user():
    url = "REMOVEDFORSECURITY"
    response = requests.get(url, auth=(username, password))
    if response.status_code == 401:
        print("\nCheck Your Credentials, playa.\n")
        authenticated = False
    else:
        print("...........................")
        print("Big Fix User Authenticated.")
        print("............................")
        print("Loading Big Fix API Tools...")
        print("..............................\n")
        authenticated = True

    return authenticated

class Computer:
    def __init__(self, machineinfo=None, port= 'REMOVEDFORSECURITY'):
        self.machineinfo = machineinfo
        self.port = port
        self.resultResponse = None
        self.domain_name = None
        self.address = None
    
    def resolve_name(self):
        while True:
            self.machineinfo = input("Enter either an IP or a Hostname: ")
            self.port
            print("You entered: {}".format(self.machineinfo))
            try:
                self.address = socket.gethostbyname(self.machineinfo)
                break
            except (UnboundLocalError, socket.gaierror):
                print("Please enter a valid IP or hostname: ")
        self.domain_name = socket.getfqdn(self.machineinfo)

        print("\nMachine info: {}".format(self.machineinfo))
        print("IP Address: {}".format(self.address))
        print("Domain Name: {}".format(self.domain_name))
        print("Port: {}".format(self.port))

        return self
    
    def test_connection(self):
        s = socket.socket()
        try:
            s.connect((self.address, self.port))
            print("Connection to {}:{} successful!".format(self.machineinfo, self.port))
        except Exception:
            print("No Connection to {}:{} found. :(".format(self.machineinfo, self.port))
        finally:
            s.close()
        
        return self
    
    def submit_relevance(self):
        url = "REMOVEDFORSECURITY"
        relevance = "(name of it, last report time of it, operating system of it, value of (result (it, bes property whose (name of it = \"Serial number (Cross platform)\")))) of bes computers whose (concatenation \";\" of (ip addresses of it as string) contains \"{0}\")".format(self.address)
        parsed = urllib.parse.quote_plus(relevance)
        finalUrl = "{0}{1}".format(url, parsed)
        response = requests.get(finalUrl, auth=(username, password))
        jsonResponse = json.loads(response.content)
        self.resultResponse: [str] = jsonResponse["result"]

        return self.resultResponse, self
    
    def print_bigfix_info(self):
        print("\n...Big Fix Info...")
        print(".....................")
        bigfix_info = self.resultResponse[0]
        computer_name = bigfix_info[0]
        last_report = bigfix_info[1]
        oper_sys = bigfix_info[2]
        serial_num = bigfix_info[3]
        print("Computer Name: {}".format(computer_name))
        print("Last Time Reported: {}".format(last_report))
        print("Serial Number: {}".format(serial_num))
        print("Operating System: {}\n".format(oper_sys))
        
        return self

if __name__ == "__main__":
    connected = test_vpn_status()
    if connected is True:
        authenticated = authenticate_user()
    testing = True
    while testing:
        if connected and authenticated is True:
            cpu = Computer()
            machine = cpu.resolve_name().test_connection().submit_relevance()
            if len(machine[0]) == 0:
                print("\nBig Fix Data on this machine is unavailable either because it is not in your console, or the machine does not exist.")
            else:
                cpu.print_bigfix_info()
                keep_going = input("...hit enter to test another machine...\n ...type exit to exit... ")
                if keep_going == 'exit':
                    testing = False
        else:
            print("\n=================================================")
            print("...Could not execute script. See message above...")
            print("==================================================")
            testing = False
