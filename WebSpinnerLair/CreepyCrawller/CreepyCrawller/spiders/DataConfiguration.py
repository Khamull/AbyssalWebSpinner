import os

class DataConfiguration:
    def __init__(self):
        import pandas
        self.myCsvFile = "dados_tratados.csv"
        self.myGeneratedCsvFile = ["stockCsvFile.csv", "fiiCsvFile.csv"]
        self.tagDictionary = {
                'Ticker'    : 'h1[title]::text'
            ,   'cName'     : 'h1 small::text'
            ,   'cValue'    : 'div[title="Valor atual do ativo"] strong.value::text'
            ,   'VPA'       : 'div[title="Indica qual o valor patrimonial de uma ação."] strong.value::text'
            ,   'LPA'       : 'div[title*="Indicar se a empresa é ou não lucrativa"] strong.value::text'
            ,   'DY'        : 'div[title="Dividend Yield com base nos últimos 12 meses"] strong.value::text'
            ,   'DV'        : 'div[title="Soma dos proventos distribuídos ano passado"] strong.value::text'
            ,   'PO'        : 'div.values strong[data-item="avg_F"]::text'
            ,   'PL'        : 'div[title="Dá uma ideia do quanto o mercado está disposto a pagar pelos lucros da empresa."] strong.value::text'
            ,   'PV'        : 'div[title="Facilita a análise e comparação da relação do preço de negociação de um ativo com seu VPA."] strong.value::text'
        }

        self.pd = pandas
        self.TickerList = []

        self.URL = 'https://statusinvest.com.br/acoes/'
    # Lê o arquivo CSV e cria um DataFrame
    def leCSV(self):
        print("Current Working Directory:", os.getcwd())
        # Get the absolute path to the current script
        script_dir = os.path.dirname(__file__)

        # Define the relative path to the CSV file
        csv_file_rel_path = 'CreepyCrawller/spiders/dados_tratados.csv'

        # Combine them to get the absolute path
        csv_file_path = os.path.join(script_dir, csv_file_rel_path)
        
        df = self.pd.read_csv(csv_file_path, encoding='utf-8', sep=',')
        #result = df.loc[df['STOCK_TYPE'] == 'AÇÃO', 'TICKER']
        # Filter tickers based on STOCK_TYPE and ending with 'F'
        result = df.loc[(df['STOCK_TYPE'] == 'AÇÃO') & (~df['TICKER'].str.endswith('F')), 'TICKER']
        unique_asst_values = result.drop_duplicates().tolist()
        self.TickerList = unique_asst_values or [
            'ENAT3'
        , 'CSNA3'
        , 'TAEE11'
        , 'TAEE4'
        , 'TAEE3'
        , 'ITSA3'
        , 'ITSA4'
        , 'KLBN4'
        , 'OIBR3'
        , 'RAIL3'
        , 'PETR3'
        , 'LEVE3'
        , 'MTRE3'
        , 'GRND3'
        , 'CEBR3'
        , 'BGIP4'
        , 'GGBR3'
        , 'CMIN3'
        , 'MELK3'
        , 'CRPG5'
        , 'BRAP4'
        , 'MRFG3'
        , 'PARD3'
        , 'AURE3'
        , 'BBSE3'
        , 'KEPL3'
        , 'GOAU4'
        , 'CBAV3'
        , 'JHSF3'
        , 'CIEL3'
        ]
