from config.configs_api import Api
from config.configs_database import Database
from datetime import datetime, date, timedelta
import pandas as pd


class DataCovid(object):
    consult = Database()
    api = Api()
    current_data = None
    top_countries = []
    data_atual = date.today()
    listaSemCasos = []

    def __init__(self):
        try:
            self.updateToday()
        except:
            print('Não foi possível fazer a atualização automática. Por favor, realize o método "DataCovid.updateToday()"')
            pass

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

        self.consult.executeDatabase(f"INSERT INTO PAIS (COD_ISO2, NOME) VALUES {values}")

    def insertDados(self):
        countries = 'https://api.covid19api.com/countries'
        jsonC = self.api.getDataAPI(countries)
        count = 0

        url = 'https://api.covid19api.com/total/dayone/country/'

        for country in jsonC:
            json = self.api.getDataAPI(url+country['Slug'])

            __lista = []
            __lista2 = []
            __lista3 = []

            __listaReturn = []
            __listaReturn2 = []
            __listaReturn3 = []

            values = ''
            values2 = ''
            values3 = ''

            for dados in json:
                iso = str(country['ISO2']).replace("'", "") if country['ISO2'] else ""
                data = datetime.strptime(str(dados['Date'][:10]), '%Y-%m-%d').date() if dados['Date'] else ''
                casos = int(dados['Confirmed']) if dados['Confirmed'] else ""
                mortes = int(dados['Deaths']) if dados['Deaths'] else ""
                add = f"('{iso}', '{data}', '{casos}', '{mortes}')"
                if len(__lista) < 1000:
                    __lista.append(add)
                elif len(__lista2) < 1000:
                    __lista2.append(add)
                else:
                    __lista3.append(add)


            for row in __lista:
                if row == __lista[len(__lista) - 1:len(__lista)][0]:
                    __listaReturn.append(row)
                else:
                    __listaReturn.append(row + ',')

            for row in __lista2:
                if row == __lista2[len(__lista2) - 1:len(__lista2)][0]:
                    __listaReturn2.append(row)
                else:
                    __listaReturn2.append(row + ',')

            for row in __lista3:
                if row == __lista3[len(__lista3) - 1:len(__lista3)][0]:
                    __listaReturn3.append(row)
                else:
                    __listaReturn3.append(row + ',')

            for linha in __listaReturn:
                values += linha

            for linha in __listaReturn2:
                values2 += linha

            for linha in __listaReturn3:
                values3 += linha

            count += 1
            if values:
                print(count)
                self.consult.executeDatabase(f"INSERT INTO CASOS (COD_ISO2, DATA, CASOS_CONFIRMADOS, MORTES) VALUES {values}")
            else:
                print(country['Country'] + ": Sem casos registrados.")
                self.listaSemCasos.append(country['Country'])

            if values2:
                print(country['Country'] + ": Lista 2")
                self.consult.executeDatabase(f"INSERT INTO CASOS (COD_ISO2, DATA, CASOS_CONFIRMADOS, MORTES) VALUES {values2}")

            if values3:
                print(country['Country'] + ": Lista 3\n")
                self.consult.executeDatabase(f"INSERT INTO CASOS (COD_ISO2, DATA, CASOS_CONFIRMADOS, MORTES) VALUES {values2}")


        print("Fim Insert")
        self.writeCountriesNotInApi()

    def writeCountriesNotInApi(self):
        self.listaSemCasos.sort()
        f = open(f"CountriesNotInAPI_{datetime.now().strftime('%Y%m%d')}.txt", "a")
        for linha in self.listaSemCasos:
            f.write(linha+"\n")
        f.close()

    def updateToday(self):
        url = 'https://api.covid19api.com/summary'
        current_result = self.api.getDataAPI(url)
        current_data = current_result['Countries']
        count = 0

        for dados in current_data:
            __lista = []
            __listaUpdate = []
            __listaReturn = []
            values = ''

            iso = str(dados['CountryCode']).replace("'", "") if dados['CountryCode'] else ""
            data = datetime.strptime(str(dados['Date'][:10]), '%Y-%m-%d').date() if dados['Date'] else ''
            casos = int(dados['TotalConfirmed']) if dados['TotalConfirmed'] else ''
            mortes = int(dados['TotalDeaths']) if dados['TotalDeaths'] else ''
            add = f"('{iso}', '{data}', '{casos}', '{mortes}')"
            addUpdate = [iso, data, casos, mortes]

            self.consult.cursor.execute(f"SELECT * FROM CASOS WHERE DATA = '{data}' AND COD_ISO2 = '{iso}'")
            exist = self.consult.cursor.fetchone()
            if exist is None:
                __lista.append(add)
            else:
                __listaUpdate.append(addUpdate)

            for row in __lista:
                if row == __lista[len(__lista) - 1:len(__lista)][0]:
                    __listaReturn.append(row)
                else:
                    __listaReturn.append(row + ',')

            for linha in __listaReturn:
                values += linha

            count += 1
            if values:
                print(count)
                self.consult.executeDatabase(f"INSERT INTO CASOS (COD_ISO2, DATA, CASOS_CONFIRMADOS, MORTES) VALUES {values}")

            if __listaUpdate:
                for linha in __listaUpdate:
                    self.consult.executeDatabase(f"UPDATE CASOS SET CASOS_CONFIRMADOS = {linha[2] if linha[2] else 0}, MORTES = {linha[3] if linha[3] else 0}"
                                                 f"WHERE COD_ISO2 = '{linha[0]}' AND Data = '{linha[1]}'")

        print(f"Dados do dia {dados['Date'][:10]} atualizados.")

    def getTopDeaths(self):
        data = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        var = 'MORTES'

        sql = "SELECT TOP 10 C.[COD_ISO2]" \
              "      ,P.[Nome]" \
              "      ,C.[DATA]" \
              "      ,C.[MORTES]" \
              "  FROM CASOS AS C" \
              "  INNER JOIN  PAIS AS P" \
              "  ON C.[COD_ISO2] = P.[COD_ISO2]" \
            f"  WHERE Data = '{data}'" \
            f"  ORDER BY {var} DESC;"

        df = pd.read_sql(sql, self.consult.conn)
        df.set_index('COD_ISO2', inplace=True)

        return df

    def getTopConfirmed(self):
        data = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        var = 'CASOS_CONFIRMADOS'

        sql = "SELECT TOP 10 C.[COD_ISO2]" \
              "      ,P.[Nome]" \
              "      ,C.[DATA]" \
              "      ,C.[CASOS_CONFIRMADOS]" \
              "  FROM CASOS AS C" \
              "  INNER JOIN  PAIS AS P" \
              "  ON C.[COD_ISO2] = P.[COD_ISO2]" \
             f"  WHERE Data = '{data}'" \
             f"  ORDER BY {var} DESC;"

        df = pd.read_sql(sql, self.consult.conn)
        df.set_index('COD_ISO2', inplace=True)
        return df

    def getTopNewDeathsSQL(self):
        hoje = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        ontem = date.today() - timedelta(1)

        sqlHoje = "SELECT C.[COD_ISO2]" \
              "      ,P.[Nome]" \
              "      ,C.[DATA]" \
              "      ,C.[MORTES]" \
              "  FROM CASOS AS C" \
              "  INNER JOIN  PAIS AS P" \
              "  ON C.[COD_ISO2] = P.[COD_ISO2]" \
            f"  WHERE Data = '{hoje}'" \
            f"  ORDER BY COD_ISO2;"

        sqlOntem = "SELECT C.[COD_ISO2]" \
                  "      ,P.[Nome]" \
                  "      ,C.[DATA]" \
                  "      ,C.[MORTES]" \
                  "  FROM CASOS AS C" \
                  "  INNER JOIN  PAIS AS P" \
                  "  ON C.[COD_ISO2] = P.[COD_ISO2]" \
                 f"  WHERE Data = '{ontem}'" \
                 f"  ORDER BY COD_ISO2;"

        dfHoje = pd.read_sql(sqlHoje, self.consult.conn)
        dfOntem = pd.read_sql(sqlOntem, self.consult.conn)

        dfHoje['MORTES_ONTEM'] = dfOntem['MORTES']

        dfHoje['NovasMortes'] = dfHoje['MORTES'] - dfHoje['MORTES_ONTEM']
        dfReturn = dfHoje.sort_values(by=['NovasMortes'] ,ascending=False)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        df = dfReturn[['COD_ISO2', 'Nome', 'DATA', 'NovasMortes']].head(10)
        df.set_index('COD_ISO2', inplace=True)

        return df

    def getTopNewConfirmedSQL(self):
        hoje = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        ontem = date.today() - timedelta(1)

        sqlHoje = "SELECT C.[COD_ISO2]" \
              "      ,P.[Nome]" \
              "      ,C.[DATA]" \
              "      ,C.[CASOS_CONFIRMADOS]" \
              "  FROM CASOS AS C" \
              "  INNER JOIN  PAIS AS P" \
              "  ON C.[COD_ISO2] = P.[COD_ISO2]" \
            f"  WHERE Data = '{hoje}'" \
            f"  ORDER BY COD_ISO2;"

        sqlOntem = "SELECT C.[COD_ISO2]" \
                  "      ,P.[Nome]" \
                  "      ,C.[DATA]" \
                  "      ,C.[CASOS_CONFIRMADOS]" \
                  "  FROM CASOS AS C" \
                  "  INNER JOIN  PAIS AS P" \
                  "  ON C.[COD_ISO2] = P.[COD_ISO2]" \
                 f"  WHERE Data = '{ontem}'" \
                 f"  ORDER BY COD_ISO2;"

        dfHoje = pd.read_sql(sqlHoje, self.consult.conn)
        dfOntem = pd.read_sql(sqlOntem, self.consult.conn)

        dfHoje['CASOS_CONFIRMADOS_ONTEM'] = dfOntem['CASOS_CONFIRMADOS']

        dfHoje['NovosCasos'] = dfHoje['CASOS_CONFIRMADOS'] - dfHoje['CASOS_CONFIRMADOS_ONTEM']
        dfReturn = dfHoje.sort_values(by=['NovosCasos'], ascending=False)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        df = dfReturn[['COD_ISO2', 'Nome', 'DATA', 'NovosCasos']].head(10)
        df.set_index('COD_ISO2', inplace=True)

        return df

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
        result = api.getDataAPI(url)
        return result