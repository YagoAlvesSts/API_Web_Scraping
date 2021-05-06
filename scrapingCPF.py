from datetime import datetime

class Scrapingcpf:

    def __init__(self, bs):
        self.html = bs

    def infos_cpf(self):
        data = {}

        try:
            data['CPF'] = self.html.find('b', text="CPF:").nextSibling.strip()
        except AttributeError:
            return {'Error': 'Não encontrado informações para esse CPF!'}


        data['Inscrição Estadual'] = self.html.find('b', text="Inscrição Estadual:").nextSibling.strip().replace("\xa0", " ")
        data['Razão Social'] = self.html.find('b', text="Razão Social:").nextSibling.strip()
        data['Nome Fantasia'] = self.html.find('b', text="Nome Fantasia:").nextSibling.strip()
        data['Unidade de Atendimento'] = self.html.find('b', text="Unidade de Atendimento:").nextSibling.strip()
        data['Unidade de Fiscalizacao'] = self.html.find('b', text="Unidade de Fiscalização:").nextSibling.strip()

        address = {}
        address['Logradouro'] = self.html.find('b', text="Logradouro:").nextSibling.strip()
        address['Numero'] = self.html.find('b', text="Número:").nextSibling.strip()
        address['Complemento'] = self.html.find('b', text="Complemento:").nextSibling.strip()
        address['Bairro/Distrito'] = self.html.find('b', text="Bairro/Distrito:").nextSibling.strip()
        address['CEP'] = self.html.find('b', text="CEP:").nextSibling.strip()
        address['Municipio'] = self.html.find('b', text="Município:").nextSibling.strip()
        address['UF'] = self.html.find('b', text="UF:").nextSibling.strip()
        address['Telefone'] = self.html.find('b', text="Telefone:").nextSibling.strip()
        address['Email'] = self.html.find('b', text="E-mail:").nextSibling.strip()
        address['Referencia'] = self.html.find('b', text="Referência:").nextSibling.strip()
        address['Localizacao'] = self.html.find('b', text="Localização:").nextSibling.strip()

        data['Endereco'] = address

        infos_complementary = {}
        date1 = self.html.find('b', text="Data de Inclusão do Contribuinte:").nextSibling.strip()
        date1 = datetime.strptime(date1, '%d/%m/%Y').date()
        date1 = date1.strftime('%d/%m/%Y')
        infos_complementary['Data de Inclusao do Contribuinte'] = date1

        infos_complementary['Atividade Economica Principal'] = self.html.find('b', text="Atividade Econômica Principal:").findNext().text.strip()

        secondary_activities = self.html.find_all("td", {"class": "style89"})
        activities = []
        for activitie in secondary_activities:
            activities.append(activitie.get_text('td'))

        infos_complementary['Atividade Economica Secundaria'] = activities
        infos_complementary['Unidade'] = self.html.find('b', text="Unidade:").nextSibling.strip()
        infos_complementary['Condicao'] = self.html.find('b', text="Condição:").nextSibling.strip()
        infos_complementary['Forma de pagamento'] = self.html.find('b', text="Forma de pagamento:").nextSibling.strip()
        infos_complementary['Situacao Cadastral Vigente'] = self.html.find('b', text="Situação Cadastral Vigente:").nextSibling.strip()


        data['Informacoes Complementares'] = infos_complementary

        date2 = self.html.find('b', text="Data da Consulta:").findNext().text.strip()
        date2 = datetime.strptime(date2, '%d/%m/%Y').date()
        date2 = date2.strftime('%d/%m/%Y')
        data['Data da Consulta'] = date2

        mailing_address = {}
        mailing_address['Endereco'] = self.html.find('b', text="Endereço:").nextSibling.strip()
        mailing_address['Complemento'] = self.html.find('b', text="Complemento:").nextSibling.strip()
        mailing_address['Referencia'] = self.html.find('b', text="Referência:").nextSibling.strip()
        mailing_address['Numero'] = self.html.find('b', text="Número:").nextSibling.strip()
        mailing_address['Bairro'] = self.html.find('b', text="Bairro:").nextSibling.strip()
        mailing_address['CEP'] = self.html.find('b', text="CEP:").nextSibling.strip()

        municipio = self.html.find("font", text="Endereço de Correspondência").findNext('b', text="Município:").nextSibling.strip()
        mailing_address['Municipio'] = municipio
        mailing_address['UF'] = self.html.find('b', text="UF:").nextSibling.strip()

        data['Endereco correspondecia'] = mailing_address

        return data