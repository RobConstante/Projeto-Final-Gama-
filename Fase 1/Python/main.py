from config.configs_data_covid import DataCovid
import os
import time
from datetime import date

if __name__ == "__main__":
    # Insere os dados para a tabela de PAIS
    #dadosCovid.insertPais()

    # Insere os dados para a tabela de CASOS e salva um arquivo .txt com os Países sem dados na API.
    #dadosCovid.insertDados()

    # Adiciona o summary do dia a tabela.
    #dadosCovid.updateToday()

    # Dados da evolução diária de Casos dos top 10 países.
    #res = dadosCovid.getTopNewConfirmedSQL()

    # Dados da evolução diária de Mortes dos top 10 países.
    #res = dadosCovid.getTopNewDeathsSQL()

    # Dados do total de mortes dos top 10 países.
    #res = dadosCovid.getTopDeaths()

    # Dados do total de casos dos top 10 países.
    #res = dadosCovid.getTopConfirmed()

    start = True
    data_atual = date.today()
    while start:
        os.system('cls')
        dadosCovid = DataCovid()
        print(120 * "-")
        print("|", "COVID-19", "|", sep=55 * " ", end="\n" + 120 * "-" + "\n")
        print("( 1 ) Evolução diária dos dez países com maior número de casos de COVID-19.")
        print("( 2 ) Evolução diária dos dez países com maior número de óbitos por COVID-19.")
        print("( 3 ) Lista dos dez países com maior número total de óbitos por COVID-19.")
        print("( 4 ) Lista dos dez países com maior número total de casos de COVID-19.")
        print("( 5 ) Sair")
        print(120 * "-")
        print("")
        try:
            opcao = int(input("Opcao: "))
            if opcao == 1:
                print('\n', dadosCovid.getTopNewConfirmedSQL(), '\n')
                csv = input('Gostaria de salvar o resultado em um CSV ? (s/n) ')
                if csv.lower() == 's':
                    dadosCovid.getTopNewConfirmedSQL().to_csv(f'csv\\CasosDiarios_{data_atual}.csv', sep='|')

                resp = input('Deseja voltar ao Menu? (s/n)\n')
                start = True if resp.lower() == 's' else False
            if opcao == 2:
                print('\n', dadosCovid.getTopNewDeathsSQL(), '\n')
                csv = input('Gostaria de salvar o resultado em um CSV ? (s/n) ')
                if csv == 's':
                    dadosCovid.getTopNewDeathsSQL().to_csv(f'csv\\MortesDiarias_{data_atual}.csv', sep='|')

                resp = input('Deseja voltar ao Menu? (s/n)\n')
                start = True if resp.lower() == 's' else False
            if opcao == 3:
                print('\n', dadosCovid.getTopDeaths(), '\n')
                csv = input('Gostaria de salvar o resultado em um CSV ? (s/n) ')
                if csv == 's':
                    dadosCovid.getTopDeaths().to_csv(f'csv\\MortesTotal_{data_atual}.csv', sep='|')

                resp = input('Deseja voltar ao Menu? (s/n)\n')
                start = True if resp.lower() == 's' else False
            if opcao == 4:
                print('\n', dadosCovid.getTopConfirmed(), '\n')
                csv = input('Gostaria de salvar o resultado em um CSV ? (s/n) ')
                if csv == 's':
                    dadosCovid.getTopConfirmed().to_csv(f'csv\\CasosTotal_{data_atual}.csv', sep='|')

                resp = input('Deseja voltar ao Menu? (s/n)\n')
                start = True if resp.lower() == 's' else False
            if opcao == 5:
                start = False
        except Exception:
            print("Opção invalida!\n")

        if opcao != 5:
            time.sleep(1)

    os.system('cls')
    print('Obrigado por usar o nosso programa.\nTodos os direitos reservados a equipe DataHeroes do curso GamaAcademy.')