import requests

import apimoex

# proxy = {"https": "https://91.144.163.169:8090"}


with requests.Session() as session:
    # session.proxies.update(proxy)
    data = apimoex.get_board_history(session, "SNGSP")
    print(data)

