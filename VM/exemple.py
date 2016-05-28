"""
VSI configuration example
"""

# your ssh keys to add
# one for you, one for ansible perhaps
sshkeys = [000000,000001]

class ServerConfig :
    basehostname = "hostname"
    configParams = {
        """
        image_id is used when creating a raw instance.
        if poping it for pool generation from slapy, you dont need it
        as it will refers to latest one found in the sl images backups
        """
        'image_id':"cafebabe-b33f-c0c4",
        'domain': "domain.net",
        'cpus': 1,
        'memory': 1024,
        'datacenter':"ams01",
        'hourly': True,
        'private_vlan': 100008,
        'private': True,
        'ssh_keys': sshkeys,
        # the first tag is used as pool name
        'tags': 'poolname,test'
    }


