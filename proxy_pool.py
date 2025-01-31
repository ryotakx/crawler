import requests


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_proxy_num():
    return requests.get("http://127.0.0.1:5010/get_status/").json().get('useful_proxy')
