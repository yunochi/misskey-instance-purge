import requests
import yaml

with open('config.yaml', 'r') as yamlFile:
    config_data = yaml.load(yamlFile, Loader=yaml.FullLoader)

auth_token = f'{config_data["token"]}'
myInstanceHost = config_data["myInstanceHost"]
user_list_req = {"i": f'{auth_token}', "host": config_data['host'], "limit": 100}
api_req_header = {'Content-type': 'application/json', 'Accept': 'application/json'}

user_list = []
id_list = []

page = 0
while True:
    print(f'get user list... {page}')
    if len(id_list) != 0:
        user_list_req['untilId'] = id_list[-1]
    res = requests.post(f'https://{myInstanceHost}/api/federation/users', json=user_list_req, headers=api_req_header)
    if not res.ok:
        print(f'Fail to get user list! Code:{res.status_code}, Response: {res.text}')
        break
    if len(res.json()) == 0:
        break
    page += 1
    user_list.extend(res.json())
    id_list.extend(list(map(lambda x: x["id"], res.json())))


print(*list(map(lambda x: [x["id"], x["url"]], user_list)), sep='\n')
print(f'Will delete {len(id_list)} user(s)...')
user_input = input('Are you sure? Enter "yes" in UPPERCASE \n(YES/no)\n')
if user_input != 'YES':
    print("exit!")
    exit(0)

for uid in id_list:
    delete_req = {'i': auth_token,
                  'userId': uid}
    res = requests.post(f'https://{myInstanceHost}/api/admin/delete-account', json=delete_req, headers=api_req_header)
    if not res.ok:
        print(f'Error to delete {uid}')
    else:
        print(f'{uid} deleted')

