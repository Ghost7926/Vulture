#!/bin/python3
import requests
import click
import json
import sys

'''
@click.command()
@click.option('-T', '--target', default=None, required=True, help='Your target.')
'''

def fetch_company_domain(company_name):
    api_url = f"https://api.hunter.io/v2/domain-search?company={company_name}&api_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    hunter_results = requests.get(api_url)
    hunter_data = hunter_results.json()
    
    # For debugging purposes
    print(hunter_data)

    domain = hunter_data['data']['domain']

    '''
    # Write the content to a file inside the folder
    hunter_file = "hunter.txt"
    output_file_path = os.path.join(directory, hunter_file)
    with open(output_file_path, 'w') as file:
        file.write(hunter_data)

    print(f"File '{hunter_file}' has been written to '{directory}'.")
    '''

    return domain


def dehashed_information(target_arg):
    headers = {'Accept': 'application/json'}
    params = (('query', f'domain:{target_arg}'),)
    
    dehashed_json = requests.get('https://api.dehashed.com/search',
        headers=headers,
        params=params,
        auth=('XXXXXXXXXXXXXXXXXXx', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')).text
    
    return dehashed_json


# For debugging purposes
#print(target)


domain = fetch_company_domain("Grand Canyon University")
if domain:
    print("Domain: ", domain)

    # Make directory for data
    # directory = 'Target_arg'
    # os.makedirs(directory, exist_ok=True)

else:
    print("No domain found for the company domain on Hunter.io.")
    sys.exit()

results = dehashed_information(domain)
if results:
    # For debugging purposes
    print(results)

    # reformat to json, better viewing
    data_dict = json.loads(results)
    formatted_results = json.dumps(data_dict, indent=4)

    print(formatted_results)

    '''
    dehashed_file = "dehashed.txt"

    # Write the content to a file inside the folder
    output_file_path = os.path.join(directory, dehashed_file)
    with open(output_file_path, 'w') as file:
        file.write(formatted_results)
    print(f"File '{file_name}' has been written to '{directory}'.")
    '''

else:
    print("No information found for the domain on dehashed.com.")






'''
put the results to a file - semi complete
clean up the initil print - hunter is not jsonifying
put the full hunter.io to a file - semi complete
fix the click shtuff
try to delete the blank variables 
create forcing the domain, add the domain hunter.io api
'''
