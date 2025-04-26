import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup

# SUBSTITUA com suas informações do Telegram
TOKEN = '8007893235:AAFqa59dlkHGNL5ltvQaOrNNiLsxhEGXHjc'
CHAT_ID = 'SelecaoPos_bot'

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': mensagem}
    requests.post(url, data=payload)

def verificar_sites():
    urls = [
        'https://www.ufpe.br/ppg',
        'https://www.ufrpe.br/br/editais',
        'https://portal.ifpe.edu.br/o-ifpe/pesquisa-pos-e-inovacao/pesquisa-pos-e-inovacao-editais/',
        'https://www.ufpe.br/propg/editaisppgs',
        'https://www.ufpe.br/ead/editais'
    ]
    palavras_chave = ['seleção', 'edital', 'mestrado', 'pós-graduação', 'processo seletivo', 'PPG']

    for url in urls:
        try:
            resposta = requests.get(url, verify=False)
            if resposta.status_code == 200:
                soup = BeautifulSoup(resposta.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    texto = link.get_text().lower()
                    if any(p in texto for p in palavras_chave):
                        href = link["href"]
                        if not href.startswith("http"):
                            href = url + href
                        mensagem = f'📝 Novo edital: {texto}\n🔗 {href}'
                        enviar_telegram(mensagem)
        except Exception as e:
            print(f'Erro em {url}: {e}')

# Rodar o bot manualmente
verificar_sites()
