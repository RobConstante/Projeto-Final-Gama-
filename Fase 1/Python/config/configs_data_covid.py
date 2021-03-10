from config.configs_api import Api
from config.configs_database import Database
from datetime import datetime, date


class DataCovid(object):
    consult = Database()
    api = Api()
    current_data = None
    top_countries = []
    data_atual = date.today()

    #def __init__(self):
    #    self.updateToday()

    def insertPais(self):
        url = 'https://api.covid19api.com/countries'
        json = self.api.getDataAPI(url)

        __lista = []
        __listaReturn = []
        values = ''

        for country in json:
            pais = str(country['Country']).replace("'","") if country['Country'] else ""
            iso = str(country['ISO2']).replace("'","") if country['ISO2'] else ""
            add = f"('{iso}', '{pais}')"
            __lista.append(add)

        for row in __lista:
            if row == __lista[len(__lista) - 1:len(__lista)][0]:
                __listaReturn.append(row)
            else:
                __listaReturn.append(row + ',')

        for linha in __listaReturn:
            values += linha

        #print("Inicio Insert")
        self.consult.executeDatabase(f"INSERT INTO PAIS (COD_ISO2, NOME) VALUES {values}")
        #print("Fim Insert")

    def insertDados(self):
        countries = 'https://api.covid19api.com/countries'
        jsonC = self.api.getDataAPI(countries)

        url = 'https://api.covid19api.com/dayone/country/'

        for country in jsonC:
            json = self.api.getDataAPI(url+country['Slug'])

            __lista = []
            __listaReturn = []
            values = ''

            for dados in json:
                iso = str(country['ISO2']).replace("'", "") if country['ISO2'] else ""
                data = datetime.strptime(dados['Date'][:10], '%Y-%m-%d').date() if dados['Date'] else ""
                casos = int(dados['Confirmed']) if dados['Confirmed'] else ""
                mortes = int(dados['Deaths']) if dados['Deaths'] else ""

                add = f"('{iso}', '{data}', '{casos}', '{mortes}')"
                __lista.append(add)

            for row in __lista:
                if row == __lista[len(__lista) - 1:len(__lista)][0]:
                    __listaReturn.append(row)
                else:
                    __listaReturn.append(row + ',')

            for linha in __listaReturn:
                values += linha

            if values:
                print(country['Country'])
                self.consult.executeDatabase(f"INSERT INTO CASOS (COD_ISO2, DATA, CASOS_CONFIRMADOS, MORTES) VALUES {values}")
            else:
                print(country['Country'] + ": Sem casos registrados.")
            # print("Fim Insert")




    def updateToday(self):
        Data = self.consult.executeDatabase("SELECT MAX(Date) FROM COUNTRIES")
        #if Data == self.data_atual:

        result = self.countries()
        countries = result

        current_result = self.data()
        current_data = current_result['Countries']

        for country in countries:
            self.consult.executeDatabase("SELECT * FROM COUNTRIES WHERE ISO2 = ?", country['ISO2'])
            exist = self.consult.cursor.fetchone()
            if exist is None:
                self.consult.executeDatabase("INSERT INTO COUNTRIES (Country, ISO2) VALUES (?, ?)", country['Country'], country['ISO2'])

            for current_country in current_data:
                self.consult.executeDatabase(
                    "INSERT INTO DATA_COVID (ISO2, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered, Date ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    current_country['CountryCode'],
                    current_country['NewConfirmed'],
                    current_country['TotalConfirmed'],
                    current_country['NewDeaths'],
                    current_country['TotalDeaths'],
                    current_country['NewRecovered'],
                    current_country['TotalRecovered'],
                    current_country['Date'][:10])

                #if current_country["CountryCode"] == id_country:
                    #consult.executeDatabase("INSERT INTO DATA_COVID (TotalConfirmed, TotalDeaths, ID_PAISES, DATA ) VALUES (?, ?, ?)", current_country['TotalConfirmed'], current_country["TotalDeaths"], id_country, current_country["Date"])
                #else:
                #    consult.executeDatabase("UPDATE DATA_COVID SET TotalConfirmed = ?, TotalDeaths = ? WHERE ID_PAISES = ?", current_country['TotalConfirmed'], current_country["TotalDeaths"], id_country)


def topTen(self, campo: str, periodo: str):
    col = campo
    if periodo == 'today':
        data_atual = date.today()

    consult = Database()
    topCountries = consult.executeDatabase(
        f"SELECT COUNTRIES.Country, DATA.{col} FROM "
        f"(SELECT ISO2,{col} FROM DATA_COVID) DATA"
        f" LEFT JOIN"
        f" (SELECT ISO2, Country FROM COUNTRIES) COUNTRIES"
        f" ON DATA.ISO2 = COUNTRIES.ISO2"
        f"ORDER BY DATA.{col} DESC LIMIT 10")
    return topCountries
    #for row in topCountries.fetchall():
    #    self.top_countries.append(row)


def getTopDeaths(self):
    self.topTen()
    result = f""
    for country in top_countries.fetchall():
        for current_country in current_data:
            if current_country["CountryCode"] == country:
                result += f"{current_country['Country']} Total de mortes é {current_data['TotalDeaths']} \n"
                break
    return result


def getTopConfirmed(self):
    self.topTen()
    result = f""
    for country in top_countries.fetchall():
        for current_country in current_data:
            if current_country["CountryCode"] == country:
                result += f"{current_country['Country']} Total de casos confirmados é {current_data['TotalConfirmed']} \n"
                break
    return result


def getTopNewDeaths(self):
    self.topTen()
    result = f""
    for country in top_countries.fetchall():
        for current_country in current_data:
            if current_country["CountryCode"] == country:
                result += f"{current_country['Country']} Número de novas mortes é {current_data['NewDeaths']} \n"
                break
    return result


def getTopNewConfirmed(self):
    self.topTen()
    result = f""
    for country in top_countries.fetchall():
        for current_country in current_data:
            if current_country["CountryCode"] == country:
                result += f"{current_country['Country']} Número de novos casos confirmados é {current_data['NewConfirmed']} \n"
                break
    return result


def countries(self):
    url = 'https://api.covid19api.com/countries'
    api = Api()
    self.result = api.getDataAPI(url)
    return self.result


def data(self):
    url = 'https://api.covid19api.com/summary'
    api = Api()
    self.result = api.getDataAPI(url)
    return self.result