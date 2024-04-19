import os, requests, random, psutil, aiohttp, asyncio, itertools, logging
from tasksio import TaskPool
from colorama import init

init()    
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
class Handler:
    def __init__(self, main):
        self.user_tokens = self.collect_user_tokens()
        self.processes = self.collect_total_processes()
        self.main = main
        
    @staticmethod
    def collect_user_tokens():
        with open("tokens.txt", "r") as file:
            return file.read().splitlines()
        
    @staticmethod   
    def collect_total_processes():
        return len([process for process in psutil.process_iter()])
    
    
    async def grab_16h_token(self, session, user_token):
        json = {'RelyingParty': 'http://accounts.xboxlive.com', 'TokenType': 'JWT', 'Properties': {'UserTokens': [user_token], 'SandboxId': 'RETAIL'}}
        async with session.post("https://52.156.147.113/xsts/authorize", json=json) as response:
            if response.status == 200:
                data = await response.json()
                uhs = data["DisplayClaims"]["xui"][0]["uhs"]
                token = data["Token"]
                self.main._16h_tokens.append(f"XBL3.0 x={uhs};{token}") 
                for spin in ["\\", "-", "/", "|", "|"]:
                    print(f"[\033[1;32;40m{spin}\033[1;37;40m] Tokens: {len(self.main._16h_tokens)} | Processes: {self.processes}", end="\r", flush=True)
         
    async def initalize(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            await asyncio.gather(*[self.grab_16h_token(session, user_token) for user_token in self.user_tokens])
                
class Main:
    def __init__(self):
        
        self.token_index = -1
        self._16h_tokens = []
        self.reserved = False
        self.attempts = 0
        
        self.rl = 0 
        self.session = None

    def token(self):
        self.token_index += 1
        if self.token_index >= len(self._16h_tokens):
            self.token_index = 0
        return self._16h_tokens[self.token_index]


    
    
    async def port(self) -> None:
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    

    async def claim(self):
        x = self.token()
        json={ "dateOfBirth": "2000-01-01T00:00:00.0000000", "email": "", "firstName": "", "gamerTag": "", "gamerTagChangeReason": None, "homeAddressInfo": { "city": None, "country": "US", "postalCode": None, "state": None, "street1": None, "street2": None },"homeConsole": None,"imageUrl": "", "isAdult": True, "lastName": "", "legalCountry": "US", "locale": "en-US", "midasConsole": None, "msftOptin": True, "ownerHash": None, "ownerXuid": None, "partnerOptin": True, "requirePasskeyForPurchase": False, "requirePasskeyForSignIn": False, "subscriptionEntitlementInfo": None, "touAcceptanceDate": "2000-01-01T00:00:00.0000000", "userHash": x.split(";")[0].split("x=")[1], "userKey": None, "userXuid": "216258806147975844"}
        headers = {'x-xbl-contract-version': '2', 'Authorization': x}
        async with self.session.post('https://accountstroubleshooter.xboxlive.com/users/current/profile', json=json, headers=headers) as response:
            #print(response.status)
            if response.status == 200:
                self.attempts += 1
            else:
                self.rl += 1
            
            
    async def printer(self):
        while not self.reserved:
            for spinner in ["|", "/", "-", "\\"]:
                print(f"[\x1b[1;32m{spinner}\x1b[39m] Converted: {self.attempts} | Errors: {self.rl}", end="\r", flush=True)
                await asyncio.sleep(0.1)
                

    
    async def initalize(self):
        await self.port()
        asyncio.create_task(self.printer())
        async with TaskPool(threads) as pool:
            while not self.reserved:
                await pool.put(self.claim())
         
                    
main = Main()
handler = Handler(main)
print('[\033[1;32;40m+\033[1;37;40m] Heasi´s Converter')
asyncio.run(handler.initalize())
print()
print('[\033[1;32;40m?\033[1;37;40m]', end='');threads = int(input(" Threads?: "))
print()
asyncio.run(main.initalize())
         
                
        
