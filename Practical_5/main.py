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

# import socket
# import struct

# # Create a new socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Define the server address and port
# server_address = ('localhost', 389)

# # Connect the socket to the server
# s.connect(server_address)

# # Define your raw LDAP message here
# message_id = 1
# base_object = 'dc=example,dc=com'
# scope = 2  # wholeSubtree
# deref_aliases = 0  # neverDerefAliases
# size_limit = 0
# time_limit = 0
# types_only = False
# filter = '(objectClass=*)'
# attributes = ['cn', 'mail']

# # Construct the LDAP message
# ldap_message = struct.pack('!B', 0x30)  # LDAPMessage SEQUENCE tag
# ldap_message += struct.pack('!B', len(base_object) + len(filter) + len(attributes) + 11)  # Length of the LDAPMessage
# ldap_message += struct.pack('!B', 0x02)  # messageID INTEGER tag
# ldap_message += struct.pack('!B', 0x01)  # Length of the messageID
# ldap_message += struct.pack('!B', message_id)  # messageID
# ldap_message += struct.pack('!B', 0x63)  # searchRequest tag
# ldap_message += struct.pack('!B', len(base_object) + len(filter) + len(attributes) + 7)  # Length of the searchRequest
# ldap_message += struct.pack('!B', 0x04)  # baseObject OCTET STRING tag
# ldap_message += struct.pack('!B', len(base_object))  # Length of the baseObject
# ldap_message += base_object.encode()  # baseObject
# ldap_message += struct.pack('!B', scope)  # scope ENUMERATED
# ldap_message += struct.pack('!B', deref_aliases)  # derefAliases ENUMERATED
# ldap_message += struct.pack('!B', size_limit)  # sizeLimit INTEGER
# ldap_message += struct.pack('!B', time_limit)  # timeLimit INTEGER
# ldap_message += struct.pack('!B', types_only)  # typesOnly BOOLEAN
# ldap_message += struct.pack('!B', 0xa0)  # filter tag (present)
# ldap_message += struct.pack('!B', len(filter) - 2)  # Length of the filter
# ldap_message += filter.encode()  # filter
# ldap_message += struct.pack('!B', 0x30)  # attributes SEQUENCE OF tag

# # Add each attribute separately
# for attribute in attributes:
#     ldap_message += struct.pack('!B', len(attribute))  # Length of the attribute
#     ldap_message += attribute.encode()  # attribute

# # Send the raw LDAP message
# s.sendall(ldap_message)

# # Receive the response
# data = s.recv(1024)

# response = struct.unpack('!B', data)

# print(response)

# # Close the socket
# s.close()
