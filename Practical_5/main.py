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
if response_id != message_id or response_protocol_op != 0x64:  # LDAP search result done
    print('Error: Invalid LDAP response')
else:
    print('Resource records:')
    print(response[5:].decode())

# import socket
# import struct

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_address = ('localhost', 389)

# s.connect(server_address)

# message_id = 1
# base_object = 'dc=example,dc=com'
# scope = 2
# deref_aliases = 0
# size_limit = 0
# time_limit = 0
# types_only = False
# filter = '(objectClass=*)'
# attributes = ['cn', 'mail']

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

# for attribute in attributes:
#     ldap_message += struct.pack('!B', len(attribute))  # Length of the attribute
#     ldap_message += attribute.encode()  # attribute

# s.sendall(ldap_message)

# data = s.recv(1024)

# response = struct.unpack('!B', data)

# print(response)

# s.close()
