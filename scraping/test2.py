from urllib.request import urlopen
import re

url = "http://olympus.realpython.org/profiles/poseidon"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)

'''
title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
print(title)
'''

match = re.findall("ab*c","ac")
print(match)

title = re.findall("<title.*>",html)
print(title)

title_ = re.search("<title.*>",html)
t = title_.group()
print(t)

string = "Everything is <replaced> if it's in <tags>."
string = re.sub("<.*>", "ELEPHANTS", string)
print(string)

string = "Everything is <replaced> if it's in <tags>."
string = re.sub("<.*?>", "ELEPHANTS", string)
print(string)