import time

import requests
import json

token = ''

tasks = ['SeveralHourlsRewardedAdTask', 'SeveralHourlsRewardedAdTask4', 'emojiOnPostTelegramNewsChannel3']
okUrls = ['ad-watched','ad-watched','ad-request']
ok = [{
        "providerId": "adsgram",
        "adsForSpins": False
    },{
        "providerId": "onclickaV2",
        "adsForSpins": False
    },{
        "providerId": "joinedChat"
    }]


def oneStart():
    urls = [f"https://boink.astronomica.io/api/rewardedActions/rewardedActionClicked/{task}?p=tdesktop" for task in tasks]

    payload = json.dumps({})
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://boink.astronomica.io',
        'priority': 'u=1, i',
        'referer': 'https://boink.astronomica.io/earn',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    for url in urls:
        while True:  # Цикл для повторных попыток
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                print(f"Response for {url}: {response.text}")  # Вывод ответа для каждого URL
                break  # Если запрос выполнен успешно, выходим из цикла
            except Exception as e:
                print(f"Ошибка при выполнении запроса к {url}: {e}. Перезапуск...")
                continue  # Продолжаем цикл для повторного выполнения


def oneOk():
    urls = [f"https://boink.astronomica.io/api/rewardedActions/{okUrl}?p=tdesktop" for okUrl in okUrls]

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://boink.astronomica.io',
        'priority': 'u=1, i',
        'referer': 'https://boink.astronomica.io/earn',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    # Проверяем, что количество URL совпадает с количеством элементов в ok
    if len(urls) == len(ok):
        for url, item in zip(urls, ok):  # Перебираем пары URL и элементов списка ok
            payload = json.dumps(item)  # Сериализация каждого элемента в JSON-формат
            while True:  # Цикл для повторных попыток
                try:
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print(
                        f"Response for {url} with payload {item}: {response.text}")  # Вывод ответа для каждого URL с payload
                    break  # Если запрос выполнен успешно, выходим из цикла
                except Exception as e:
                    print(f"Ошибка при выполнении запроса к {url} с payload {item}: {e}. Перезапуск...")
                    continue  # Продолжаем цикл для повторного выполнения
    else:
        print("Количество URL не совпадает с количеством элементов в списке ok.")

def oneClaim():
    urls = [f"https://boink.astronomica.io/api/rewardedActions/claimRewardedAction/{task}?p=tdesktop" for task in tasks]

    payload = json.dumps({})
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://boink.astronomica.io',
        'priority': 'u=1, i',
        'referer': 'https://boink.astronomica.io/earn',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    for url in urls:
        while True:  # Цикл для повторных попыток
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                print(f"Response for {url}: {response.text}")  # Вывод ответа для каждого URL
                break  # Если запрос выполнен успешно, выходим из цикла
            except Exception as e:
                print(f"Ошибка при выполнении запроса к {url}: {e}. Перезапуск...")
                continue  # Продолжаем цикл для повторного выполнения


while True:
    print('Стартуем......')
    oneStart()

    print('Ждем время для подтвеждения')
    time.sleep(25)
    oneOk()

    print('собираем за рекламу')
    time.sleep(2)
    oneClaim()

    print('Просто подождем')
    time.sleep(5)