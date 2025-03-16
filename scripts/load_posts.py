#!/usr/bin/env python3
"""
Test script for the database schema.
This script creates the database tables, inserts some sample data, and performs basic queries.
"""
import json
import sys
import os

from database.Models import Post

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from database.database import setup_database


def main():
    # Set up the database
    print("Setting up the database...")
    engine, Session = setup_database()
    session = Session()

    # Read json
    with open('../data/linkedin_posts.json') as f:
        posts = json.load(f)

    try:
        for post in posts:
            post_obj = Post(
                post_url=post['url'],
                user_name=post['user_id'],
                user_url=post['use_url'],
                content=post['post_text'],
                timestamp=datetime.fromisoformat(post['date_posted']),
                likes=post['num_likes'],
                comments=post['num_comments'],
                shares=0
            )
            session.add(post_obj)
            session.commit()
            print(f"Created posts: {post_obj}")

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
