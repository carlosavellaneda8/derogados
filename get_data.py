import requests, re, time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def data_derogados(url):
    print("===============================================")
    print(f"Getting info from {url}")
    start = time.time()
    r = requests.get(url)
    s = BeautifulSoup(r.text, features="html.parser")

    arts = s.find_all("a", {"name": re.compile(r"^\d")}) # Get all articles
    arts_parent = [x.parent for x in arts] # Get all parents for every article
    arts_links = [x.find_all("a", href=True) for x in arts_parent] # Get all links contained in each parent

    df = pd.DataFrame(data = {
        "articulo": [x.text for x in arts],
        "all_text": [x.text for x in arts_parent],
        "link": [urljoin(url, x[0]["href"]) if len(x) >= 1 else "" for x in arts_links] # Get only the first link that appears in each article
        })

    df["derogado"] = df.all_text.str.contains("derogado")
    df = df.loc[df.articulo != ""]

    file_name = "output/" + url.rsplit("/", 1)[-1] + ".csv"
    df.loc[df.derogado].drop("derogado", axis=1).to_csv(file_name, index=False) # Save only those articles that are repealed
    print("===============================================")
    print(f"File saved as {file_name}")
    print(f"Spent {round(time.time() - start, )} seconds")

if __name__ == "__main__":
    url = "https://normograma.info/crc/docs/resolucion_crc_5050_2016.htm"
    data_derogados(url)
    # for url in urls:
    #     data_derogados(url)