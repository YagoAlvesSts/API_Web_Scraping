# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import traceback
import requests
from bs4 import BeautifulSoup
import urllib3
import re
urllib3.disable_warnings()
from scrapingCPF import Scrapingcpf
from scrapingCNPJ import Scrapingcnpj

class Webscraping:

    def __init__(self, data):
        self.infos = data
        self.req = requests.Session()
        self.type = ''

    def get_data(self):
        url = 'https://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/consultaBa.asp'
        response = self.req.get(url, verify=False)

        self.infos = self.infos.replace('.', '').replace('-', '').replace('/', '')

        if len(self.infos) == 11:
            self.type = 1
            if not (self.validate_cpf()):
                return [{'Error': 'Insira um CPF válido!'}]
        elif len(self.infos) == 14:
            self.type = 0
            if not self.validate_cnpj():
               return {'Error': 'Insira um CNPJ válido!'}
        else:
            return {'Error': 'Insira um CPF ou CNPJ válido!'}


        if response.status_code == 200:

            url = 'https://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/result.asp'

            if self.type == 1:
                payload = {
                'sefp': '1',
                'estado': 'BA',
                'CGC': '',
                'CPF': self.infos,
                'B3': 'CPF+->',
                'IE': ''
                }
            if self.type == 0:
                payload = {
                    'sefp': '1',
                    'estado': 'BA',
                    'CGC': self.infos,
                    'B1': 'CNPJ++->',
                    'CPF': '',
                    'IE': ''
                }

            response = self.req.get(url, data=payload)


            return self.scraping(response.content.decode('utf-8'))


        else:
            return {'Error ao acessar url': url}

    def scraping(self, html):

        bs = BeautifulSoup(html, 'html.parser')

        if self.type == 1:
            scrapingcpf = Scrapingcpf(bs)
            data = scrapingcpf.infos_cpf()
        if self.type == 0:
            scrapingcnpj = Scrapingcnpj(bs)
            data = scrapingcnpj.infos_cnpj()



        data = [data]

        return {'data': data}


    def validate_cpf(self):
        cpf = ''.join(re.findall(r'\d', str(self.infos)))

        old = [int(d) for d in cpf]
        new = old[:9]
        while len(new) < 11:
            rest = sum([v * (len(new) + 1 - i) for i, v in enumerate(new)]) % 11

            verifying_digit = 0 if rest <= 1 else 11 - rest

            new.append(verifying_digit)

        if new == old:
            return True
        
        return False

    def validate_cnpj(self):
        cnpj = ''.join(re.findall(r'\d', str(self.infos)))

        whole = list(map(int, cnpj))
        new = whole[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(new) < 14:
            r = sum([x * y for (x, y) in zip(new, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            new.append(f)
            prod.insert(0, 6)

        if new == whole:
            return True

        return False








