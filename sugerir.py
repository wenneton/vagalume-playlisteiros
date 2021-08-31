import requests
import sys
from time import time, sleep

def get_token(session_id, user, playlist):
    url = f"https://app2.vagalume.com.br/ajax/playlisteiros.php?action=buildToken&sessionID={session_id}&sessionUser={user}&playlistID={playlist}"
    with requests.Session() as s:
        r = s.get(url, headers={'Connection': 'close'})
        token = r.text.split('"')[1]

    return token

def suggest_music(pointer_id, session_id, token, user, playlist, proxy=None):
    data = {
        'action': 'addMusicToPlaylist', 'playlistID': playlist, 'pointerHID': pointer_id, 'token': token, 'sessionID': session_id,
        'sessionUser': user
    }

    proxies = {
        'https': proxy
    }

    with requests.Session() as s:
        if proxy:
            r = s.post("https://app2.vagalume.com.br/ajax/playlisteiros.php", data=data, headers={'Connection': 'close'}, proxies=proxies)
            response = r.text
        else:
            r = s.post("https://app2.vagalume.com.br/ajax/playlisteiros.php", data=data, headers={'Connection': 'close'})
            response = r.text
    
    print(response)

    return response

if __name__ == '__main__':
    user = '3ade68b7gaf47cea3'
    playlist = '3931'
    if len(sys.argv) > 2:
        session_id = sys.argv[1]
        seconds_to_sleep = int(sys.argv[2])*60
    else:
        print("Você precisa passar o id da sessão e quantidade de segundos entre as sugestoes!")

    with open('pointer_ids.txt', 'r') as f:
        lines = f.readlines()

    # schedule.every(4).seconds.do(print('uhul'))

    while len(lines) != 0:
        pointer_id = lines.pop(0)[:-1]

        with open('pointer_ids.txt', 'w') as f:
            f.writelines(lines)

        print(pointer_id)

        token = get_token(session_id, user, playlist)

        print(token)
        suggest_music(pointer_id, session_id, token, user, playlist)

        with open('pointer_ids.txt', 'r') as f:
            lines = f.readlines()

        sleep(seconds_to_sleep)
        # sleep(2)
        # schedule.run_pending()
        # print('oi')

    print("Acabaram as sugestões na lista :(")
