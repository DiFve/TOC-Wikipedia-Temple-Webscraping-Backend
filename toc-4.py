import requests
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    result = {
        "บึงกาฬ": [],
        "เลย": [],
        "ศรีสะเกษ": [],
        "สกลนคร": [],
        "สงขลา": []
    }
    result["บึงกาฬ"] = getListTempleName(
        "https://th.wikipedia.org/wiki/รายชื่อวัดในจังหวัดบึงกาฬ")
    result["เลย"] = getListTempleName(
        "https://th.wikipedia.org/wiki/รายชื่อวัดในจังหวัดเลย")
    result["ศรีสะเกษ"] = getListTempleName(
        "https://th.wikipedia.org/wiki/รายชื่อวัดในจังหวัดศรีสะเกษ")
    result["สกลนคร"] = getListTempleName(
        "https://th.wikipedia.org/wiki/รายชื่อวัดในจังหวัดสกลนคร")
    result["สงขลา"] = getListTempleName(
        "https://th.wikipedia.org/wiki/รายชื่อวัดในจังหวัดสงขลา")

    return {
        "result":  result
    }


def getListTempleName(URL):
    url = URL
    response = requests.get(url)
    html_content = response.text
    result = re.findall(">(.*?)<", html_content)
    result = [s for s in result if re.match(r"^(วัด|ที่พักสงฆ์).*$", s)]
    result = [s for s in result if re.match(
        r"^(?!.*(มหานิกาย|ธรรมยุติกนิกาย|จีนนิกาย|อนัมนิกาย)$).*$", s)]
    result = [s for s in result if re.match(
        r"^(?:(?!ในอำเภอ|ในจังหวัด|ในตำบล|ในกิ่งอำเภอ).)*$", s)]
    result = [re.sub(r' (ตำบล|ที่ตั้ง).*$', '', s) for s in result]
    result = [re.sub(r'\(.*\)', '', s) for s in result]
    result = list(set(result[:-2]))
    # print(len(result))
    return result


# print(getListTempleName("https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%83%E0%B8%99%E0%B8%88%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%A8%E0%B8%A3%E0%B8%B5%E0%B8%AA%E0%B8%B0%E0%B9%80%E0%B8%81%E0%B8%A9"))


# url = sys.argv[1]

# print(getListTempleName(url))
