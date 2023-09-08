from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import credenciais

pedidos = [
20230831693196,
]
lista = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://app.konduto.com/login')
    time.sleep(2)
    page.fill('input#ember352', 'leandro.garcia@mateusmais.com')
    time.sleep(1)
    page.fill('input#ember353', credenciais.senha)
    time.sleep(1)
    page.click('button[type=submit]')
    time.sleep(2)
    print("Login OK!")
    
    i = 0

    for pedido in pedidos:
        page.goto(f'https://app.konduto.com/orders/29877/{pedidos[i]}')
        time.sleep(5)
        
        ## scrape do valor dentro de <body>

        p_tags = page.inner_html('.order-left')
        soup = BeautifulSoup(p_tags, 'html.parser')
        p_valor = (soup.find_all('p')[1]).text.strip()
        p_valor = p_valor[3:]
        ## scrape do email dentro da classe .customer-details

        all_p_tags = soup.find_all('p')
        p_tags = page.inner_html('.customer-details')
        soup = BeautifulSoup(p_tags, 'html.parser')
        all_p_tags = soup.find_all('p')
        #p_valor = (soup.find_all('p')[1]).text.strip('R$') # dentro do body
        p_email = (soup.find_all('p')[6]).text.strip()
        #p_mercado = (soup.find_all('p')[43]).text.strip()
        #print(p_valor)
        #print(p_email)
        
        # scrape do mercado dentro da classe .new-payment
        #print(all_p_tags)
        p_tags = page.inner_html('.new-payment')
        soup = BeautifulSoup(p_tags, 'html.parser')
        p_mercado = (soup.find_all('p')[12]).text.strip()
        #print(p_mercado)
        
        lista.append([pedidos[i], p_mercado, p_email, p_valor])
        print(f"{i+1}o pedido OK!")
        i+=1
        

df = pd.DataFrame(lista, columns=['ID-Pedido', 'Estabelecimento', 'E-mail', 'Valor'])
df.to_csv('teste teste.csv')
    
#valor_total = (soup.find_all('td')[2]).text.strip()
#categoria = (soup.find_all('td')[4]).text.strip()
#estabelecimento = (soup.find_all('td')[5]).text.strip()
#email = (soup.find_all('td')[7]).text.strip()
#print(valor_total)
#print(categoria)
#print(estabelecimento)
#print(email)
