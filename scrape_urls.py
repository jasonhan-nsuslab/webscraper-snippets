import asyncio
import time
from pyppeteer import launch
from db import local_db

async def goto(database):
    urls = []
    with open("output.txt", "w") as file:
        try:
            browser = await launch({'args': ['--proxy-server=10.10.50.53:6010'], 'headless': False })
            page = await browser.newPage()
            loadGamesSelector = "a[href='#anchorFltrList']"
            await page.goto('https://slotcatalog.com/en/The-Best-Slots')
            await page.waitForSelector(loadGamesSelector)
            await page.click(loadGamesSelector)
            
            for gamePage in range(2, 1054):
                nextPageSelector = "a[onClick*='val({0})']".format(gamePage)
                try:
                    await page.waitForSelector(nextPageSelector)
                except:
                    time.sleep(600)
                    await page.reload()
                    await page.waitForSelector(nextPageSelector)
                games = await page.querySelectorAll("a[href*='/en/slots/']")
                for game in games:
                    url = await page.evaluate('(element => element.href)', game)
                    url = url.split("#")[0].split("?")[0]
                    if url not in urls:
                        print(url)
                        urls.append(url)
                        file.write(url+"\n")
                time.sleep(15)
                await page.click(nextPageSelector)
        except Exception as e:
            print(e)
            await browser.close()
        finally:
            await browser.close()


async def main():
    await goto(local_db())

if __name__=="__main__":
    asyncio.run(main())