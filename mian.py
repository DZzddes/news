import requests
import json
import time
from datetime import datetime
import traceback
# import bs4


session = requests.Session()

headers = {
    "Host": "i.news.qq.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://news.qq.com",
    "Referer": "https://news.qq.com/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

news_headers = {
    "Host": "news.qq.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

session.headers.update(headers)
news_result_list = []

for page in range(0,11):
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>正在抓取第{page}页>>>>>>>>>>>>>>>>>>>>>>>>>>> length: {len(news_result_list)}")
    try:
        body = f"page={page}&query=%E4%BB%A3%E5%AD%95&is_pc=1&hippy_custom_version=24&search_type=all&search_count_limit=10&appver=15.5_qqnews_7.1.80&"

        response = session.post("https://i.news.qq.com/gw/pc_search/result", data=body)

        data = json.loads(response.text)
        for news in data["secList"][-10:]:
            _id = news.get("newsList","")[0].get("id","")
            if _id :
                news_result = dict()
                news_url = f'https://news.qq.com/rain/a/{_id}'
                news_resp = requests.get(news_url,headers=news_headers)
                # news_soup = bs4.BeautifulSoup(news_resp.text, "html.parser")

                news_result['title'] = news['newsList'][0].get('title')
                news_result['url'] = news_url
                news_result['html'] = news_resp.text
                news_result_list.append(news_result)
                time.sleep(2)
        time.sleep(3)
        if len(news_result_list) >= 20:
            break
    except:
        traceback.print_exc()
if len(news_result_list) >0:

    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>正在抓取第抓取完毕，正在保存文件>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    now = datetime.now()
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    file_name = f"{day}_{hour}_{minute}_{second}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(news_result_list, f, indent=4, ensure_ascii=False)

    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>保存完毕，文件名为{file_name}>>>>>>>>>>>>>>>>>>>>>>>>>>> length: {len(news_result_list)}")
else:
    print("抓取失败")
