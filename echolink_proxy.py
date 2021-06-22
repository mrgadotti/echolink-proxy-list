import json
import requests
import pandas as pd

url = 'http://www.echolink.org/proxylist.jsp'
print("Getting data from URL")
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[2]
# print(df)
print("Send data to Json")
j = df.to_json() # json
data = json.loads(j) # create dict
proxy_str = ""
print("Copy each proxy to dict")
for i in data['Status']:
    if data['Status'][str(i)] == "Ready":
        #print(data['Name'][str(i)] +" -> " + str(data['Host Address'][str(i)]) + ":" + str(data['Port'][str(i)]))
        proxy_str += str(data['Name'][str(i)]) +" -> " + str(data['Host Address'][str(i)]) + ":" + str(data['Port'][str(i)]) + "\r\n"

print(proxy_str)
text_file = open("proxy.txt", "w")
text_file.write(proxy_str)
text_file.close()
