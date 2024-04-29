import socket
import struct

LDAP_SERVER = 'localhost'
LDAP_PORT = 389

BASE_DN = 'dc=example,dc=com'
SEARCH_FILTER_TEMPLATE = '(o={})'
SCOPE_WHOLE_SUBTREE = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((LDAP_SERVER, LDAP_PORT))

org_name = input('Please enter an organization name: ')

search_filter = SEARCH_FILTER_TEMPLATE.format(org_name)

message_id = 1
protocol_op = 0x63
scope = SCOPE_WHOLE_SUBTREE
deref_aliases = 0 
size_limit = 0
time_limit = 0
types_only = False
attributes = ['*']
message = struct.pack('>Ib', message_id, protocol_op) + \
    BASE_DN.encode() + \
    struct.pack('>bbb', scope, deref_aliases, size_limit) + \
    struct.pack('>bb', time_limit, types_only) + \
    search_filter.encode() + \
    struct.pack('>b', len(attributes)) + \
    b''.join(attr.encode() for attr in attributes)

sock.send(message)

response = sock.recv(4096)

print('Response:', response)

sock.close()

response_id, response_protocol_op = struct.unpack('>Ib', response[:5])
if response_id != message_id or response_protocol_op != 0x64:
    print('Error: Invalid LDAP response')
else:
    print('Resource records:')
    print(response[5:].decode())