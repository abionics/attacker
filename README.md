## Гайд по DDoS сайтів окупантів
Отличие сборки - перечень целей в файле list.txt

### Запуск через докер (потрібен попередньо встановлений докер і docker-compose)
Інструкція як встановити докер [тут](/docs/docker_installation.md)
1) `git clone https://github.com/abionics/attacker`
2) `cd attacker`
3) `./start.sh`
4) "Щоб призупинити зашквар і трохи провітрити хату" `./stop.sh`

Корегуйте параметри `REQUESTS_PER_SITE` та `PARALLEL_COUNT` для зміни швидкості.
За замовчуванням використовуються проксі (див. [з api](http://46.4.63.238/api.php)).
Також є можливість використовувати власні проксі та власны проксы файли (див. `CUSTOM_PROXY` та `CUSTOM_PROXIES_FILE`) 

### Без докеру
1) Встановити python, для linux це `sudo apt install git python`
2) `git clone https://github.com/abionics/attacker`
3) `cd attacker`
4) `pip3 install -r requirements.txt`
5) `python3 main.py`
* при проблемах з pip3 на linux юзайте `apt install python3-pip`

### З використанням Google Colab
Запускайте **[цей блокнот](https://colab.research.google.com/drive/1eOynwkRAmYcCRIOl7IDVitmrL9NbEQss)**,
дякую [vrkssi](https://www.instagram.com/vrkssi/) за його створення!

### Координація
Координуємо наші атаки у группах, наприклад https://t.me/ddos_kotyky та https://t.me/itarmyofukraine2022

Про усі проблеми пишіть у issues, буду намагатися допомогти
