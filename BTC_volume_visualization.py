import requests
from lxml import html
import matplotlib.pyplot as plt

with open('2023_dates.txt') as f:
    dates = f.read().splitlines()

with open('2023 - Copy.txt') as f:
    dates2 = f.read().splitlines()

volumes = []
volumes2 = []

for date in dates:
    url = f'https://coinmarketcap.com/historical/{date}/'
    response = requests.get(url)
    content = response.content

    tree = html.fromstring(content)

    extracted = False

    while not extracted:
        try:
            volume = tree.xpath('/html/body/div[1]/div[1]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[1]/td[7]/a/text()')
            volume = volume[0].strip('$')
            volume = round(float(volume.replace(',', '')))
            print(volume)

            if date in dates2:
                volumes2.append(volume)
            volumes.append(volume)
            extracted = True
        except IndexError:
            print(f"No data found for {date}. Retrying...")

x_axis_dates = [date for date in dates if date.endswith('01')]

avg_volume_all = sum(volumes) / len(volumes)
avg_volume_full_moon = sum(volumes2) / len(volumes2) 

plt.plot(dates, volumes)
plt.scatter(dates2, volumes2, c='red')
plt.axhline(y=avg_volume_all, color='blue', linestyle='--', label='Average Volume (All Days): {:.2f}'.format(avg_volume_all))
plt.axhline(y=avg_volume_full_moon, color='red', linestyle='--', label='Average Volume (Full Moon Days): {:.2f}'.format(avg_volume_full_moon))

for i in range(0, len(volumes2)-1, 2):
    plt.plot([dates2[i], dates2[i+1]], [volumes2[i], volumes2[i+1]], c='red')

plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price Over Time')
plt.xticks(x_axis_dates, rotation=45)
plt.legend()
plt.show()