### Created by Igbana Israel
### 15-08-2024
### 
### I didn't use threading so that it will not look like a bruteforce the the website
### (and I didn't want to start reformatting my code)...
###
### It logs the status code and index of each link in the list of links gotten off the website, to the console
### It then saves each log in a logs.txt file
### At the end, it saves the total output in an output.txt file in somewhat of a json format (safety precaution)


from bs4 import BeautifulSoup
import requests
from pprint import pprint
URL = "https://futminna.edu.ng"


print("Initializing...\n")
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
links = soup.find_all("a")
print(f"{len(links)} links found...\n\n")


final_result = {}
good_links = []
bad_links = []
home_links = []
recheck = []
for link in links:
    try:
        status_code = requests.get(link["href"], timeout=15).status_code
        inner_html = link.text if link.text != '' else list(link.children)[0]
        output = f"[{status_code}] {links.index(link)+1}. {inner_html} ({link['href']})\n"
        if str(status_code)[0] == '2':
            good_links.append((link['href'], status_code))
        else:
            bad_links.append((link['href'], status_code))
    except Exception as e:
        if ((type(e) == requests.exceptions.ConnectionError) or (type(e) == requests.exceptions.ReadTimeout) or (type(e) == requests.exceptions.Timeout) or (type(e) == requests.exceptions.ConnectTimeout)):
            output = f"[TIMEOUT] {links.index(link)+1}. ({link['href']}): {e}... May need manual recheck\n"
            recheck.append(link['href'])
        else: 
            if link['href'] == "#":
                home_links.append(inner_html)
                output = f"[HASH] {links.index(link)+1}. {inner_html} ({link['href']})\n" 
            else:
                final_result[inner_html] = [link['href'], e]
                output = f"[INVALID] {links.index(link)+1}. {inner_html} ({link['href']}): {e}\n"
                bad_links.append((link['href'], "INVALID"))
    
    print(output)
    with open('logs.txt', 'a') as file: file.write(output+"\n")

final_result['GOOD_LINKS'] = good_links
final_result['BAD_LINKS'] = bad_links
final_result['HOME_LINKS'] = home_links
with open('output.txt', 'w') as file: pprint(final_result, stream=file)

pprint(final_result)