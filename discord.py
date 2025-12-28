# the api is really harsh so if you use your public account multiple times you could be ratelimited and the account can get disbaled (also ik the proxy function sucks ass i need to make a better one)
import requests

class Status:
    Ok = 'ok'
    Bad = 'bad'
    Mfa = 'mfa'
    Custom = 'custom'
    Retry = 'retry'
    Banned = 'banned'
    Captcha = 'captcha'
    Ratelimited = 'ratelimited'

def proxy(proxi: str):
    if not proxi:
        return None
    if not proxi.startswith(("http://", "https://", "socks5://", "socks4://")):
        proxi = "http://" + proxi
    return {"http": proxi, "https": proxi}

def clearcookie(session):
    session.cookies.clear()

session = requests.Session()

def login(email, password, proxy = None):
    clearcookie(session)

    p = {
        "login": email,
        "password": password,
        "undelete": False,
        "captcha_key": None,
        "login_source": None,
        "gift_code_sku_id": None
    }
    h = {
        "Content-Type": "application/json",
        "Host": "discord.com",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE0LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIwMjMyNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
        "X-Fingerprint": "1114921074073796628.RAOlVbPKcjJXtMcp3f8BK5eUbNs",
        "X-Debug-Options": "bugReporterEnabled",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Failed-Requests": "1",
        "X-Discord-Timezone": "Indian/Mauritius",
        "X-Discord-Locale": "en-US",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept": "*/*",
        "Origin": "https://discord.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://discord.com/login",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "__dcfduid=45d00f9002df11eea1372b830b2009b9; __sdcfduid=45d00f9102df11eea1372b830b2009b954f2ae40b94adfcd8455145309fcd72ee6a94afc57611b5fef8ed4ecd2adc316; __cfruid=e67862390d00db3461e594b9769a8e8870452c38-1685886846; locale=en-US; __cf_bm=SX7Si1MrcXK509PRPJtbEHHIUtzSAid4AMOeZTXKnck-1685886847-0-AXs7NTo+txPzO+lzS3WjGQjEVU90vezQlt8U1hcAm7VxXu1Ek1bjw1yoBwyjQ+s6YjQgXVYPCS2AneP/8l2BQ2F2WgD+HqJS+eV3QphV0j2Z; OptanonConsent=isIABGlobal=false&datestamp=Sun+Jun+04+2023+17%3A54%3A06+GMT%2B0400+(Mauritius+Standard+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _gcl_au=1.1.80443082.1685886847; _ga=GA1.1.2086961407.1685886847; _ga_Q149DFWHT7=GS1.1.1685886847.1.0.1685886849.0.0.0",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "155"
    }
    r = session.post("https://discord.com/api/v9/auth/login",headers=h, json=p, proxies=proxy)

    if "Login or password is invalid." in r.text:
        return Status.Bad, r
    if "502 Bad Gateway" in r.text:
        return Status.Bad, r
    if "INVALID_LOGIN" in r.text:
        return Status.Bad, r
    if "Status code: None" in r.text:
        return Status.Bad, r
    if r.status_code == 400:
        return Status.Bad, r
    if "Your account has been disabled." in r.text:
        return Status.Banned, r
    if "ACCOUNT_PERMANENTLY_DISABLED" in r.text:
        return Status.Banned, r
    if "\"token\":\"" in r.text:
        return Status.Ok, r
    if "Ratelimited" in r.text:
        return Status.Retry
    if "captcha-required" in r.text:
        return Status.Captcha, r
    if "captcha-key" in r.text:
        return Status.Captcha, r
    if "Please try again in a few minutes." in r.text:
        return Status.Ratelimited, r
    else:
        return Status.Custom, r

def main():
    email = "email"
    password = "password"

    proxi = None
    proxie = proxy(proxi)

    status, response = login(email, password, proxie)

    print(status)
    print(f"{email}:{password}")
    print(response.text)

if __name__ == "__main__":
    main()
