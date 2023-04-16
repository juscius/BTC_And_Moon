import requests
from lxml import html
import matplotlib.pyplot as plt

with open('2014_dates.txt') as f:
    dates = f.read().splitlines()

with open('2014_full_moon.txt') as f:
    dates2 = f.read().splitlines()

prices = []
prices2 = []

for date in dates:
    # Construct URL and fetch HTML content
    url = f'https://coinmarketcap.com/historical/{date}/'
    response = requests.get(url)
    content = response.content

    tree = html.fromstring(content)

    extracted = False

    while not extracted:
        try:
            price = tree.xpath('/html/body/div[1]/div[1]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[1]/td[5]/div/text()')

            price = price[0].strip('$')
            price = float(price.replace(',', ''))
            print(price)

            if date in dates2:
                prices2.append(price)
            prices.append(price)
            extracted = True
        except IndexError:
            print(f"No data found for {date}. Retrying...")

x_axis_dates = [date for date in dates if date.endswith('01')]

plt.plot(dates, prices)
plt.scatter(dates2, prices2, c='red')

for i in range(0, len(prices2)-1, 2):
    plt.plot([dates2[i], dates2[i+1]], [prices2[i], prices2[i+1]], c='red')

plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price Over Time')
plt.xticks(x_axis_dates, rotation=45)
plt.show()