import requests
import yaml

with open('config.yaml', 'r') as yamlFile:
    config_data = yaml.load(yamlFile, Loader=yaml.FullLoader)

auth_token = config_data["token"]
myInstanceHost = config_data["myInstanceHost"]
targetHost = config_data['targetHost']
user_list_req = {"i": f'{auth_token}', "host": targetHost, "limit": 100}
api_req_header = {'Content-type': 'application/json', 'Accept': 'application/json'}

user_list = []
user_id_list = []
page = 0
while True:
    print(f'get user list... {page}')
    if len(user_id_list) != 0:
        user_list_req['untilId'] = user_id_list[-1]
    res = requests.post(f'https://{myInstanceHost}/api/federation/users',
                        json=user_list_req, headers=api_req_header)
    if not res.ok:
        print(f'Fail to get user list! Code:{res.status_code}, Response: {res.text}')
        break
    if len(res.json()) == 0:
        break
    page += 1
    user_list.extend(res.json())
    user_id_list.extend(list(map(lambda x: x["id"], res.json())))

emoji_id_list = []
emoji_list = []
emoji_list_req = {"i": f'{auth_token}', "host": targetHost, "limit": 100}
page = 0
while True:
    print(f'get emoji list... {page}')
    if len(emoji_id_list) != 0:
        emoji_list_req['untilId'] = emoji_id_list[-1]
    res = requests.post(f'https://{myInstanceHost}/api/admin/emoji/list-remote',
                        json=emoji_list_req, headers=api_req_header)
    if not res.ok:
        print(f'Fail to get emoji list! Code:{res.status_code}, Response: {res.text}')
        break
    if len(res.json()) == 0:
        break
    page += 1
    emoji_list.extend(res.json())
    emoji_id_list.extend(list(map(lambda x: x["id"], res.json())))

emoji_list_with_host = list(map(lambda x: {"name": x["name"], "host": x["host"]}, emoji_list))
uid_list_with_url = list(map(lambda x: {"id": x["id"], "url": x["url"]}, user_list))
for emoji_with_host in emoji_list_with_host:
    print(f'emoji: :{emoji_with_host["name"]}@{emoji_with_host["host"]}:')
for uid_with_url in uid_list_with_url:
    print(f'user: {uid_with_url["id"]} ( {uid_with_url["url"]} )')

print(f'Will DELETE {len(user_id_list)} user(s) and {len(emoji_id_list)} emoji(s)...')
user_input = input('Are you sure? Enter "yes" in UPPERCASE \n(YES/no)\n')
if user_input != 'YES':
    print("exit!")
    exit(0)

for uid in user_id_list:
    delete_req = {'i': auth_token,
                  'userId': uid}
    res = requests.post(f'https://{myInstanceHost}/api/admin/delete-account',
                        json=delete_req, headers=api_req_header)
    if not res.ok:
        print(f'Error to delete {uid}')
    else:
        print(f'User {uid} deleted')

i = 0
while True:
    emoji_id_chunk = emoji_id_list[i * 10: (i * 10) + 10]
    if len(emoji_id_chunk) == 0:
        break
    i += 1
    delete_req = {'i': auth_token,
                  'ids': emoji_id_chunk}
    res = requests.post(f'https://{myInstanceHost}/api/admin/emoji/delete-bulk',
                        json=delete_req, headers=api_req_header)
    if not res.ok:
        print(f'Error to delete emoji: {emoji_id_chunk}')
    else:
        print(f'emoji {emoji_id_chunk} deleted')
