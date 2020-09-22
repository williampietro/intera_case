from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import hashlib 
import json


logging.basicConfig(level = logging.DEBUG)


def load_html(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html,'html')
        logging.info('Site carregado')
        return bs
    except:
        logging.error('Não foi possível carregar o site')
    
def scrapper_flamengo(url):
    players = {}
    bs = load_html(url)
    try:
        positions = [i for i in bs.find_all('div',class_='row') if 'elenco-profissional/' in str(i)]
        logging.info('Posições carregadas')
        for p in positions:
            for j in p.findAll('img'):
                player_hash = hashlib.md5(j['src'].encode() + j['alt'].encode() + p.find('h2').contents[0].encode()).hexdigest()
                picture = j['src']
                name = j['alt']
                position = p.find('h2').contents[0]
                player = '"name":"{0}", "position": "{1}","picture":"{2}"'.format(name,position,picture)
                players[player_hash] = player
        logging.info('jogadores carregados')
        return players
    except:
        logging.error('Falha na estrutura do site.')

def main():
    players = scrapper_flamengo("https://www.flamengo.com.br/elencos/elenco-profissional/")
    print(json.dumps(players, indent=4))

if __name__ == "__main__":
    main()