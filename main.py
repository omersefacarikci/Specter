import os
import sys
from dotenv import load_dotenv
from core.github_api import GitHubAPI
from core.bot_detector import is_bot
from ui.menu import (
    show_banner, show_menu, show_bot_table, show_unfollow_table,
    show_repos_table, confirm, spinner, success, error, info, console
)

load_dotenv()

def get_config():
    token = os.getenv("GITHUB_TOKEN", "").strip()
    username = os.getenv("GITHUB_USERNAME", "").strip()
    
    if not token or not username:
        error("Something went wrong with .env file!")
        console.print("[dim]→ Copy .env.example file and save it as .env[/dim]")
        sys.exit(1)
    
    return token, username

def action_detect_bots(api: GitHubAPI, dry_run=False):
    info("Followers are being fetched.")
    with spinner("Getting followers from GitHub..."):
        followers = api.get_followers()
    
    info(f"{len(followers)} followers found, analyzing...")
    
    bots = []
    for f in followers:
        with spinner(f"@{f['login']} analyzing..."):
            detail = api.get_user_detail(f["login"])
        result, reason = is_bot(detail)
        if result:
            bots.append({"login": f["login"], "reason": reason})
    
    show_bot_table(bots)
    
    if not bots:
        return
    
    if dry_run:
        info("Dry-run mode: No action will be taken.")
        return
    
    if confirm(f"{len(bots)} accounts will be blocked. Do you want to continue?"):
        for bot in bots:
            if api.block_user(bot["login"]):
                success(f"@{bot['login']} blocked")
            else:
                error(f"@{bot['login']} blocked")

def action_unfollow(api: GitHubAPI, dry_run=False):
    info("Following list is being fetched.")
    with spinner("Fetching following list from GitHub..."):
        following = api.get_following()
    with spinner("Fetching followers from GitHub..."):
        followers = api.get_followers()
    
    follower_logins = {f["login"] for f in followers}
    not_following_back = [u for u in following if u["login"] not in follower_logins]
    
    show_unfollow_table(not_following_back)
    
    if not not_following_back:
        return
    
    if dry_run:
        info("Dry-run mode: No action will be taken.")
        return
    
    if confirm(f"{len(not_following_back)} users will be unfollowed. Do you want to continue?"):
        for u in not_following_back:
            if api.unfollow_user(u["login"]):
                success(f"@{u['login']} unfollowed")
            else:
                error(f"@{u['login']} unfollowed")

def action_star_repos(api: GitHubAPI, dry_run=False):
    info("Getting my repositories...")
    with spinner("Getting my repositories from GitHub..."):
        repos = api.get_my_repos()
    
    show_repos_table(repos)
    
    if dry_run:
        info("Dry-run mode: No action will be taken.")
        return
    
    if confirm(f"{len(repos)} repositories will be starred. Do you want to continue?"):
        for repo in repos:
            owner, name = repo["full_name"].split("/")
            if api.star_repo(owner, name):
                success(f"⭐ {repo['full_name']}")
            else:
                error(f"{repo['full_name']} star'lanamadı")

def action_report(api: GitHubAPI):
    info("Generating full report...")
    
    with spinner("Fetching data..."):
        followers = api.get_followers()
        following = api.get_following()
        repos = api.get_my_repos()
    
    follower_logins = {f["login"] for f in followers}
    not_following_back = [u for u in following if u["login"] not in follower_logins]
    
    bots = []
    for f in followers:
        detail = api.get_user_detail(f["login"])
        result, reason = is_bot(detail)
        if result:
            bots.append({"login": f["login"], "reason": reason})
    
    console.print(f"\n[bold]📊 Account Summary[/bold]")
    console.print(f"  Followers     : [cyan]{len(followers)}[/cyan]")
    console.print(f"  Following     : [cyan]{len(following)}[/cyan]")
    console.print(f"  Repositories  : [cyan]{len(repos)}[/cyan]")
    console.print(f"  Bot suspicious: [red]{len(bots)}[/red]")
    console.print(f"  Not following back: [yellow]{len(not_following_back)}[/yellow]\n")
    
    show_bot_table(bots)
    show_unfollow_table(not_following_back)

def main():
    show_banner()
    token, username = get_config()
    
    api = GitHubAPI(token, username)
    
    info("Verifying token...")
    if not api.validate_token():
        error("Invalid token! Please check your .env file.")
        sys.exit(1)
    success(f"Logged in as @{username}\n")
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            dry = not confirm("Perform actual operation? (No = only list)")
            action_detect_bots(api, dry_run=dry)
        elif choice == "2":
            dry = not confirm("Perform actual operation? (No = only list)")
            action_unfollow(api, dry_run=dry)
        elif choice == "3":
            dry = not confirm("Perform actual operation? (No = only list)")
            action_star_repos(api, dry_run=dry)
        elif choice == "4":
            action_report(api)
        elif choice == "5":
            console.print("\n[dim] Specter closed.[/dim]\n")
            break
        
        console.print()

if __name__ == "__main__":
    main()
