import os
import sys
import urllib.request
import json
from unidecode import unidecode

#input_d = input("영단어를 입력하세요:")


def translate_function(self):
    client_id = "WJRDMeZ92D0HeyqwvfMV"
    client_secret = "P3okeaBHY8"
    encText = urllib.parse.quote(self)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        response_d = response_body.decode('utf-8')

        j = json.loads(response_d)
        #print (j)
        t = j["message"]["result"]
        translate_t = t["translatedText"]
        romanize_r = unidecode(translate_t)


        #print(response_body.decode('utf-8') )
        #print ("Input: %s" %input_d)
        #print ("Output: %s" %translate_t)
        #print ("Romanize: %s" %romanize_r)
    else:
        return "Error Code:" + rescode


    return ["%s" %translate_t, "%s" %romanize_r]

if __name__ == '__main__':
    translate_function()
