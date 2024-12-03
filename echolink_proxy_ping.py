import json
import requests
import pandas as pd
import subprocess
import re

def ping_host(ip):
    try:
        # Executa o comando ping no IP especificado (4 pacotes)
        result = subprocess.run(["ping", "-c", "4", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Extrai o tempo médio do ping usando regex
        match = re.search(r"min/avg/max/mdev = [\d\.]+/([\d\.]+)/", result.stdout)
        if match:
            return float(match.group(1))  # Retorna o tempo médio de ping
        return float('inf')  # Retorna infinito caso o ping falhe
    except Exception:
        return float('inf')

# Obter dados do URL
url = 'http://www.echolink.org/proxylist.jsp'
print("Getting data from URL")
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[2]

# Convertendo para JSON e carregando em um dicionário
j = df.to_json()
data = json.loads(j)

# Processar os proxies prontos
proxy_list = []
print("Filtering Ready proxies")
for i in data['Status']:
    if data['Status'][str(i)] == "Ready":
        ip_port = f"{data['Host Address'][str(i)]}:{data['Port'][str(i)]}"
        ip = str(data['Host Address'][str(i)])
        proxy_list.append((ip, ip_port))

# Realizar ping em cada endereço IP e armazenar os resultados
ping_results = []
print("Pinging each proxy")
for ip, ip_port in proxy_list:
    print(f"Pinging {ip}...")
    response_time = ping_host(ip)
    ping_results.append((ip_port, response_time))

# Ordenar os resultados pelo tempo de resposta
sorted_results = sorted(ping_results, key=lambda x: x[1])

# Salvar no arquivo txt
output_file = "sorted_proxies.txt"
with open(output_file, "w") as text_file:
    for ip_port, response_time in sorted_results:
        text_file.write(f"{ip_port}\n")

print(f"Sorted proxies saved to {output_file}")
