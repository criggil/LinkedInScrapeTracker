import json
import os
from datetime import datetime

class Storage:
    def __init__(self):
        self.matches_dir = "matches"
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """
        Create the matches directory if it doesn't exist
        """
        if not os.path.exists(self.matches_dir):
            os.makedirs(self.matches_dir)

    def save_matches(self, search_id, matches):
        """
        Save matched posts for a specific search
        """
        filename = os.path.join(self.matches_dir, f"{search_id}.json")
        
        existing_matches = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing_matches = json.load(f)

        # Add timestamp to new matches
        for match in matches:
            match['matched_at'] = datetime.now().isoformat()

        # Combine existing and new matches, avoiding duplicates
        existing_ids = {m['id'] for m in existing_matches}
        new_matches = [m for m in matches if m['id'] not in existing_ids]
        all_matches = existing_matches + new_matches

        with open(filename, 'w') as f:
            json.dump(all_matches, f, indent=2)

    def get_matches(self, search_id):
        """
        Retrieve matches for a specific search
        """
        filename = os.path.join(self.matches_dir, f"{search_id}.json")
        
        if not os.path.exists(filename):
            return []

        with open(filename, 'r') as f:
            return json.load(f)
