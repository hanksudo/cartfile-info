import os
import re
import sys
import json
import urllib3
urllib3.disable_warnings()

BASE_URL = "https://api.github.com/search/repositories?q={query}"
headers = {
    "user-agent": "Python script"
}

# https://developer.github.com/v3/search/#rate-limit
token = os.getenv("GITHUB_API_TOKEN")
if token is not None:
    headers["Authorization"] = "token " + token

def main(filepath):
    with open(filepath) as f:
        for line in f.read().split("\n"):
            m = re.match(r"github \"(.+)\"", line)
            if m:
                repo_name = m.group(1)
                http = urllib3.PoolManager(1, headers=headers)
                
                r = http.request("GET", BASE_URL.format(query=repo_name))
                response = json.loads(r.data.decode("utf-8"))

                print(repo_name)
                if r.status == 403:
                    print(response["message"])
                else:
                    repo = response["items"][0] 
                    print(repo["description"])
                    print(repo["html_url"])
                print()

def usage():
    print("python app.py Cartfile")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    else:
        main(sys.argv[1])
