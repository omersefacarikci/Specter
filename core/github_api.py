import requests
import time

class GitHubAPI:
    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        })
        self.base = "https://api.github.com"

    def _get_paged(self, url: str) -> list:
        results = []
        page = 1
        while True:
            r = self.session.get(url, params={"per_page": 100, "page": page})
            r.raise_for_status()
            data = r.json()
            if not data:
                break
            results.extend(data)
            page += 1
            time.sleep(0.3)
        return results

    def get_followers(self) -> list:
        return self._get_paged(f"{self.base}/users/{self.username}/followers")

    def get_following(self) -> list:
        return self._get_paged(f"{self.base}/users/{self.username}/following")

    def get_user_detail(self, login: str) -> dict:
        r = self.session.get(f"{self.base}/users/{login}")
        r.raise_for_status()
        return r.json()

    def get_my_repos(self) -> list:
        return self._get_paged(f"{self.base}/user/repos")

    def block_user(self, login: str) -> bool:
        r = self.session.put(f"{self.base}/user/blocks/{login}")
        return r.status_code == 204

    def unfollow_user(self, login: str) -> bool:
        r = self.session.delete(f"{self.base}/user/following/{login}")
        return r.status_code == 204

    def star_repo(self, owner: str, repo: str) -> bool:
        r = self.session.put(f"{self.base}/user/starred/{owner}/{repo}",
                             headers={"Content-Length": "0"})
        return r.status_code == 204

    def validate_token(self) -> bool:
        r = self.session.get(f"{self.base}/user")
        return r.status_code == 200
