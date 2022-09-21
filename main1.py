import json, re, base64, aiohttp, asyncio, os, aiofiles
import logging, logging.config, json
import requests
from bs4 import BeautifulSoup

header = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
linksss = [
    ['체인소맨(전기톱맨) 104화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=167727&spage=1'], ['체인소맨(전기톱맨) 103화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=166306&spage=1'], ['체인소맨(전기톱맨) 102화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=165474&spage=1'], ['체인소맨(전기톱맨) 101화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=164442&spage=1'], ['체인소맨(전기톱맨) 100화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=164078&spage=1'], ['체인소맨(전기톱맨) 99화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=163641&spage=1'], ['체인소맨(전기톱맨) 98화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=163191&spage=1'], ['체인소맨(전기톱맨) 97화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48630&spage=1'], ['체인소맨(전기톱맨) 96화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48624&spage=1'], ['체인소맨(전기톱맨) 95화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48619&spage=1'], ['체인소맨(전기톱맨) 94화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48613&spage=1'], ['체인소맨(전기톱맨) 93화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48608&spage=1'], ['체인소맨(전기톱맨) 92화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48602&spage=1'], ['체인소맨(전기톱맨) 91화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48596&spage=1'], ['체인소맨(전기톱맨) 90화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48590&spage=1'], ['체인소맨(전기톱맨) 89화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48584&spage=1'], ['체인소맨(전기톱맨) 88화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48578&spage=1'], ['체인소맨(전기톱맨) 87화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48572&spage=1'], ['체인소맨(전기톱맨) 86화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48566&spage=1'], ['체인소맨(전기톱맨) 85화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48560&spage=1'], ['체인소맨(전기톱맨) 84화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48554&spage=1'], ['체인소맨(전기톱맨) 83화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48549&spage=1'], ['체인소맨(전기톱맨) 82화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48543&spage=1'], ['체인소맨(전기톱맨) 81화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48536&spage=1'], ['체인소맨(전기톱맨) 80화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48530&spage=1'], ['체인소맨(전기톱맨) 79화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48524&spage=1'], ['체인소맨(전기톱맨) 78화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48518&spage=1'], ['체인소맨(전기톱맨) 77화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48513&spage=1'], ['체인소맨(전기톱맨) 76화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48507&spage=1'], ['체인소맨(전기톱맨) 75화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48501&spage=1'], ['체인소맨(전기톱맨) 74화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48495&spage=1'], ['체인소맨(전기톱맨) 73화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48489&spage=1'], ['체인소맨(전기톱맨) 72화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48483&spage=1'], ['체인소맨(전기톱맨) 71화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48478&spage=1'], ['체인소맨(전기톱맨) 70화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48472&spage=1'], ['체인소맨(전기톱맨) 69화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48466&spage=1'], ['체인소맨(전기톱맨) 68화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48460&spage=1'], ['체인소맨(전기톱맨) 67화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48454&spage=1'], ['체인소맨(전기톱맨) 66화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48448&spage=1'], ['체인소맨(전기톱맨) 65화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48442&spage=1'], ['체인소맨(전기톱맨) 64화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48436&spage=1'], ['체인소맨(전기톱맨) 63화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48431&spage=1'], ['체인소맨(전기톱맨) 62화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48425&spage=1'], ['체인소맨(전기톱맨) 61화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48419&spage=1'], ['체인소맨(전기톱맨) 60화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48414&spage=1'], ['체인소맨(전기톱맨) 59화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48408&spage=1'], ['체인소맨(전기톱맨) 58화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48400&spage=1'], ['체인소맨(전기톱맨) 57화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48395&spage=1'], ['체인소맨(전기톱맨) 56화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48390&spage=1'], ['체인소맨(전기톱맨) 55화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48383&spage=1'], ['체인소맨(전기톱맨) 54화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48378&spage=1'], ['체인소맨(전기톱맨) 53화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48372&spage=1'], ['체인소맨(전기톱맨) 52화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48366&spage=1'], ['체인소맨(전기톱맨) 51화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48360&spage=1'], ['체인소맨(전기톱맨) 50화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48354&spage=1'], ['체인소맨(전기톱맨) 49화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48347&spage=1'], ['체인소맨(전기톱맨) 48화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48341&spage=1'], ['체인소맨(전기톱맨) 47화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48334&spage=1'], ['체인소맨(전기톱맨) 46화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48329&spage=1'], ['체인소맨(전기톱맨) 45화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48324&spage=1'], ['체인소맨(전기톱맨) 44화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48317&spage=1'], ['체인소맨(전기톱맨) 43화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48311&spage=1'], ['체인소맨(전기톱맨) 42화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48303&spage=1'], ['체인소맨(전기톱맨) 41화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48297&spage=1'], ['체인소맨(전기톱맨) 40화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48291&spage=1'], ['체인소맨(전기톱맨) 39화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48286&spage=1'], ['체인소맨(전기톱맨) 38화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48281&spage=1'], ['체인소맨(전기톱맨) 37화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48275&spage=1'], ['체인소맨(전기톱맨) 36화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48269&spage=1'], ['체인소맨(전기톱맨) 35화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48263&spage=1'], ['체인소맨(전기톱맨) 34화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48257&spage=1'], ['체인소맨(전기톱맨) 33화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48251&spage=1'], ['체인소맨(전기톱맨) 32화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48245&spage=1'], ['체인소맨(전기톱맨) 31화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48239&spage=1'], ['체인소맨(전기톱맨) 30화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48234&spage=1'], ['체인소맨(전기톱맨) 29화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48228&spage=1'], ['체인소맨(전기톱맨) 28화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48222&spage=1'], ['체인소맨(전기톱맨) 27화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48216&spage=1'], ['체인소맨(전기톱맨) 26화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48210&spage=1'], ['체인소맨(전기톱맨) 25화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48204&spage=1'], ['체인소맨(전기톱맨) 24화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48198&spage=1'], ['체인소맨(전기톱맨) 23화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48192&spage=1'], ['체인소맨(전기톱맨) 22화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48186&spage=1'], ['체인소맨(전기톱맨) 21화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48180&spage=1'], ['체인소맨(전기톱맨) 20화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48174&spage=1'], ['체인소맨(전기톱맨) 19화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48168&spage=1'], ['체인소맨(전기톱맨) 18화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48163&spage=1'], ['체인소맨(전기톱맨) 17화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48158&spage=1'], ['체인소맨(전기톱맨) 번외편', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48153&spage=1'], ['체인소맨(전기톱맨) 16화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48146&spage=1'], ['체인소맨(전기톱맨) 15화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48138&spage=1'], ['체인소맨(전기톱맨) 14화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48133&spage=1'], ['체인소맨(전기톱맨) 13화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48128&spage=1'], ['체인소맨(전기톱맨) 12화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48120&spage=1'], ['체인소맨(전기톱맨) 11화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48114&spage=1'], ['체인소맨(전기톱맨) 10화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48108&spage=1'], ['체인소맨(전기톱맨) 9화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48102&spage=1'], ['체인소맨(전기톱맨) 8화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48097&spage=1'], ['체인소맨(전기톱맨) 7화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48091&spage=1'], ['체인소맨(전기톱맨) 6화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48086&spage=1'], ['체인소맨(전기톱맨) 5화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48080&spage=1'], ['체인소맨(전기톱맨) 4화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48074&spage=1'], ['체인소맨(전기톱맨) 3화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48068&spage=1'], ['체인소맨(전기톱맨) 2화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48062&spage=1'], ['체인소맨(전기톱맨) 1화', 'https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=48056&spage=1']]

def wait():
    async def get_site_content(i):
        async with aiohttp.ClientSession() as session:
            async with session.get(i) as resp:
                text = await resp.read()
                
        return text

    async def req(ur):
        html = requests.get(ur, headers=header).text
        

        matched = re.search(r'var manamoa_img = (.*?);', html, re.S)
        json_string = matched.group(1)
        res = base64.b64decode(json_string) 
        
        img_list = []
        soup = BeautifulSoup(res, "lxml")

        passmydivs = soup.find_all("img", src=True)
        for i in passmydivs:
            img_list.append(i['src'])


    async def feach1(url):
        link = url[1]
        name = url[0]
        os.mkdir(f'./manga/{name}')

        html = await requests.get(link, headers=header).text
        
        json_string = await re.search(r'var manamoa_img = (.*?);', html, re.S).group(1)
        res = await base64.b64decode(json_string) 
        
        soup = await BeautifulSoup(res, "lxml")
        passmydivs = await soup.find_all("img", src=True)
        img_list = [i["src"] for i in passmydivs]
        asyncio.gather(*[files(name, i) for i in img_list])

    # async def main():
    #     asyncio.gather(*[feach(i) for i in linksss])

def episode_lists(ur):
    linkss = []
    html = requests.get(ur, headers=header).text
    
    soup = BeautifulSoup(html, "lxml")

    passmydivs = soup.find_all("a", {"class": "item-subject"}, href=True)
    for i in passmydivs:
        linkss.append([i.contents[0].replace('\n', '').replace('체인쏘맨', '체인소맨').rstrip(), i['href']])

    return linkss

async def files(session, name, url):
    logger.debug(f"{name} files started {url}")
    a = 1
    async with session.get(url) as response:
        if response.status == 200:
            f = await aiofiles.open(f'./manga/{name}/{str(a)}.jpg', mode='wb')
            await f.write(await response.read())
            await f.close()
            logger.debug(f"{name} file finished")
            a += 1
        else:
            await asyncio.sleep(2)
            f = await aiofiles.open(f'./manga/{name}/{str(a)}.jpg', mode='wb')
            await f.write(await response.read())
            await f.close()
            logger.debug(f"{name} file finished")
            a += 1


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
    
    return [[name, i] for i in img_list]
    
    # body = soup.find('div', attrs={'class':'entry-content'})
    # return [normalize('NFKD',para.get_text())
    #         for para in body.find_all('p')]

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
        *(files(session, url[0], url[1], url) for url in paras)
    )

async def main():
    logger.debug("main start")
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(fetch_and_parse(session, url) for url in linksss)
        )

if __name__ == "__main__":
    with open("info.log", 'w') as f: f.close()
    with open('logging.json', 'rt') as f: config = json.load(f)
    logging.config.dictConfig(config)
    logger = logging.getLogger()
    # linksss = episode_lists('https://manamoa26.com/bbs/board.php?bo_table=cartoon&wr_id=12888')
    # with open('lss.txt', 'w') as f: f.write(str(linksss))
    # for i in linksss:
    #      os.mkdir(f'./manga/{i[0]}')
    asyncio.run(main())