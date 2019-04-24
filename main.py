import requests, os, argparse, dotenv
from dotenv import load_dotenv


def create_bitlink(url_to_check, token):
  headers = {"Authorization" : "Bearer {}".format(token)}

  url = 'https://api-ssl.bitly.com/v4/bitlinks'

  body = {
      "long_url": url_to_check
    }

  response = requests.post(url, headers=headers, json=body)

  if response.ok:
    return response.json()['id']


def get_bitlink(url_to_check, token):
  headers = {"Authorization" : "Bearer {}".format(token)}

  url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url_to_check)

  response = requests.get(url, headers = headers)

  if response.ok:
    return url_to_check

  url_to_check_replace = url_to_check.replace('http://','').replace('https://','')

  url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url_to_check_replace)

  response = requests.get(url, headers = headers)
  if response.ok:
    return url_to_check_replace


def get_clicks_number(bitlink, token):
  headers = {"Authorization" : "Bearer {}".format(token)}

  url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks'.format(bitlink)

  payload = {"unit":"day", "units":"-1"}

  response = requests.get(url, params=payload, headers = headers)

  if response.ok:
    return response.json()['link_clicks']


def get_clicks_count(url, token):
  clicks_count = dict()

  bitlink = get_bitlink(url, token)

  if bitlink is None:
    return None

  for clicks_info in get_clicks_number(bitlink, TOKEN_API_BITLY):
    clicks_count[clicks_info['date']] = clicks_info['clicks']

  return clicks_count


def main():
  load_dotenv()

  TOKEN_API_BITLY = os.getenv("TOKEN_API_BITLY")

  parser = argparse.ArgumentParser(
       description='''Создание коротких ссылок или
       подсчет количества кликов, если ссылка уже создана'''
   )
  parser.add_argument('url', help='Укажите ссылку')
  args = parser.parse_args()
  url = args.url

  clicks_count = get_clicks_count(url, TOKEN_API_BITLY)

  if clicks_count is None:
    print('bitlink:', create_bitlink(url, TOKEN_API_BITLY))
  elif not clicks_count:
    print('Список кликов пуст')
  else:
    for date, count in clicks_count.items():
      print(f'{date} количество {count}')


if __name__ == "__main__":
  main()