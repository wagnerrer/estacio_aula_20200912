from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import datetime
import os
import re
import logging
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/', methods=['GET'])
def index():
    return f"<h1>Welcome to our Data Service! <br> {str(datetime.datetime.today())} </h1>"

@app.route('/volatility', methods=['GET'])
def volatility():
    headers = {
        'authority': 'www.myfxbook.com',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.myfxbook.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.myfxbook.com/forex-market/volatility',
        'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'cookie': 'locale=en; timezone=-3.0; dst=0; toolbarWindow=4; cookieconsent_status=dismiss; __gads=ID=573cbb7e9c623ea5:T=1599247563:S=ALNI_MaKixskg2G-VZ00VlCrq5-7FsOftA; correlationSymbols="1,6,5,4,3,10,8,7#2119,5079,2115,1815,1806,10064,2114,2348,356365,397724,2090,3473,1246,1245,2076,1247,356945,356944,1236,356943,1863,356942,3488,356941,1233,1234,367974,367967,367960,1209,2,1893,1,6,5,4,3,10,9,8669,8,7,12755,2872,2603,51,50,49,48,47,46,45,43,1694,2521,2516,2511,3887,24,23,26,25,20,19,22,21,15,18,17,5779,12,11,14,13,40,41,42,36,37,3304,38,31,33,34,27,28,29,14247,107,3005,3001,131,137,2729,19780,129,2012,5435,79789,3240,103,2482"; spreads="1,2,3,4,5,6,7,17,28,29#27,85,187,229,272,332,408,492,589,616,620,716,727,755,776,790,808,828,918,921,925,929,930,955,1017,1038,1055,1065,1124,1131,1156,1184,1208,1212,1216,1241,1256,1420,1437,1453,1486,1496,1505,1575,1606,1673,1678,1736,1751,1768,1881,1890,1942,1946,2015,2057,2059,2061,2228,2279,2320,2398,2426,2449,2461,2468,2512,2515,2559,2613,2627,2641,2659,2719,2768,2773,2824,2879,2880,2925,2929,2945,3036,3067,3131,3234,3263,3278,3302,3349,3359,3360,3381,3420,3451,3478,3505,3512,3533,3576,3622,3819,3895,3957,3970,3971,3984,4214,4262,4329,4342,4346,4417,4552,4575,4582,4686,4715,4777,4778,4779,4830,4833,4875,4887,4891,4904,4928,4931,5051,5116,5187,5245,5265,5712,5786,5799,5909,6049,6052,6217,6222,6233,6250,6265,6340,6410,6627,6746,7180,7467,8314,8538,9217,9280,10024,10102,10365,10687,10708"; indicatorFilters="1,2,3,5//2"; JSESSIONID=22EA8410CCB6A1779F2DDDEEDFE4154B; __utma=52609076.1186003120.1599229065.1599504451.1599914233.9; __utmc=52609076; __utmz=52609076.1599914233.9.3.utmcsr=colab.research.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/; patternsFilters="18,23,1,107,2,5,3/27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,44,45,46,47,48,50,51,52,53,54,56,57,58,59,61,60,49,62,63,64,65,66,67,68,69,70,41,71,72,73,74,75,26,21,22,24,25,23,76,77,20,78,79,80/2"; lastVisitDate=1; __utmt=1; __utmb=52609076.13.9.1599914235996; marketSymbols="0,2119,5079,2115,1815,1806,10064,2348,356365,397724,2090,3473,1246,1245,2076,1247,356945,356944,1236,356943,1863,356942,3488,356941,1233,1234,367974,367967,367960,1209,2,1893,1,6,5,4,3,10,9,8669,8,7,12755,2872,2603,51,50,49,48,47,46,45,43,1694,2521,2516,2511,3887,24,23,26,25,20,19,22,21,15,18,17,5779,12,11,14,13,40,41,42,36,37,3304,38,31,33,34,27,28,29,14247,107,3005,3001,131,137,2729,19780,129,2012,5435,79789,3240,103,2482"',
    }

    data = {
        'symbols': '2119,5079,2115,1815,1806,10064,2348,356365,397724,2090,3473,1246,1245,1247,356945,356944,1236,356943,1863,356942,3488,356941,1233,1234,367974,367967,367960,1209,2,1893,1,6,5,4,3,10,9,8669,8,7,12755,2872,2603,51,50,49,48,47,46,45,43,1694,2521,2516,2511,3887,24,23,26,25,20,19,22,21,15,18,17,5779,12,11,14,13,40,41,42,36,37,3304,38,31,33,34,27,28,29,14247,107,3005,3001,131,137,2729,19780,129,2012,5435,79789,3240,103,2482',
        'pageId': 'forexMarketVolatility',
        'z': '0.8379831365929087'
    }

    response = requests.post('https://www.myfxbook.com/updateMarketSymbolMenu.json', headers=headers, data=data)
    table_content = response.json()

    # obter a lista de pares de moedas
    # find -> retorna sempre o primeiro!

    soup = BeautifulSoup(table_content['content']['marketVolatilityTable'], "html.parser")

    # Obtendo os indicadores
    linhas = soup.find("table").find_all("tr")

    # limpeza simples
    del linhas[0]

    # dicionario de resultado
    resultados = {}

    for linha in linhas:
        colunas = linha.find_all("td")
        for idx, coluna in enumerate(colunas):
            if idx == 0:
            # .strip -> remove os espaços em branco
                moeda = coluna.string.strip()

            # garantia de inicialização
            if moeda not in resultados:
                resultados[moeda] = {}

            else:
                # alternativa ao find
                # no .select() / .select_one() você poderá usar seletores CSS 
                span = coluna.select_one("span")
                # AUDCADTimeScale15
                # split("TimeScale") -> string para array
                # [AUDCAD, 15]
                # [-1] => 15
                timeframe = span['name'].split("TimeScale")[-1] 
                resultados[moeda][timeframe] = {
                    "value": span['value'],
                    "high": span['high'],
                    "low": span['low'],
                    "decimals": span['decimals']
                }

    return jsonify(resultados)

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except:
        app.run()
    