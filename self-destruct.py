import requests
import yaml

with open('config.yaml', 'r') as yamlFile:
    config_data = yaml.load(yamlFile, Loader=yaml.FullLoader)

auth_token = config_data["token"]
myInstanceHost = config_data["myInstanceHost"]
user_list_req = {"i": f'{auth_token}', "limit": 100, "origin": 'local'}
api_req_header = {'Content-type': 'application/json', 'Accept': 'application/json'}

user_list = []
user_id_list = []
page = 0
while True:
    print(f'Get local user list... {page}')
    user_list_req['offset'] = page * 100
    res = requests.post(f'https://{myInstanceHost}/api/admin/show-users',
                        json=user_list_req, headers=api_req_header)
    if not res.ok:
        print(f'Fail to get user list! Code:{res.status_code}, Response: {res.text}')
        break
    if len(res.json()) == 0:
        break
    page += 1
    user_list.extend(res.json())
    user_id_list.extend(list(map(lambda x: x["id"], res.json())))

uid_list_with_username = list(map(lambda x: {"id": x["id"], "username": x["username"]}, user_list))

for uid_with_url in uid_list_with_username:
    print(f'user: {uid_with_url["id"]} ( {uid_with_url["username"]} )')

print(f'Will Run Self-Destruct. Delete {len(user_id_list)} user(s)...')
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
        print(f'Error to delete {uid} - Code:{res.status_code}, Text:{res.text}')
    else:
        print(f'User {uid} deleted')

