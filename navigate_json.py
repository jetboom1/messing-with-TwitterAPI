import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
def twitter_api(username):
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    base_url = "https://api.twitter.com/"
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_params = {
        'usernames': username,
        'user.fields': 'id,name,username,protected,verified,withheld,profile_image_url,location,url,description,'
                       'entities,pinned_tweet_id,public_metrics'
    }
    search_url = '{}2/users/by'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    return search_resp

def display_dict(file):
    """
    :param file: dict
    :return:
    """
    print("Ключи об'єкта, оберіть, який хочете переглянути:")
    for i in file.keys():
        print('> {}| Тип значення: {}'.format(i, type(file[i])))
    print('Надрукуйте exit, щоб вийти')
    print("Надрукуйте up, щоб піднятися на об'єкт вище")

def display_list(file):
    """
    :param file: list
    :return:
    """
    print("Елементи списку, оберіть, який хочете переглянути:")
    for i in range(len(file)):
        print('> {} | Тип значення: {}'.format(i, type(file[i])))
    print('Надрукуйте exit, щоб вийти')
    print("Надрукуйте up, щоб піднятися на рівень вище")

if __name__ == '__main__':
    inp = input('Введіть username людини, чий профіль ви хочете переглянути. E.g elonmusk')
    obj = twitter_api(inp).json()
    stack = [obj,]
    while inp != 'exit':
        if inp == 'up':
            try:
                obj = stack[-2]
                stack = stack[:-1]
            except IndexError:
                print('Вище тільки зорі!')
        if type(obj) == dict:
            display_dict(obj)
            inp = input("Введіть ключ, який ви хочете переглянути")
            while True:
                try:
                    obj = obj[inp]
                    break
                except (KeyError, ValueError) as e:
                    if inp == 'up':
                        try:
                            obj = stack[-2]
                            stack = stack[:-1]
                        except IndexError:
                            print('Вище тільки зорі!')
                        break
                    if inp == 'exit':
                        break
                    print('Помилка! Такого ключа не існує!')
                    display_dict(stack[-1])
                    inp = input("Введіть ключ, який ви хочете переглянути")
            stack.append(obj)
        elif type(obj) == list:
            display_list(obj)
            inp = input("Введіть індекс елементу, який ви хочете переглянути")
            while True:
                try:
                    obj = obj[int(inp)]
                    break
                except (IndexError, ValueError) as e:
                    if inp == 'up':
                        try:
                            obj = stack[-2]
                            stack = stack[:-1]
                        except IndexError:
                            print('Вище тільки зорі!')
                        break
                    if inp == 'exit':
                        break
                    print('Помилка! Такого індексу не існує!')
                    display_list(obj)
                    inp = int(input("Введіть індекс елементу, який ви хочете переглянути"))
            stack.append(obj)
        else:
            print(obj)
            inp = input("Надрукуйте exit, щоб вийти, надрукуйте up, щоб піднятися на рівень вище")