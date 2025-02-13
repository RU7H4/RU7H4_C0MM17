import os
import subprocess
import requests
from datetime import datetime, timedelta
import getpass
banner = """
RRRRRRRRRRRRRRRRR   UUUUUUUU     UUUUUUUU77777777777777777777HHHHHHHHH     HHHHHHHHH     444444444  
R::::::::::::::::R  U::::::U     U::::::U7::::::::::::::::::7H:::::::H     H:::::::H    4::::::::4  
R::::::RRRRRR:::::R U::::::U     U::::::U7::::::::::::::::::7H:::::::H     H:::::::H   4:::::::::4  
RR:::::R     R:::::RUU:::::U     U:::::UU777777777777:::::::7HH::::::H     H::::::HH  4::::44::::4  
  R::::R     R:::::R U:::::U     U:::::U            7::::::7   H:::::H     H:::::H   4::::4 4::::4  
  R::::R     R:::::R U:::::D     D:::::U           7::::::7    H:::::H     H:::::H  4::::4  4::::4  
  R::::RRRRRR:::::R  U:::::D     D:::::U          7::::::7     H::::::HHHHH::::::H 4::::4   4::::4  
  R:::::::::::::RR   U:::::D     D:::::U         7::::::7      H:::::::::::::::::H4::::444444::::444
  R::::RRRRRR:::::R  U:::::D     D:::::U        7::::::7       H:::::::::::::::::H4::::::::::::::::4
  R::::R     R:::::R U:::::D     D:::::U       7::::::7        H::::::HHHHH::::::H4444444444:::::444
  R::::R     R:::::R U:::::D     D:::::U      7::::::7         H:::::H     H:::::H          4::::4  
  R::::R     R:::::R U::::::U   U::::::U     7::::::7          H:::::H     H:::::H          4::::4  
RR:::::R     R:::::R U:::::::UUU:::::::U    7::::::7         HH::::::H     H::::::HH        4::::4  
R::::::R     R:::::R  UU:::::::::::::UU    7::::::7          H:::::::H     H:::::::H      44::::::44
R::::::R     R:::::R    UU:::::::::UU     7::::::7           H:::::::H     H:::::::H      4::::::::4
RRRRRRRR     RRRRRRR      UUUUUUUUU      77777777            HHHHHHHHH     HHHHHHHHH      4444444444
          RU7H C0MM17 - Fake GitHub Commits
"""
print(banner)
github_user = input("Enter your GitHub username: ")
github_token = getpass.getpass("Enter your GitHub personal access token: ")
repo_name = input("Enter a name for the new private repository: ")
days = int(input("Enter the number of days for fake commits: "))
api_url = "https://api.github.com/user/repos"
repo_data = {
    "name": repo_name,
    "private": True
}
print("[+] Creating private repository on GitHub...")
response = requests.post(api_url, json=repo_data, auth=(github_user, github_token))
if response.status_code == 201:
    print(f"[✓] Repository '{repo_name}' created successfully.")
else:
    print(f"[✗] Failed to create repository: {response.json()}")
    exit(1)
repo_url = f"https://{github_user}:{github_token}@github.com/{github_user}/{repo_name}.git"
os.makedirs("fake_commits", exist_ok=True)
os.chdir("fake_commits")
subprocess.run(["git", "init"])
subprocess.run(["git", "remote", "add", "origin", repo_url])
for i in range(days):
    fake_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S")
    commit_message = f"Update {fake_date}"
    with open("commit.txt", "w") as file:
        file.write(commit_message)
    subprocess.run(["git", "add", "commit.txt"])
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = fake_date
    env["GIT_COMMITTER_DATE"] = fake_date
    subprocess.run(["git", "commit", "-m", commit_message], env=env)
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "push", "-u", "origin", "main"])
print("[✓] Fake commits created and pushed successfully!")
