from config.configs_api import Api
from config.configs_data_covid import DataCovid
from config.configs_database import Database


if __name__ == "__main__":
    dadosCovid = DataCovid()

    # Insere os dados para a tabela de PAIS
    #dadosCovid.insertPais()

    # Insere os dados para a tabela de CASOS
    #dadosCovid.insertDados()