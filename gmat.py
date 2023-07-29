#!/bin/python3
import requests
import click
import json
import sys


global hunter_key, dehashed_cred_key, dehashed_key

# Place Keys here
hunter_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Hunter.io API Key
dehashed_cred_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX' # Dehashed email
dehashed_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Dehashed API Key


@click.command()
@click.option('-T', '--target', default=None, help='Specify your target to enumerate domain and credentials.')
@click.option('-D', '--domain', default=None, help='Specify the domain to enumerate credentials.')

def main(target, domain):
    if (target and domain):
        print('Error: Target and Domain are exclusive.')
        print('Usage: gmat.py [OPTIONS]')
        print("Try 'gmat.py --help' for help.")
        sys.exit()
    elif target:
        print("Target set: " +target)
        target_option(target)
    elif domain:
        print("Domain set: " + domain)
        domain_option(domain)
    else:
        print('Error: No target or domain specified.')
        print('Usage: gmat.py [OPTIONS]')
        print("Try 'gmat.py --help' for help.")
        sys.exit()

# Target 
# Starts with searching for a domain of the company specified with Hunter.io then will move into enumerating for credentials
def target_option(target):
    global hunter_key, dehashed_cred_key, dehashed_key
       # Use the 'target' variable in your program logic
    
    # Hunter.io API
    def fetch_company_domain(company_name):
        global hunter_key
        api_url = f"https://api.hunter.io/v2/domain-search?company={company_name}&api_key={hunter_key}"
        hunter_results = requests.get(api_url)
        hunter_data = hunter_results.json()
        
        # For debugging purposes
        #print(hunter_data)

        fixed_hunter_data = fix_hunter_json_string(json.dumps(hunter_data))
        print(format_json_indents(fixed_hunter_data))

        domain = hunter_data['data']['domain']
    
        # File Stuff for later 
        '''
        # Write the content to a file inside the folder
        hunter_file = "hunter.txt"
        output_file_path = os.path.join(directory, hunter_file)
        with open(output_file_path, 'w') as file:
            file.write(hunter_data)
    
        print(f"File '{hunter_file}' has been written to '{directory}'.")
        '''
    
        return domain
    
    # Dehashed API
    def dehashed_information(target_arg):
        global dehashed_cred_key, dehashed_key
        headers = {'Accept': 'application/json'}
        params = (('query', f'domain:{target_arg}'),)
        
        dehashed_json = requests.get('https://api.dehashed.com/search',
            headers=headers,
            params=params,
            auth=(f'{dehashed_cred_key}', f'{dehashed_key}')).text

        # print(dehashed_json)
        
        return dehashed_json
    
    
    #Removes empty JSON values
    def remove_empty_dehashed_values(json_data):
        response_dict = json.loads(json_data)
        entries = response_dict.get("entries", [])
        cleaned_entries = []
        
        for item in entries:
            cleaned_item = {key: value for key, value in item.items() if value is not None and value != ""}
            cleaned_entries.append(cleaned_item)
    
        response_dict["entries"] = cleaned_entries
        return json.dumps(response_dict)
    
    
    # reformat to json, better viewing
    def format_json_indents(json_data):
        data_dict = json.loads(json_data)
        formatted_results = json.dumps(data_dict, indent=4)
        return formatted_results
    

    # This fixes the weird json string that hunter.io responds with
    def fix_hunter_json_string(json_data_str):
        fixed_json_data_str = json_data_str.replace("'", '"').replace(": True", ': "true"').replace(": False", ': "false"').replace(": None", ': ""')
        return fixed_json_data_str
    

    
    
    domain = fetch_company_domain(target)
    if domain:
        print("Domain: ", domain)
    
        # Make directory for data for later
        # directory = 'Target_arg'
        # os.makedirs(directory, exist_ok=True)
    
    else:
        print("No domain found for the company domain on Hunter.io.")
        sys.exit()
    
    results = dehashed_information(domain)
    if results:
        # For debugging purposes
        # print(results)
    
        formatted_results = format_json_indents(results) #This was abstracting into its own method since it will be used several times
    
        finished_results = remove_empty_dehashed_values(formatted_results)
    
        print(format_json_indents(finished_results))
    
    
    
        # File stuff for later
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
    
    return

# Domain
# This will skip the domain enumeration with Hunter.io and only enumerate for credentials with the domain given
def domain_option(domain):
    # This is being worked on
    global hunter_key, dehashed_cred_key, dehashed_key
       # Use the 'target' variable in your program logic
    
    # Hunter.io API
    def domain_information(company_domain):
        global hunter_key
        api_url = f"https://api.hunter.io/v2/domain-search?domain={company_domain}&api_key={hunter_key}"
        hunter_results = requests.get(api_url)
        hunter_data = hunter_results.json()
        
        # For debugging purposes
        #print(hunter_data)

        fixed_hunter_data = fix_hunter_json_string(json.dumps(hunter_data))

        # This doesnt need to be printed but should be sent to a file
        # print(format_json_indents(fixed_hunter_data))

        # File Stuff for later 
        '''
        # Write the content to a file inside the folder
        hunter_file = "hunter.txt"
        output_file_path = os.path.join(directory, hunter_file)
        with open(output_file_path, 'w') as file:
            file.write(hunter_data)
    
        print(f"File '{hunter_file}' has been written to '{directory}'.")
        '''
    
        return 
    
    # Dehashed API
    def dehashed_information(target_arg):
        global dehashed_cred_key, dehashed_key
        headers = {'Accept': 'application/json'}
        params = (('query', f'domain:{target_arg}'),)
        
        dehashed_json = requests.get('https://api.dehashed.com/search',
            headers=headers,
            params=params,
            auth=(f'{dehashed_cred_key}', f'{dehashed_key}')).text

        # print(dehashed_json)
        
        return dehashed_json
    
    #Removes empty JSON values
    def remove_empty_dehashed_values(json_data):
        response_dict = json.loads(json_data)
        entries = response_dict.get("entries", [])
        cleaned_entries = []
        
        for item in entries:
            cleaned_item = {key: value for key, value in item.items() if value is not None and value != ""}
            cleaned_entries.append(cleaned_item)
    
        response_dict["entries"] = cleaned_entries
        return json.dumps(response_dict)
    
    # reformat to json, better viewing
    def format_json_indents(json_data):
        data_dict = json.loads(json_data)
        formatted_results = json.dumps(data_dict, indent=4)
        return formatted_results

    # This fixes the weird json string that hunter.io responds with
    def fix_hunter_json_string(json_data_str):
        fixed_json_data_str = json_data_str.replace("'", '"').replace(": True", ': "true"').replace(": False", ': "false"').replace(": None", ': ""')
        return fixed_json_data_str
    

    
    
    domain_information(domain)
    
    results = dehashed_information(domain)
    if results:
        # For debugging purposes
        # print(results)
    
        formatted_results = format_json_indents(results) #This was abstracting into its own method since it will be used several times
    
        finished_results = remove_empty_dehashed_values(formatted_results)
    
        print(format_json_indents(finished_results))
    
    
    
        # File stuff for later
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
    
    return



if __name__ == '__main__':
    main()



'''
put the results to a file - semi complete
clean up the initil print - hunter is not jsonifying but eh
create domain, will still go through hunter.io, then go through dehashed
'''
