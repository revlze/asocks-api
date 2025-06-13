from asocks_api import ASocksClient

client = ASocksClient()
ports = client.get_ports()

for port in ports:
  print(port["proxy"])