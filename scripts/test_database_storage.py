#!/usr/bin/env python3
"""
Test script for the DatabaseStorage class.
This script demonstrates how to use the DatabaseStorage class to perform operations on searches.
"""

import sys
import os
import uuid
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.storage import DatabaseStorage
# Import all necessary models to ensure tables are created in the correct order
from database.User import User
from database.Models import Company
from database.Post import PostModel

def main():
    # Initialize the DatabaseStorage
    print("Initializing DatabaseStorage...")
    db_storage = DatabaseStorage()

    # Test saving a new search
    print("\nSaving a new search...")
    search_data = {
        'name': 'Test Search',
        'type': 'topic',
        'keywords': 'python,database,storage',
        'notify': True
    }
    search_id = db_storage.save_search(search_data)
    print(f"Saved search with ID: {search_id}")

    # Test getting a specific search
    print("\nGetting the search we just created...")
    search = db_storage.get_search(search_id)
    if search:
        print(f"Retrieved search: {search}")
        print(f"Search ID: {search.id}")
        print(f"Name: {search.name}")
        print(f"Type: {search.type}")
        print(f"Keyword: {search.keyword}")
        print(f"Notify: {search.notify}")
    else:
        print("Search not found!")

    # Test updating an existing search
    print("\nUpdating the search...")
    updated_search_data = {
        'id': search_id,
        'name': 'Updated Test Search',
        'notify': False
    }
    updated_id = db_storage.save_search(updated_search_data)
    print(f"Updated search with ID: {updated_id}")

    # Test getting the updated search
    print("\nGetting the updated search...")
    updated_search = db_storage.get_search(updated_id)
    if updated_search:
        print(f"Retrieved updated search: {updated_search}")
        print(f"Search ID: {updated_search.id}")
        print(f"Name: {updated_search.name}")
        print(f"Type: {updated_search.type}")
        print(f"Keyword: {updated_search.keyword}")
        print(f"Notify: {updated_search.notify}")
    else:
        print("Updated search not found!")

    # Test getting all searches
    print("\nGetting all searches...")
    all_searches = db_storage.get_all_searches()
    print(f"Found {len(all_searches)} searches:")
    for search in all_searches:
        print(f"- {search.id}: {search.name} ({search.type})")

    # Test deleting the search we created
    print("\nDeleting the search we created...")
    deleted = db_storage.delete_search(search_id)
    if deleted:
        print(f"Successfully deleted search with ID: {search_id}")
    else:
        print(f"Failed to delete search with ID: {search_id}")

    # Verify the search was deleted
    print("\nVerifying the search was deleted...")
    deleted_search = db_storage.get_search(search_id)
    if deleted_search:
        print(f"Search still exists: {deleted_search}")
    else:
        print("Search was successfully deleted!")

    # Create a new search for testing matches
    print("\nCreating a new search for testing matches...")
    search_data = {
        'name': 'Match Test Search',
        'type': 'topic',
        'keywords': 'test,match',
        'notify': True
    }
    search_id = db_storage.save_search(search_data)
    print(f"Created search with ID: {search_id}")

    # Test saving a match
    print("\nSaving a new match...")
    from datetime import datetime
    match_data = {
        'search_id': search_id,
        'post_id': 1,  # Assuming post with ID 1 exists
        'matched_at': datetime.now()
    }
    match_id = db_storage.save_match(match_data)
    print(f"Saved match with ID: {match_id}")

    # Test getting matches for a search
    print("\nGetting matches for the search...")
    matches = db_storage.get_matches(search_id)
    print(f"Found {len(matches)} matches for search {search_id}:")
    for match in matches:
        print(f"- Match ID: {match.id}, Post ID: {match.post_id}, Matched at: {match.matched_at}")

    # Test deleting matches for a search
    print("\nDeleting matches for the search...")
    deleted_count = db_storage.delete_matches(search_id)
    print(f"Deleted {deleted_count} matches for search {search_id}")

    # Verify matches were deleted
    print("\nVerifying matches were deleted...")
    remaining_matches = db_storage.get_matches(search_id)
    if remaining_matches:
        print(f"Found {len(remaining_matches)} matches still exist")
    else:
        print("All matches were successfully deleted!")

    # Clean up by deleting the search
    db_storage.delete_search(search_id)

    print("\nDatabaseStorage test completed!")

if __name__ == "__main__":
    main()
