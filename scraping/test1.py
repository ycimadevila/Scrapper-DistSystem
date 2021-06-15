from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/aphrodite"
page = urlopen(url)# devuelve un objeto HTTPResponse

html_bytes = page.read()#devuelve el html como una secuencia de bytes
html = html_bytes.decode("utf-8")#convierte a string

print(html)

title_index = html.find("<title>")#devuelve el indice
start_index = title_index + len("<title>")
end_index = html.find("</title>")

title = html[start_index:end_index]
print(title)

