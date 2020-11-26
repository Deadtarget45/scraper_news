import requests
import lxml.html as html 
import datetime
import os
import io

HOME_URL = 'http://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_SUMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div/div[@class="html-content"]/p/text()'

def parse_notices(link, today):
    try:
        response = requests.get(link) 
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                sumary = parsed.xpath(XPATH_SUMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return 

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')



        else:
            raise ValueError(f'error: {response}')
    except ValueError as ve:
        pass



def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
           # print(links_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
               os.mkdir(today)

            for link in links_notices:
                parse_notices(link, today)

        else:
            raise ValueError(f'error {response.status_code}')

    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()