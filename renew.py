import os
import sys
import requests

KATABUMP_EMAIL = os.environ.get("KATABUMP_EMAIL")
KATABUMP_PASSWORD = os.environ.get("KATABUMP_PASSWORD")
SERVER_ID = os.environ.get("SERVER_ID")

BASE_URL = "https://katabump.com"

def login(session):
    resp = session.post(
        f"{BASE_URL}/auth/login",
        data={"email": KATABUMP_EMAIL, "password": KATABUMP_PASSWORD},
        allow_redirects=True,
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code}")
        sys.exit(1)
    print("Logged in successfully.")
    return session

def renew(session):
    resp = session.post(
        f"{BASE_URL}/server/renew",
        data={"server_id": SERVER_ID},
        timeout=30,
    )
    if resp.status_code == 200:
        print(f"Renew request sent for server {SERVER_ID}.")
    else:
        print(f"Renew failed: {resp.status_code} - {resp.text[:200]}")
        sys.exit(1)

def main():
    if not all([KATABUMP_EMAIL, KATABUMP_PASSWORD, SERVER_ID]):
        print("Missing required secrets.")
        sys.exit(1)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; KatabumpAutoRenew/1.0)"
    })
    login(session)
    renew(session)
    print("Done.")

if __name__ == "__main__":
    main()
