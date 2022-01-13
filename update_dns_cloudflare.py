import sys
import requests
import re

ZONE_ID = '{zone id, you can find under your domain}'
CF_EMAIL = '{your email}'
CF_API_KEY = '{global API KEY}'
CLOUD_API_URL = 'https://api.cloudflare.com/client/v4/zones/{}'.format(ZONE_ID)

def get_my_ip():
    """Cloudflare API code - example"""

    # This list is adjustable - plus some v6 enabled services are needed
    # url = 'http://myip.dnsomatic.com'
    # url = 'http://www.trackip.net/ip'
    # url = 'http://myexternalip.com/raw'
    url = 'http://ip.tool.lu'
    try:
        response = requests.get(url).text
        ip_address = re.findall( r'[0-9]+(?:\.[0-9]+){3}',response)[0]
    except:
        exit('%s: failed' % (url))
    if ip_address == '':
        exit('%s: failed' % (url))

    if ':' in ip_address:
        ip_address_type = 'AAAA'
    else:
        ip_address_type = 'A'

    return ip_address, ip_address_type


def get_record_id(domain_name):
    resp = requests.get(CLOUD_API_URL + '/dns_records?name={}'.format(domain_name), headers={'X-Auth-Key': CF_API_KEY, 'X-Auth-Email': CF_EMAIL})
    json_obj = resp.json()
    if len(json_obj['result']) == 0:
        return ''
    return json_obj['result'][0]['id']


def update_record(record_id, domain_name, ip, record_type):
    resp = requests.put(CLOUD_API_URL + '/dns_records/{}'.format(record_id), headers={'X-Auth-Key': CF_API_KEY, 'X-Auth-Email': CF_EMAIL}, json={'type': record_type, 'name':domain_name, 'content': ip, 'proxied': False})
    return resp.status_code == 200


def main():
    dns_names = sys.argv[1]
    print('Starting to update the following dns: {}'.format(dns_names))
    dns_list = dns_names.split(',')
    
    ip, record_type = get_my_ip()
    for dns in dns_list:
        record_id = get_record_id(dns)
        result = update_record(record_id, dns, ip, record_type)
        if result == True:
            print('Update {} with {} successfully'.format(dns, ip))
        else:
            print('Update {} failed'.format(dns))

if __name__ == '__main__':
    main()
