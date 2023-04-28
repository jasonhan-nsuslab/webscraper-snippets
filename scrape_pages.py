import asyncio
from multiprocessing import Process, Queue, Lock
from pyppeteer import launch
from db import local_db

query = "INSERT INTO casino.games VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
gameNameSelector = "div.slotAttrReview > h3"
attrsTableSelector = "div.slotAttrReview > table > tbody > tr"

async def goto(database, queue):
    try:
        browser = await launch({'args': ['--proxy-server=10.10.50.53:6010'], 'headless': False })
        page = await browser.newPage()
        while not queue.empty():
            url = queue.get()
            curGame = {
                "Name": None,
                "Provider": None,
                "Release Date": None,
                "Wide release date": "N/A",
                "Type": None,
                "RTP": None,
                "Variance": None,
                "Hit Frequency": None,
                "Max Win": None,
                "Min bet $, €, £": None,
                "Max bet $, €, £": None,
                "Layout": None,
                "Betways": None,
                "Features": None,
                "Theme": None,
                "Objects": None,
                "Genre": None,
                "Other tags": None,
                "Technology": None,
                "Game Size": None,
                "Last Update": None,
                "url": url
            }
            await page.goto(url)
            print(url)
            
            attrsTable = await page.querySelectorAll(attrsTableSelector)
            if not attrsTable:
                continue
            
            for attrs in attrsTable:
                text = await page.evaluate("(element => element.textContent)", attrs)
                text = " ".join(text.split())
                if text:
                    attr = text.split(": ", maxsplit=1)
                    curGame[attr[0]] = attr[1]
            gameName = await page.evaluate("(element => element.textContent)", await page.querySelector(gameNameSelector))
            curGame["Name"] = " ".join(gameName.split(" ")[:-1])
            database.cur.execute(query, (
                    curGame["Name"],
                    curGame["Provider"],
                    curGame["Release Date"],
                    curGame["Wide release date"],
                    curGame["Type"],
                    curGame["RTP"],
                    curGame["Variance"],
                    curGame["Hit Frequency"],
                    curGame["Max Win"],
                    curGame["Min bet $, €, £"],
                    curGame["Max bet $, €, £"],
                    curGame["Layout"],
                    curGame["Betways"],
                    curGame["Features"],
                    curGame["Theme"],
                    curGame["Objects"],
                    curGame["Genre"],
                    curGame["Other tags"],
                    curGame["Technology"],
                    curGame["Game Size"],
                    curGame["Last Update"],
                    curGame["url"]
                )
            )
            database.conn.commit()
    
    except Exception as e:
        print(e)
        await browser.close()
        exit()
    finally:
        await browser.close()
        exit()


def runner(database, queue):
    asyncio.run(goto(database, queue))
    exit()

def main():
    q = Queue()
    with open("output.txt", "r") as file:
        for url in file:
            q.put(url)

    for num in range(20):
        Process(target=runner, args=(local_db(), q)).start()
    
    

if __name__ == "__main__":
    main()
