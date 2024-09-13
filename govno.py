import threading
import time
import json
import requests  # убедитесь, что у вас установлен requests
from datetime import datetime, timedelta, timezone

token = ''

header = {
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
timers = [302, 62, 28800]

def oneStart(task):
    url = f"https://boink.astronomica.io/api/rewardedActions/rewardedActionClicked/{task}?p=tdesktop"
    payload = json.dumps({})
    headers = header

    while True:  # Цикл для повторных попыток
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            claimDateTime = response.json()['claimDateTime']
            # print(claimDateTime)  # Выводим дату и время
            # print(f"Response for {url}: {response.text}")  # Вывод ответа для каждого URL
            return claimDateTime  # Возвращаем claimDateTime для дальнейших расчетов
        except Exception as e:
            print(f"Ошибка при выполнении запроса к {url}: {e}. Перезапуск...")
            continue  # Продолжаем цикл для повторного выполнения

def oneOk(okUrl, okPayload):
    url = f"https://boink.astronomica.io/api/rewardedActions/{okUrl}?p=tdesktop"
    payload = json.dumps(okPayload)  # Сериализация каждого элемента в JSON-формат
    headers = header

    while True:  # Цикл для повторных попыток
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(f"Response for {url} with payload {okPayload}: {response.text}")  # Вывод ответа для каждого URL с payload
            break  # Если запрос выполнен успешно, выходим из цикла
        except Exception as e:
            print(f"Ошибка при выполнении запроса к {url} с payload {okPayload}: {e}. Перезапуск...")
            continue  # Продолжаем цикл для повторного выполнения

def oneClaim(task):
    url = f"https://boink.astronomica.io/api/rewardedActions/claimRewardedAction/{task}?p=tdesktop"
    payload = json.dumps({})
    headers = header

    while True:  # Цикл для повторных попыток
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(f"Response for {url}: {response.text}")  # Вывод ответа для каждого URL

            if response.status_code == 403:
                return response.status_code
            else:
                claimDateTime = response.json()['newUserRewardedAction']['claimDateTime']
                # print(claimDateTime)
                return claimDateTime  # Возвращаем claimDateTime для дальнейших расчетов
        except Exception as e:
            print(f"Ошибка при выполнении запроса к {url}: {e}. Перезапуск...")
            continue  # Продолжаем цикл для повторного выполнения

def calculate_sleep_time(claim_time_str, claimDateTimeStart, timer):
    c_time = claim_time_str
    if claim_time_str == 403:
        c_time = claimDateTimeStart
    # Преобразуем строки в объекты datetime
    claim_time = datetime.strptime(c_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_time = datetime.now(timezone.utc).replace(tzinfo=None)

    # Вычисляем время завершения с учетом таймера
    end_time = claim_time + timedelta(seconds=timer)

    # Определяем время ожидания или сразу возвращаем 0
    if end_time > current_time:
        remaining_time = (end_time - current_time).total_seconds()
        return remaining_time
    else:
        return 0  # Если уже время прошло, возвращаем 0

def task_runner(task, okUrl, okPayload, timer):
    while True:
        print(f'Стартуем для задачи {task}...')
        claimDateTimeStart = oneStart(task)  # Получаем claimDateTime

        print('Ждем время для подтверждения')
        time.sleep(25)
        oneOk(okUrl, okPayload)

        print('Собираем за рекламу')
        # time.sleep(10)
        claimDateTime = oneClaim(task)

        # Вычисляем оставшееся время перед следующим запуском
        remaining_time = calculate_sleep_time(claimDateTime, claimDateTimeStart, timer)
        if remaining_time > 0:
            print(f'Просто подождем {remaining_time} секунд перед следующим циклом для задачи {task}')
            time.sleep(remaining_time)
        else:
            print(f'Время ожидания истекло или не требуется ожидания, начинаем цикл заново для задачи {task}')
            continue  # Начинаем цикл заново

# Создаем потоки для каждой задачи с разными таймерами и различными параметрами
threads = []
for task, okUrl, okPayload, timer in zip(tasks, okUrls, ok, timers):
    thread = threading.Thread(target=task_runner, args=(task, okUrl, okPayload, timer))
    threads.append(thread)
    thread.start()

# Ждем завершения всех потоков
for thread in threads:
    thread.join()