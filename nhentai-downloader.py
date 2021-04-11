import os, shutil, itertools, time, concurrent.futures, ctypes
import requests
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup

os.system('title nHentai Downloader Ver 0.1 By NekoChan')

session = FuturesSession()
session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 3))
kernel32 = ctypes.windll.kernel32

for i in itertools.count(1) :
    print(i)

    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))

    bookId = input(f'請輸入ＩＤ：')
    nBook = requests.get(f'https://nhentai.net/g/{bookId}/')

    if nBook.status_code == 200 :
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))

        begin = time.time()
        html = BeautifulSoup(nBook.text, 'html.parser')
        coverImgHtml = html.select('#cover > a > img')[0].get('data-src')

        imgType = coverImgHtml.split('.')[-1]
        galleriesId = coverImgHtml.split('/')[-2]
        pages = int(html.select('#tags > div:nth-child(8) > span > a > span')[0].string)

        savePath = f'{os.getcwd()}\\{bookId}'

        if os.path.isdir(savePath) :
            shutil.rmtree(savePath)

        os.mkdir(savePath)

        print(f'ＩＤ：{bookId}, 圖片類型：{imgType}, 資料庫ＩＤ：{galleriesId}, 頁數：{pages}, 狀態：開始下載')

        with FuturesSession(max_workers = 50) as seesion :
                futures = []

                for index in range(pages) :
                    future = session.get(f'https://i.nhentai.net/galleries/{galleriesId}/{index + 1}.{imgType}', timeout = (5, None))
                    future.index = index
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures) :
                    response = future.result()
                    savImg = open(f'{savePath}\\{future.index + 1}.{imgType}', 'ab')
                    savImg.write(response.content)
                    savImg.close()

        print(f'ＩＤ：{bookId}, 圖片類型：{imgType}, 資料庫ＩＤ：{galleriesId}, 頁數：{pages}, 狀態：下載完畢, 花費時間：{round(time.time() - begin)} 秒')

    else :
        print('請輸入正確的ＩＤ。')