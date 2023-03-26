import requests
import json
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out.strip()

def processo(cep):

    url = "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm"
    data = {"relaxation": cep}

    page = requests.post(url, data=data)

    soup = BeautifulSoup(page.text, 'html.parser')

    dados = soup.find_all('td')

    res = []

    # return dados

    for dado in dados:
        res.append(remove_html_markup(dado))

    # print(dados)
    return res



# print('{"endereco": "' + remove_html_markup(resposta[0]) + '"}')

class MyRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Parse the query string from the URL
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        # Extract the value of the 'name' parameter
        cep = params.get('cep', [''])[0]

        resposta = processo(cep)
        
        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f'{json.dumps(resposta)}'.encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f'Serving on http://{server_address[0]}:{server_address[1]}...')
    httpd.serve_forever()