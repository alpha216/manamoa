import json, re, base64, aiohttp, asyncio, os, aiofiles
import logging, logging.config
import requests
from bs4 import BeautifulSoup

header = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

def episode_lists(ur):
    linkss = []
    html = requests.get(ur, headers=header).text
    
    soup = BeautifulSoup(html, "lxml")

    passmydivs = soup.find_all("a", {"class": "item-subject"}, href=True)
    for i in passmydivs:
        linkss.append([i.contents[0].replace('\n', '').replace('체인쏘맨', '체인소맨').rstrip(), i['href']])

    return linkss


async def files(session, name, url ,li):
    try:
        loc = int(li.index(url))+1
        if not os.path.isfile(f'./manga/{name}/{str(loc)}.jpg'):
            logger.debug(f"{name} files started {url}")
            async with session.get(url) as response:
                    if response.status == 200:
                        f = await aiofiles.open(f'./manga/{name}/{str(loc)}.jpg', mode='wb')
                        await f.write(await response.read())
                        await f.close()
                        logger.debug(f"{name} file finished")
                    else: 
                        await asyncio.sleep(2)
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                f = await aiofiles.open(f'./manga/{name}/{str(loc)}.jpg', mode='wb')
                                await f.write(await response.read())
                                await f.close()
                                logger.debug(f"{name} file finished")
        else: logger.debug(f"{name} files are already exist {url}")
    except:
        async with aiohttp.ClientSession() as session:
            files(session, name, url, li)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def parse(html, url):
    name = url[0]
    logger.debug(f"{url[0]} parse started")
    
    json_string = re.search(r'var manamoa_img = (.*?);', html, re.S).group(1)
    res = base64.b64decode(json_string) 
    
    soup = BeautifulSoup(res, "lxml")

    passmydivs = soup.find_all("img", src=True)
    img_list =[i["src"] for i in passmydivs]
    
    return [name, [i for i in img_list]]


async def fetch_and_parse(session, url):
    link = url[1]
    logger.debug(f"{url[0]} started")
    html = await fetch(session, link)
    logger.debug(f"{url[0]} fetched")
    loop = asyncio.get_event_loop()
    # run parse(html) in a separate thread, and
    # resume this coroutine when it completes
    paras = await loop.run_in_executor(None, parse, html, url)
    logger.debug(f"{url[0]} parse finished")
    return await asyncio.gather(
        *(files(session, paras[0], url, paras[1]) for url in paras[1])
    )


async def main():
    logger.debug("main start")
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(fetch_and_parse(session, url) for url in linksss)
        )


if __name__ == "__main__":
    #Setup
    with open("info.log", 'w') as f: f.close()
    with open('logging.json', 'rt') as f: config = json.load(f)
    logging.config.dictConfig(config)
    logger = logging.getLogger()
    #Lists
    linksss = episode_lists('https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=303')
    with open('lss.txt', 'w') as f: f.write(str(linksss))
    for i in linksss:
         os.mkdir(f'./manga/{i[0]}')
    asyncio.run(main())
    print("finished")
    logger.debug("finished")