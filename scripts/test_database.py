#!/usr/bin/env python3
"""
Test script for the database schema.
This script creates the database tables, inserts some sample data, and performs basic queries.
"""

import sys
import os

from database.Models import Match, Search, Post

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from database.database import setup_database


def main():
    # Set up the database
    print("Setting up the database...")
    engine, Session = setup_database()
    session = Session()

    try:
        # Create sample posts
        print("\nCreating sample posts...")
        post1 = Post(
            post_url="https://www.linkedin.com/posts/john-doe-123456789-123456789/",
            user_name="John Doe",
            user_url="https://www.linkedin.com/in/john-doe/",
            content="Excited to announce our new product launch!",
            timestamp=datetime.now(),
            likes=100,
            comments=25,
            shares=10
        )

        post2 = Post(
            post_url="https://www.linkedin.com/posts/jane-doe-123456789-123456789/",
            user_name="Jane Doe",
            user_url="https://www.linkedin.com/in/jane-doe/",
            content="We're hiring! Check out our open positions.",
            timestamp=datetime.now(),
            likes=50,
            comments=10,
            shares=5
        )

        session.add_all([post1, post2])
        session.commit()
        print(f"Created posts: {post1}, {post2}")

        # Create sample searches
        print("\nCreating sample searches...")
        search1 = Search(
            id=1,
            name="User Posts",
            type="user",
            keyword="john_doe",
            notify=True
        )

        search2 = Search(
            id=2,
            name="Tech Topics",
            type="topic",
            keyword="AI,SEO,joy,Positive,remote",
            notify=True
        )

        session.add_all([search1, search2])
        session.commit()
        print(f"Created searches: {search1}, {search2}")

        # Create sample matches
        print("\nCreating sample matches...")
        match1 = Match(
            search_id=search1.id,
            post_id=post1.id,
            matched_at=datetime.now()
        )

        match2 = Match(
            search_id=search2.id,
            post_id=post2.id,
            matched_at=datetime.now()
        )

        session.add_all([match1, match2])
        session.commit()
        print(f"Created matches: {match1}, {match2}")

        # Query the database
        print("\nQuerying the database...")

        # Get all posts
        posts = session.query(Post).all()
        print(f"All posts: {posts}")

        # Get all searches
        searches = session.query(Search).all()
        print(f"All searches: {searches}")

        # Get a specific search by ID
        specific_search = session.query(Search).filter(Search.id == 1).first()
        print(f"Specific search: {specific_search}")

        # Get searches with notify=True
        notify_searches = session.query(Search).filter(Search.notify == True).all()
        print(f"Searches with notify=True: {notify_searches}")

        # Get all matches
        matches = session.query(Match).all()
        print(f"All matches: {matches}")

        # Get matches for a specific search
        search_matches = session.query(Match).filter(Match.search_id == search1.id).all()
        print(f"Matches for {search1}: {search_matches}")

        # Get matches for a specific post
        post_matches = session.query(Match).filter(Match.post_id == post1.id).all()
        print(f"Matches for post {post1.id}: {post_matches}")

        print("\nDatabase test completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
