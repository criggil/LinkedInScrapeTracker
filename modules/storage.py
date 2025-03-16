from datetime import datetime
from typing import Dict

from sqlalchemy.orm import joinedload

from database.Models import Search, Match, Post
from database.database import setup_database


class DatabaseStorage:
    """
    A storage class that wraps database.py to handle search operations
    """
    def __init__(self, db_path='sqlite:///linkedin_data.db'):
        """
        Initialize the database connection
        """
        self.engine, self.Session = setup_database(db_path)

    def get_all_searches(self):
        """
        Get all saved searches from the database

        Returns:
            list: A list of Search objects
        """
        session = self.Session()
        try:
            searches = session.query(Search).all()
            return searches
        finally:
            session.close()

    def get_search(self, search_id: int):
        """
        Get a specific search by ID

        Args:
            search_id (int): The ID of the search to retrieve

        Returns:
            Search: The search object if found, None otherwise
        """
        session = self.Session()
        try:
            search = session.query(Search).filter(Search.id == search_id).first()
            return search
        finally:
            session.close()

    def save_search(self, search_data):
        """
        Save a search to the database

        Args:
            search_data (dict): A dictionary containing search data with the following keys:
                - id (int): The ID of the search (optional for new searches)
                - name (str): The name of the search
                - type (str): The type of search (user, company, topic, or job)
                - keywords (str): Keywords or usernames
                - notify (bool): Whether to notify on matches

        Returns:
            int: The ID of the saved search
        """
        session = self.Session()
        try:
            # Check if id is provided and if it exists
            if 'id' in search_data and search_data['id']:
                existing_search = session.query(Search).filter(
                    Search.id == search_data['id']
                ).first()

                if existing_search:
                    # Update existing search
                    if 'name' in search_data:
                        existing_search.name = search_data['name']
                    if 'type' in search_data:
                        existing_search.type = search_data['type']
                    if 'usernames' in search_data:
                        existing_search.type = search_data['usernames']
                    if 'keywords' in search_data:
                        existing_search.keyword = search_data['keywords']
                    if 'notify' in search_data:
                        existing_search.notify = search_data['notify']

                    session.commit()
                    return existing_search.id

            # Create new search
            search = Search(
                id=search_data.get('id'),  # Will be None for new searches
                name=search_data['name'],
                type=search_data['type'],
                usernames=search_data.get('usernames'),
                keywords=search_data.get('keywords'),
                notify=search_data.get('notify', False)
            )

            session.add(search)
            session.commit()
            return search.id
        finally:
            session.close()

    def delete_search(self, search_id: int):
        """
        Delete a search from the database

        Args:
            search_id (int): The ID of the search to delete

        Returns:
            bool: True if the search was deleted, False otherwise
        """
        session = self.Session()
        try:
            search = session.query(Search).filter(Search.id == search_id).first()
            if search:
                session.delete(search)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def save_match(self, match_data):
        """
        Save a match to the database

        Args:
            match_data (dict): A dictionary containing match data with the following keys:
                - id (int): The ID of the match (optional for new matches)
                - search_id (int): The ID of the search
                - post_id (int): The ID of the post
                - matched_at (datetime): When the match occurred

        Returns:
            int: The ID of the saved match
        """
        session = self.Session()
        try:
            # Check if id is provided and if it exists
            if 'id' in match_data and match_data['id']:
                existing_match = session.query(Match).filter(
                    Match.id == match_data['id']
                ).first()

                if existing_match:
                    # Update existing match
                    if 'search_id' in match_data:
                        existing_match.search_id = match_data['search_id']
                    if 'post_id' in match_data:
                        existing_match.post_id = match_data['post_id']
                    if 'matched_at' in match_data:
                        existing_match.matched_at = match_data['matched_at']

                    session.commit()
                    return existing_match.id

            # Create new match
            match = Match(
                id=match_data.get('id'),  # Will be None for new matches
                search_id=match_data['search_id'],
                post_id=match_data['post_id'],
                matched_at=match_data.get('matched_at', datetime.now())
            )

            session.add(match)
            session.commit()
            return match.id
        finally:
            session.close()

    def get_matches(self, search_id: int):
        """
        Get all matches for a specific search

        Args:
            search_id (int): The ID of the search

        Returns:
            list: A list of Match objects
        """
        session = self.Session()
        try:
            matches = session.query(Match).filter(Match.search_id == search_id).all()
            return matches
        finally:
            session.close()

    def get_matches_paginated(self, search_id: int, page=1, per_page=10):
        """
        Get matches for a specific search with pagination

        Args:
            search_id (int): The ID of the search
            page (int): The page number (1-indexed)
            per_page (int): The number of matches per page

        Returns:
            tuple: (matches, total_count) - A list of Match objects and the total count of matches
        """
        session = self.Session()
        try:
            # Calculate offset
            offset = (page - 1) * per_page

            # Get matches with pagination
            matches = (session.query(Match)
                       .filter(Match.search_id == search_id)
                       .options(joinedload(Match.posts))
                       .order_by(Match.matched_at.desc())
                       .offset(offset)
                       .limit(per_page)
                       .all())

            # Get total count of matches for this search
            total_count = session.query(Match).filter(Match.search_id == search_id).count()

            return matches, total_count
        finally:
            session.close()

    def delete_matches(self, search_id: int):
        """
        Delete all matches for a specific search

        Args:
            search_id (int): The ID of the search

        Returns:
            int: The number of matches deleted
        """
        session = self.Session()
        try:
            count = session.query(Match).filter(Match.search_id == search_id).delete()
            session.commit()
            return count
        finally:
            session.close()

    def save_matches(self, search_id: int, matches: list[Dict], replace=False):
        """
        Save multiple matches for a specific search

        Args:
            search_id (int): The ID of the search
            matches (list): A list of dictionaries containing match data
            replace (bool): If True, replaces all existing matches instead of appending

        Returns:
            int: The number of matches saved
        """
        # If replace is True, delete all existing matches for this search
        if replace:
            self.delete_matches(search_id)

        # Save each match individually
        count = 0
        for match in matches:
            # Add search_id to the match data
            match_data = match.copy()
            match_data['search_id'] = search_id

            # Add matched_at timestamp if not present
            if 'matched_at' not in match_data:
                match_data['matched_at'] = datetime.now()

            # Save the match
            self.save_match(match_data)
            count += 1

        return count

    def get_all_posts(self):
        """
        Get all saved posts from the database

        Returns:
            list: A list of Post objects
        """
        session = self.Session()
        try:
            return session.query(Post).all()
        finally:
            session.close()

    def get_posts(self, page=1, per_page=10):
        """
        Get posts with pagination

        Args:
            page (int): The page number (1-indexed)
            per_page (int): The number of posts per page

        Returns:
            tuple: (posts, total_count) - A list of Post objects and the total count of posts
        """
        session = self.Session()
        try:
            # Calculate offset
            offset = (page - 1) * per_page

            # Get posts with pagination
            posts = session.query(Post).order_by(Post.timestamp.desc()).offset(offset).limit(per_page).all()

            # Get total count of posts
            total_count = session.query(Post).count()

            return posts, total_count
        finally:
            session.close()
