
def parse_message(message):
    parsed = dict()
    parsed['chat_id'] = message['message']['chat']['id']
    parsed['txt'] = message['message']['text']
    parsed['user_id'] = message['message']['from']['id']
    parsed['first_name'] = message['message']['from']['first_name']
    parsed['last_name'] = message['message']['from']['last_name']
    parsed['username'] = message['message']['from']['username']
    parsed['message_id'] = message['message']['message_id']
    parsed['update_id'] = message['update_id']
    parsed['mes_date'] = message['message']['date']
    return parsed

def send_message(chat_id, token, text='bla-bla-bla'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload)
    return r
