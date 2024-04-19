import json, requests, datetime, colorama, aiohttp
from colorama import Fore; colorama.init()

class Xbox:
    def removeInvalidTokens(invalids: list[str]):
        with open('data/tokens.txt', 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in lines:
                if line.strip() not in invalids:
                    f.write(line)
    
    def getProfile(gamertag: str):
        try:
            r = requests.get(f'https://xbl.io/api/v2/search/{gamertag}', headers={'X-Authorization': 'k0osgso04o0ckssg4kkwocogskokowkw0os'})
            return r.json()
        except:
            return False
        
    @staticmethod
    def getTokens():
        with open('data/tokens.txt', 'r') as f:
            return f.read().splitlines()

    def isTokenValid(token: str, tokens: list):
        if token == "" or token == None:
            return False
        
        beginning = token.split('.')[0]
        if beginning == "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkExMjhDQkMtSFMyNTYiLCJ6aXAiOiJERUYiLCJ4NXQiOiJxcEQtU2ZoOUg3NFFHOXlMN1hSZXJ5RmZvbk0iLCJjdHkiOiJKV1QifQ":
            tokens.append(token)
            return True
        
        return False
    
    def checkToken(token: str, invalids=None):
        if invalids is None:
            invalids = []

        json_payload = {'RelyingParty': 'http://xboxlive.com', 'TokenType': 'JWT', 'Properties': {'UserTokens': [token], 'SandboxId': 'RETAIL'}}
        try:
            response = requests.post('https://xsts.auth.xboxlive.com/xsts/authorize', json=json_payload)
            if response.status_code in (401, 200, 400):
                invalids.append(token)
                return response, invalids
        except requests.exceptions.RequestException as e:
            
            invalids.append(token)
            return False, invalids

        return False, invalids

    async def sendFollow(token: str, clientInput: str, user: str):
        response, invalids = Xbox.checkToken(token)
        with open('data/blacklist.txt', 'r') as file:
            blacklist = file.readlines()
            if f"{clientInput}\n" in blacklist:
                return False, 'Gamertag Blacklisted'
            else:
                if isinstance(response, requests.models.Response) and response.status_code == 200:
                    tokenx = 'XBL3.0 x={};{}'.format(response.json()['DisplayClaims']['xui'][0]['uhs'], response.json()['Token'])
                    headers = {'Authorization': tokenx, "X-XBL-Contract-Version": "2"}
                    response = requests.put(f"https://social.xboxlive.com/users/xuid({response.json()['DisplayClaims']['xui'][0]['xid']})/people/xuid({clientInput})?app_name=xbox_on_windows&app_ctx=user_profile", headers=headers)
                    if '"gtg":null' not in response.text:
                        print(f"{Fore.GREEN}Successfully sent follower to {clientInput} from {response.json()['DisplayClaims']['xui'][0]['gtg']} sent by {user}! ")

                else:
                    pass
            
    
    async def black(xuid:int) -> bool:
        with open('data/blacklist.txt', 'r') as file:
            gamertags = file.readlines()
        if f"{xuid}\n" in gamertags:
            print(f"\n[\033[1;32;40m!\033[1;37;40m] Order: [\033[1;32;40m{xuid}\033[1;37;40m] Already Blacklisted")
            return False, 'Gamertag Blacklisted'
        elif f"{xuid}\n" not in gamertags:
            with open('data/blacklist.txt', 'a') as file:
                file.write(f"{xuid}\n")
            print(f"\n[\033[1;32;40m!\033[1;37;40m] Order: [\033[1;32;40m{xuid}\033[1;37;40m] Blacklisted | Status: [\033[1;32;40mTRUE\033[1;37;40m]")
            return True, f'Successfully Blacklisted {xuid}'
    

class Authentication:
    def addSubscription(userId: int, days: int) -> bool:
        with open('data/users.json', 'r') as f:
            subscriptions = json.load(f)

        if str(userId) in subscriptions:
            end_date = datetime.datetime.strptime(subscriptions[str(userId)], '%Y-%m-%d %H:%M:%S.%f')
            if datetime.datetime.now() < end_date:
                return False, 'User already has an active subscription.'

        end_date = datetime.datetime.now() + datetime.timedelta(days=days)
        subscriptions[str(userId)] = end_date.strftime('%Y-%m-%d %H:%M:%S.%f')

        with open('data/users.json', 'w') as f:
            json.dump(subscriptions, f, indent=4)

        return True, f'Successfully added subscription for {days} days.'

    def removeSubscription(userId: int) -> bool:
        with open('data/users.json', 'r') as f:
            subscriptions = json.load(f)

        if str(userId) not in subscriptions:
            return False

        del subscriptions[str(userId)]

        with open('data/users.json', 'w') as f:
            json.dump(subscriptions, f, indent=4)

        return True
    
    def getSubscription(userId: int) -> str:
        with open('data/users.json', 'r') as f:
            subscriptions = json.load(f)

        if str(userId) not in subscriptions:
            return 'No subscription found.'

        end_date = datetime.datetime.strptime(subscriptions[str(userId)], '%Y-%m-%d %H:%M:%S.%f')
        if datetime.datetime.now() > end_date:
            Authentication.removeSubscription(userId)
            return 'No subscription found.'

        return end_date.strftime('%m-%d-%y %H:%M%p')
    
    def checkSubscription(userId: int) -> bool:
        with open('data/users.json', 'r') as f:
            subscriptions = json.load(f)

        if str(userId) not in subscriptions.keys():
            return False

        end_date = datetime.datetime.strptime(subscriptions[str(userId)], '%Y-%m-%d %H:%M:%S.%f')
        if datetime.datetime.now() > end_date:
            Authentication.removeSubscription(userId)
            return False

        return True
    
    def getSubscriptions() -> dict:
        with open('data/users.json', 'r') as f:
            subscriptions = json.load(f)

        return subscriptions
