import json, re, base64, asyncio, os 
import logging, logging.config
import requests, aiohttp, aiofiles
from bs4 import BeautifulSoup

class Req():
    
    def __init__(self) -> None:
        self.title = ""

    async def files(self, session, name, url ,li):
        #files(session, name = '197', url = "https://img.imimggggg87878.com/", li = ["https://img.com/", "https://img.com/"])
        try:
            #Get image location number ex) 1
            loc = int(li.index(url))+1
            #Keep process if image wasn't made
            # ./주술회전/197 - 1.jpg
            if not os.path.isfile(f'./{self.title}/{name}-{str(loc)}.jpg'):
                logger.debug(f"{name} files started {url}")
                #fetch image
                async with session.get(url) as response:
                        if response.status == 200:
                            #save the image
                            f = await aiofiles.open(f'./{self.title}/{name}-{str(loc)}.jpg', mode='wb')
                            await f.write(await response.read())
                            await f.close()
                            logger.debug(f"{name}-{str(loc)}.jpg file finished")
                        else: #Bad Request
                            await asyncio.sleep(2)
                            async with aiohttp.ClientSession() as session:
                                self.files(session, name, url, li)
                            
            else: logger.debug(f"{name} files are already exist {url}")
        except: #Timeout
            await asyncio.sleep(2)
            async with aiohttp.ClientSession() as session:
                self.files(session, name, url, li)


    def parse(self, html, url):
        # parse(html,['주술회전 197화', 'https://manamoa26.com/bbs/'])
        name = url[0] #주술회전 197화
        name = name.split()[1].replace('화', '') #197
        logger.debug(f"{url[0]}-{name} parse started")
        
        # find img_list in js on html & decode
        json_string = re.search(r'var manamoa_img = (.*?);', html, re.S).group(1)
        res = base64.b64decode(json_string) 
        # Parse
        soup = BeautifulSoup(res, "lxml")
        #collect img 
        passmydivs = soup.find_all("img", src=True)
        img_list =[i["src"] for i in passmydivs]
        
        #['197', ["https://img.imimggggg87878.com/", "https://img.imimggggg87878.com/"]]
        return [name, [i for i in img_list]]


    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def fetch_and_parse(self, session, url):
        # feach(session, ['주술회전 197화', 'https://manamoa26.com/bbs/'])
        link = url[1] #'https://manamoa26.com/bbs/'
        logger.debug(f"{url[0]} started")
        #feach html
        html = await self.fetch(session, link)
        logger.debug(f"{url[0]} fetched")
        # run parse(html) in a separate thread, and resume this coroutine when it completes
        loop = asyncio.get_event_loop()
        # parse(html,['주술회전 197화', 'https://manamoa26.com/bbs/'])
        paras = await loop.run_in_executor(None, self.parse, html, url)
        #['197', ["https://img.imimggggg87878.com/", "https://img.imimggggg87878.com/"]]
        logger.debug(f"{url[0]} parse finished")
        #fetch img files & Save
        #files(session, '197', "https://img.imimggggg87878.com/", ["https://img.com/", "https://img.com/"])
        return await asyncio.gather(
            *(self.files(session, paras[0], url, paras[1]) for url in paras[1])
        )


    async def main(self):
        print(self.title)
        print("Title: ", self.title)
        # Make directory if it dosen't exist
        # if not self.title in os.listdir('./'):
        #     await os.mkdir(f'./{self.title}')
    
        logger.info("main start")
        #Make session & feach_and_parse
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(
                # feach(session, ['주술회전 197화', 'https://manamoa26.com/bbs/'])
                *(self.fetch_and_parse(session, url) for url in linksss)
            )

    def episode_lists(self, ur):
            html = requests.get(ur).text
            #parse
            soup = BeautifulSoup(html, "lxml")
            #title
            self.title = soup.find("meta", property="og:title")['content'].strip()
            #Epsiode Name & Link
            passmydivs = soup.find_all("a", {"class": "item-subject"}, href=True)
            linkss = [[i.contents[0].replace('\n', '').rstrip(), i['href']] for i in passmydivs]
            
            # return [['주술회전 197화', 'https://manamoa26.com/bbs/'], ['주술회전 196화', 'https://manamoa26.com/bbs/']]
            return linkss

if __name__ == "__main__":
    #Logger Setup
    with open('logging.json', 'rt') as f: config = json.load(f)
    logging.config.dictConfig(config)
    logger = logging.getLogger()
    
    #Make Class
    make = Req()
    #Page link
    link = input("Link: ")
    # return [['주술회전 197화', 'https://manamoa26.com/bbs/'], ['주술회전 196화', 'https://manamoa26.com/bbs/']]
    linksss = make.episode_lists(link.strip())
    #Run Main
    asyncio.run(make.main())
    logger.info("finished \n")