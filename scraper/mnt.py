#!/usr/bin/env python3
import json
import re
from tqdm import tqdm
from chatgpt_wrapper import ChatGPT
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By

template = "Svet vie byť nepekným miestom, ale teraz je čas na pozitivu a optimizmus. Prepíš následujúce, zavše trochu nelichotivé, správy na správy lásky a porozumenia. Zachovaj ich približne rovnakú dĺžku a pokús sa zachovať aj formu. Dbaj na to, nech sú dostatočne umelecké, plné nezvyčajných slovných obratov. Neboj sa popustiť uzdu svojej fantázii. Prvú vetu obklop dvoma hviezdičkami **.\n\n"

firefox_dev_binary = FirefoxBinary("/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox")
options = webdriver.FirefoxOptions()
options.add_argument("-headless")
browser = webdriver.Firefox(firefox_binary=firefox_dev_binary, options=options)

browser.get("https://mnt.sk")

with open("../news.json") as fh:
    old_data = json.load(fh)

ids = set(x["id"] for x in old_data)

print("Scraping articles...")

data = []
articles = browser.find_elements(By.CLASS_NAME, "mnt-FeedArticle")
for article in tqdm(articles[:-1]):
    toolbar = article.find_element(By.CLASS_NAME, "mnt-toolbar")
    link_el = toolbar.find_element(By.TAG_NAME, "a")
    time_el = link_el.find_element(By.CLASS_NAME, "mnt-time")
    content_el = article.find_element(By.CLASS_NAME, "mnt-article").find_element(By.TAG_NAME, "p")

    time = time_el.get_attribute("textContent").lstrip()
    link = link_el.get_property("href")
    id = link.split("/")[-1]

    if id in ids:
        continue

    content = content_el.get_property("innerHTML")
    content = re.sub("</?strong>", "**", content)
    content = re.sub("</?a[^>]*>", "**", content)
    content = re.sub("&nbsp;", " ", content)
    data.append({
        "id": id,
        "time": time,
        "link": link,
        "content": content,
    })

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

print(len(data), "new articles")
print("Adding love, respect, and understanding...")

bot = ChatGPT()
for b in tqdm(batch(data, n=4), total=len(data) // 4 + (len(data) % 4 > 0), unit="batch"):
    texts = "\n\n".join(article["content"] for article in b)
    bot.new_conversation()
    response = bot.ask(template + texts)
    new_content = response.split("\n\n")[-len(b):]
    for c, d in zip(new_content, b):
        c = re.sub(r"\*\*", "<strong>", c, 1)
        c = re.sub(r"\*\*", "</strong>", c, 1)
        d["new_content"] = c

with open("../news.json", "w") as fh:
    json.dump([x for x in data if "new_content" in x] + old_data, fh, indent=2)

browser.quit()
