 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import mysql.connector
from datetime import datetime
import time

mydb = mysql.connector.connect(
  host="database-1.cju59kyu5adn.us-east-2.rds.amazonaws.com",
  port="3307",
  user="admin",
  passwd="Lr8T34HzAdMLs9aEDFfN",
  database="dfrexa"
)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'id':'1,2577'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '768dbcb5-6ff1-45cd-8080-e804974a0544',
}

session = Session()
session.headers.update(headers)

while True:
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    mycursor = mydb.cursor()
    sql = "UPDATE realtime_price SET usd_price = '" + str(data['data']['1']['quote']['USD']['price']) + "', updated_at='" + dt_string + "' WHERE coin_type = 'bitcoin'"
    mycursor.execute(sql)
    mydb.commit()

    mycursor = mydb.cursor()
    sql = "UPDATE realtime_price SET usd_price = '" + str(data['data']['2577']['quote']['USD']['price']) + "', updated_at='" + dt_string + "' WHERE coin_type = 'ravencoin'"
    mycursor.execute(sql)
    mydb.commit()

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

  time.sleep(300)