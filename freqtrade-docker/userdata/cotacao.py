from pandas import DataFrame
from binance.client import Client
from api import Config
from colorama import Fore, Style
import json
import os

client = Client(Config.api_key, Config.api_secret)

def get_previous_prices():
    try:
        with open('previous_prices.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_current_prices(prices):
    with open('previous_prices.json', 'w') as file:
        json.dump(prices, file)

# Função para calcular a mudança percentual
def calculate_percentage_change(current_price, previous_price):
    if previous_price is None or previous_price == 0:
        return 0
    return ((current_price - previous_price) / previous_price) * 100

# Função para imprimir uma linha formatada
def print_formatted_row(symbol, current_price, percentage_change):
    color = Fore.GREEN if percentage_change >= 0 else Fore.RED
    formatted_row = f"| {symbol:<8}     |  {current_price:.6f}          |     {color}{percentage_change:+.2f}%{Style.RESET_ALL} |"
    print(formatted_row)

# Cotação de uma lista de moedas
def data_coins(coins, client, par):
    os.system("clear")
    coin = [i + str(par).upper() for i in coins]

    # Obtém todos os preços dos símbolos
    prices = DataFrame(client.get_all_tickers())
    prices["price"] = prices["price"].astype("float16")

    # Filtra os símbolos que contêm "USDT"
    data = prices[prices['symbol'].str.contains("USDT")]

    # Filtra os símbolos que não contêm 'DOWN'
    data = data[~data['symbol'].str.contains('DOWN')]

    # Filtra os símbolos da lista e ordena por preço
    selected_coins = data.loc[data.symbol.isin(coin)].sort_values(by='price', ascending=False)

    previous_prices = get_previous_prices()

    # Imprime cabeçalho da tabela
    print("+--------------+------------------+------------------+")
    print("| Symbol       |   Current Price  |    % Change      |")
    print("+--------------+------------------+------------------+")

    for index, row in selected_coins.iterrows():
        symbol = row['symbol']
        current_price = row['price']

        # Obtém o preço anterior
        previous_price = previous_prices.get(symbol, None)

        # Calcula a mudança percentual
        percentage_change = calculate_percentage_change(current_price, previous_price)

        # Exibe a linha formatada
        print_formatted_row(symbol, current_price, percentage_change)

        # Atualiza o preço anterior para a próxima iteração
        previous_prices[symbol] = current_price

    # Imprime a linha de fechamento da tabela
    print("+--------------+------------------+------------------+")

    # Salva os preços atuais para uso futuro
    save_current_prices(previous_prices)

if __name__ == "__main__":
    lista = ['BTC', 'CKB', 'ROSE', 'SFP', 'COS', 'VTHO', 'RSR', 'CHZ']
    data_coins(lista, client, 'USDT')
    print("\n")
