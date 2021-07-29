from yahoofinancials import YahooFinancials
import psycopg2
import matplotlib.pyplot as plt

#adds the data taken from the api to postgres db usdsar table
def add_to_db (connection, dates, rates):

    try:

        cur = connection.cursor()

        #insterts dates to the month column and rates to the rate column
        insert_data_query = """INSERT INTO usdsar(month, rate) VALUES (%s,%s)"""
        for i in range(len(dates)):
            cur.execute(insert_data_query, (dates[i], rates[i]))

        connection.commit()
    
    except Exception as e:
        print(e)
    
#uses the monthly exchange data json to return a list of the months' dates
def get_dates (monthly_exchange):
    dates = [monthly_exchange["SAR=X"]["prices"][0]["formatted_date"], monthly_exchange["SAR=X"]["prices"][1]["formatted_date"], monthly_exchange["SAR=X"]["prices"][2]["formatted_date"]]
    return dates

#uses the monthly exchange data json to return a list of the exchange rates
def get_rates (monthly_exchange):
    rates = [monthly_exchange["SAR=X"]["prices"][0]["high"], monthly_exchange["SAR=X"]["prices"][1]["high"], monthly_exchange["SAR=X"]["prices"][2]["high"]]
    return rates

#utilizes YahooFinancials api to return monthly exchange data in the form of json based on the
#given currency, start date and end date
def currency_exchange_data (currency, startDate, endDate):
    currencies = [currency]
    USDSAR = YahooFinancials(currencies)
    monthly_exchange = USDSAR.get_historical_price_data(startDate, endDate, 'monthly')
    return monthly_exchange

if __name__ == "__main__":

    connection = psycopg2.connect(
                                host = "DESKTOP-PVSDF04",
                                database = "postgres",
                                user = "postgres",
                                password="postgres123789",
                            )

    monthly_exchange = currency_exchange_data("SAR=X", '2021-04-28', '2021-07-28')

    dates = get_dates(monthly_exchange)
    rates = get_rates(monthly_exchange)

    add_to_db(connection, dates, rates)

    #plots a graph with dates on the x-axis and rates on the y-axis
    plt.plot(dates, rates)
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate USD/SAR')
    plt.show()

    connection.close()