#!/usr/bin/env python3
import argparse
import json
import sys
from modules.post_filter import PostFilter
from modules.storage import Storage
from modules.config_manager import ConfigManager

def setup_argparse():
    parser = argparse.ArgumentParser(description='LinkedIn Post Monitor')
    parser.add_argument('--input', '-i', type=str, help='Input JSON file with LinkedIn posts')
    parser.add_argument('--add-search', '-a', action='store_true', help='Add a new saved search')
    parser.add_argument('--list-searches', '-l', action='store_true', help='List all saved searches')
    parser.add_argument('--process', '-p', action='store_true', help='Process posts and find matches')
    parser.add_argument('--view-matches', '-v', type=str, help='View matches for a specific search ID')

    # New arguments for non-interactive search addition
    parser.add_argument('--name', type=str, help='Name for the new search')
    parser.add_argument('--type', choices=['user', 'topic', 'job'], help='Type of search')
    parser.add_argument('--keywords', type=str, help='Keywords for topic/job search (comma-separated)')
    parser.add_argument('--usernames', type=str, help='Usernames for user search (comma-separated)')
    parser.add_argument('--notify', action='store_true', help='Enable notifications for the search')

    return parser

def add_new_search(config_manager, args):
    if not args.name or not args.type:
        print("Error: --name and --type are required for adding a search")
        return

    criteria = {"type": args.type}

    if args.type == "user":
        if not args.usernames:
            print("Error: --usernames required for user search")
            return
        criteria["usernames"] = args.usernames.split(",")
    elif args.type in ["topic", "job"]:
        if not args.keywords:
            print("Error: --keywords required for topic/job search")
            return
        criteria["keywords"] = args.keywords.split(",")
        if args.type == "job":
            criteria["keywords"].extend(["hiring", "looking for", "job opportunity"])

    search_id = config_manager.add_search(args.name, criteria, args.notify)
    print(f"Saved search '{args.name}' added successfully! (ID: {search_id})")

def main():
    parser = setup_argparse()
    args = parser.parse_args()

    config_manager = ConfigManager()
    storage = Storage()
    post_filter = PostFilter()

    if args.add_search:
        add_new_search(config_manager, args)
        return

    if args.list_searches:
        searches = config_manager.get_all_searches()
        print("\n=== Saved Searches ===")
        for search_id, search in searches.items():
            print(f"\nID: {search_id}")
            print(f"Name: {search['name']}")
            print(f"Type: {search['criteria']['type']}")
            if search['criteria']['type'] == 'user':
                print(f"Usernames: {', '.join(search['criteria']['usernames'])}")
            else:
                print(f"Keywords: {', '.join(search['criteria'].get('keywords', []))}")
            print(f"Notifications: {'Enabled' if search['notify'] else 'Disabled'}")
        return

    if args.process:
        if not args.input:
            print("Error: Please provide an input JSON file with --input")
            return

        try:
            with open(args.input, 'r') as f:
                data = json.load(f)
                posts = data.get('posts', [])
        except Exception as e:
            print(f"Error loading input file: {e}")
            return

        searches = config_manager.get_all_searches()
        for search_id, search in searches.items():
            matches = post_filter.filter_posts(posts, search['criteria'])
            if matches:
                storage.save_matches(search_id, matches)
                if search['notify']:
                    print(f"\nAlert! New matches for search '{search['name']}':")
                    for match in matches:
                        print(f"- {match['content'][:100]}...")

    if args.view_matches:
        matches = storage.get_matches(args.view_matches)
        if matches:
            print(f"\n=== Matches for Search ID: {args.view_matches} ===")
            for match in matches:
                print(f"\nPost ID: {match['id']}")
                print(f"Content: {match['content']}")
                print(f"Author: {match['author']}")
                print(f"Matched at: {match.get('matched_at', 'N/A')}")
                print("-" * 50)
        else:
            print("No matches found for this search ID")

if __name__ == "__main__":
    main()