import smtplib
import requests
import lxml
from bs4 import BeautifulSoup
import os

URL = "https://www.amazon.com/Nintendo-Controller-Super-Smash-Bros-switch/dp/B07HC2F97Q/ref=sr_1_2?crid=KVUIARRY1PJ1&keywords=gamecube+controller&qid=1646060759&sprefix=%2Caps%2C88&sr=8-2"
BUY_PRICE = 50
MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]

header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"}

response = requests.get(URL, headers=header)
response.raise_for_status
webpage_content = response.text
soup = BeautifulSoup(webpage_content, "lxml")
price = float(soup.find("span", id = "priceblock_ourprice").get_text().strip("$"))

title = soup.find(id="productTitle").get_text().strip()

if price < BUY_PRICE:
    message = f"{title} is now ${price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="mauriciomatos44@gmail.com",
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}"
        )