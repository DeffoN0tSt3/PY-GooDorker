# Python 3 Google Dorker by sZ - Updated to work with python3
# To be used for legitimate, authorized pen testing only.
# DISCLAIMER: 
# ANY MALICIOUS USE OF THE CONTENTS FROM THIS ARTICLE WILL NOT HOLD THE AUTHOR & OR UPLOADER RESPONSIBLE,
# THE CONTENTS ARE SOLELY FOR EDUCATIONAL PURPOSE & LEGITIMATE Authorized PENTESTING.


import requests
import re
import urllib.parse
import urllib.request

print('Simple Goo Dorker by sZ')
start_from = 0
query = urllib.parse.quote(input("> Dork: "))
country = input("> Country: ")
filename = input("> Output filename: ")

with open(filename + '.txt', 'w') as f:
    f.write('-- START --\n')
    f.close()

print()
print('https://www.google.com/search?q=inurl:' + query + '&num=100&cr=country' + country)
print()

def dorker(query, country):
    r = requests.get('https://www.google.com/search?q=inurl:' + query + '&num=100&cr=country' + country)
    if r.status_code == 200:
        pattern = r'<div class="kCrYT"><a href="\/url\?q=(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})*">'
        url_list = re.findall(pattern, r.text)
        return url_list
    else:
        print("Error! Code: <" + str(r.status_code) + ">")
        exit(0)

if len(dorker(query, country)) != 0:
    url_list = dorker(query, country)
    how_much = 0
    for i in range(0, len(url_list)):
        how_much += 1
        vulnerable = False
        currentUrl = urllib.parse.urlparse(urllib.parse.unquote(url_list[i])).netloc
        urlWithQuery = currentUrl + '/' + urllib.parse.unquote(query)
        with open(filename + '.txt', 'a') as f:
            try:
                realUrl = urllib.request.urlopen(url_list[i]).geturl()
            except:
                realUrl = urlWithQuery
                pass
            print(currentUrl + " --> " + realUrl)
            f.write(realUrl + '\n')
    print("=== WE DONE, (" + str(how_much) + ") ===")
else:
    print("=== NOTHING FOUND?! ===")
