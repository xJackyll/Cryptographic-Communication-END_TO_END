import socket


def ip_and_machine_name_finder():

    # getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()

    # getting the IP address using socket.gethostbyname() method
    # WARNING: this may cause problem if you set up some virtual network on a VM
    own_ip_address = socket.gethostbyname(hostname)
    return hostname, own_ip_address