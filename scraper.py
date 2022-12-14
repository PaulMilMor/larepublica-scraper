import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/descendant-or-self::text()'


def parse_news(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            new = response.content.decode('utf-8')
            parsed = html.fromstring(new)

            try: 
                title = parsed.xpath(XPATH_TITLE)[0]
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                title = title.replace('\"','')
                title = title.replace('\n                        ','')
                title = title.replace('\n                    ', '')
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                for p in body:
                    f.write(p)

                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_news)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_news:
                parse_news(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

    
if __name__ == '__main__':
    run()