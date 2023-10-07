import requests

import apimoex

# proxy = {"https": "http://yhv02e:SP9zBP@46.161.47.116:9358"}


with requests.Session() as session:
    # session.proxies.update(proxy)
    data = apimoex.get_market_candles(session=session, security="SNGSP", start="2022-10-07", interval=1)
    print(data)

