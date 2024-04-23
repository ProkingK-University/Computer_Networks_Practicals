import socket
import struct

# Define the LDAP server details
LDAP_SERVER = 'localhost'
LDAP_PORT = 389

# Define the LDAP search request details
BASE_DN = 'dc=example,dc=com'
SEARCH_FILTER_TEMPLATE = '(o={})'
SCOPE_WHOLE_SUBTREE = 2

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the LDAP server
sock.connect((LDAP_SERVER, LDAP_PORT))

# Ask the user for an organization name
org_name = input('Please enter an organization name: ')

# Create the search filter
search_filter = SEARCH_FILTER_TEMPLATE.format(org_name)

# Create the LDAP search request message
message_id = 1
protocol_op = 0x63  # LDAP search request
scope = SCOPE_WHOLE_SUBTREE
deref_aliases = 0  # never dereference aliases
size_limit = 0  # no limit
time_limit = 0  # no limit
types_only = False
attributes = ['*']  # request all attributes
message = struct.pack('>Ib', message_id, protocol_op) + \
    BASE_DN.encode() + \
    struct.pack('>bbb', scope, deref_aliases, size_limit) + \
    struct.pack('>bb', time_limit, types_only) + \
    search_filter.encode() + \
    struct.pack('>b', len(attributes)) + \
    b''.join(attr.encode() for attr in attributes)

# Send the LDAP search request
sock.send(message)

# Receive the LDAP search response
response = sock.recv(4096)

print('Response:', response)

# Close the socket
sock.close()

# Parse the LDAP search response
response_id, response_protocol_op = struct.unpack('>Ib', response[:5])
if response_id != message_id or response_protocol_op != 0x64:  # LDAP search result done
    print('Error: Invalid LDAP response')
else:
    # Print the resource records
    print('Resource records:')
    print(response[5:].decode())
