import ldap3

# Define the LDAP server details
LDAP_SERVER = 'localhost'
LDAP_PORT = 389

# Define the LDAP search request details
BASE_DN = 'dc=example,dc=com'
SEARCH_FILTER_TEMPLATE = '(o={})'

# Ask the user for an organization name
org_name = input('Please enter an organization name: ')

# Create the search filter
search_filter = SEARCH_FILTER_TEMPLATE.format(org_name)

# Create a Server object
server = ldap3.Server(LDAP_SERVER, port=LDAP_PORT)

# Create a Connection object
conn = ldap3.Connection(server)

# Bind to the server
if not conn.bind():
    print('Error: Could not bind to the server')
else:
    # Perform the search
    if not conn.search(BASE_DN, search_filter, attributes=ldap3.ALL_ATTRIBUTES):
        print('Error: Could not perform LDAP search')
    else:
        # Print the search results
        for entry in conn.entries:
            print(entry)

# Unbind from the server
conn.unbind()