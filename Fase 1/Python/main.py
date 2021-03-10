#importando biblioteca requests e dando alias rq
import requests as rq
import json
import pyodbc

class API(object):
    def getDataAPI(self, url):
        #send_url = url; 
        #request = requests.get(send_url)
        #result = request.json()
        
        dados = rq.get(url)
        dados2 = json.loads(dados.content)

        return dados2

class Database(object):
    conn ="";
    cursor = "";
    
    def __init__(self, json_covid=None):
        self.connectDatabase()

    def connect(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LOCALHOST;'
                      'Database=Projeto_Final;'
                      'UID=projeto;'
                      'PWD=dados@ibge1;')

        self.cursor = conn.cursor()
    
    def close(self):
        self.conn.close()

    def execute(self, query):
        exec_query = query;

        #cursor.fast_executemany = True
        #cursor.executemany(exec_query)

        cursor.execute(exec_query)
        cursor.commit()

class dataCovid(object):    
    current_data = None;
    top_countries= []

    def countries(self):
        url = 'https://api.covid19api.com/countries'
        api = API()
        self.result = api.getDataAPI(url)
        return self.result;

    def data(self):
        url = 'https://api.covid19api.com/summary'
        api = API()
        self.result = api.getDataAPI(url)
        return self.result;
    
    def allData(self):
        url = 'https://api.covid19api.com/all'
        api = API()
        self.result = api.getDataAPI(url)
        return self.result;

    

    """def __init__(self, json_covid=None):
        #self.updateToday()

    def updateToday(self):
        result = self.countries();
        countries = result   
      
        current_result = self.data();
        current_data = current_result['Countries'] 
        
        for country in countries:
            id_country   = country['ISO2'];            
            name_country = str(country['Country']);
            #consult = Database()
            #consult.executeDatabase("SELECT * FROM COUNTRIES WHERE id_country = ?", id_country)
            #exist = consult.cursor.fetchone()
            #if exist is None:
              #consult.executeDatabase("INSERT INTO COUNTRIES VALUES (?, ?)", id_country, name_country)                
              for current_country in current_data:
                totalConfirmed = int(current_country["TotalConfirmed"])
                totalDeaths = int(current_country["TotalDeaths"])
                if current_country["CountryCode"] == id_country:                
                  #consult.executeDatabase("INSERT INTO DATA_COVID (TotalConfirmed, TotalDeaths, id_country ) VALUES (?, ?, ?)", current_country['TotalConfirmed'], current_country["TotalDeaths"], id_country) 
                  break               
            #else:
              #consult.executeDatabase("UPDATE DATA_COVID SET TotalConfirmed = ?, TotalDeaths = ? WHERE id_country = ?", current_country['TotalConfirmed'], current_country["TotalDeaths"], id_country) 
    def topTen(self):
      #consult = Database()
      topCountries = consult.executeDatabase("SELECT DATA.id_country FROM DATA_COVID AS DATA, COUNTRIES WHERE DATA.id_country = COUNTRIES._id_country ORDER BY TotalConfirmed LIMIT = 10")
      for row in topCountries.fetchall():
        top_countries.append(row);

    def getTopDeaths(self):
      self.topTen()
      result =f"";
      for country in top_countries.fetchall():
        for current_country in current_data:          
          if current_country["CountryCode"] == country:  
            result += f"{current_country['Country']} Total de mortes é {current_data['TotalDeaths']} \n"
            break
      return result;"""

    def getTopConfirmed(self):
      self.topTen()
      result =f"";
      for country in top_countries.fetchall():
        for current_country in current_data:          
          if current_country["CountryCode"] == country:  
            result += f"{current_country['Country']} Total de casos confirmados é {current_data['TotalConfirmed']} \n"
            break
      return result;

    def getTopNewDeaths(self):
      self.topTen()
      result =f"";
      for country in top_countries.fetchall():
        for current_country in current_data:          
          if current_country["CountryCode"] == country:  
            result += f"{current_country['Country']} Número de novas mortes é {current_data['NewDeaths']} \n"
            break
      return result;

    def getTopNewConfirmed(self):
      self.topTen()
      result =f"";
      for country in top_countries.fetchall():
        for current_country in current_data:          
          if current_country["CountryCode"] == country:  
            result += f"{current_country['Country']} Número de novos casos confirmados é {current_data['NewConfirmed']} \n"
            break
      return result;
            

        
teste = dataCovid().countries()

print(teste[10]['ISO2'])
print(teste[10]['Country'])

Database.connect
