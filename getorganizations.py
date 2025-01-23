import meraki
import warnings
import requests
import os
from urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Path to the Zscaler root CA certificate
zscaler_cert_path = r"C:\Users\keith.ransom\dashboard-api-python\certs\zscaler_root_ca.pem"

# Ensure the certificate file exists
if not os.path.exists(zscaler_cert_path):
    raise FileNotFoundError(f"Zscaler root CA certificate not found at {zscaler_cert_path}")

# Get API key from environment variable
api_key = os.environ.get('MERAKI_DASHBOARD_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set the MERAKI_DASHBOARD_API_KEY environment variable.")
# Initialize the Meraki dashboard API client
dashboard = meraki.DashboardAPI(
    api_key=api_key,
    suppress_logging=False,
    output_log=True,
    print_console=False,
    certificate_path=zscaler_cert_path,  # Use the Zscaler root CA certificate
    requests_proxy=None,
    wait_on_rate_limit=True,
    maximum_retries=3,
    single_request_timeout=30,
)

# Get organizations
try:
    organizations = dashboard.organizations.getOrganizations()
    print(organizations)
except meraki.exceptions.APIError as e:
    print(f"Error: {e}")

# Print the organizations and get the first organization ID
org_id = None
for org in organizations:
    print(f"Organization Name: {org['name']}, ID: {org['id']}")
    if org_id is None:
        org_id = org['id']

# Get networks for the first organization
if org_id:
    networks = dashboard.organizations.getOrganizationNetworks(org_id)

    # Print the networks and get the first network ID
    network_id = None
    for network in networks:
        print(f"Network Name: {network['name']}, ID: {network['id']}")
        if network_id is None:
            network_id = network['id']

    # Get devices for the first network
    if network_id:
        devices = dashboard.networks.getNetworkDevices(network_id)

        # Print the devices
        for device in devices:
            print(f"Device Name: {device['name']}, Serial: {device['serial']}, Model: {device['model']}")
    else:
        print("No networks found in the organization.")
else:
    print("No organizations found.")

