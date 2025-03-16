import json
from typing import List, Dict, Generator
import itertools

class PostLoader:
    def __init__(self, file_path: str, batch_size: int = 100):
        self.file_path = file_path
        self.batch_size = batch_size

    def load_posts_batch(self) -> Generator[List[Dict], None, None]:
        """
        Generator that yields batches of posts to avoid loading entire file
        """
        current_batch = []

        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                # Read the entire file content
                content = f.read()
                # Parse JSON content
                if content.startswith('\ufeff'):  # Remove BOM if present
                    content = content[1:]
                data = json.loads(content)

                # Process posts
                for post in data:
                    try:
                        simplified_post = {
                            'id': str(post['id']),
                            'author': post['user_id'],
                            'content': post['post_text'],
                            'timestamp': post['date_posted']
                        }
                        current_batch.append(simplified_post)

                        if len(current_batch) >= self.batch_size:
                            yield current_batch
                            current_batch = []
                    except KeyError as e:
                        print(f"Skipping post due to missing field: {e}")
                        continue

                # Yield remaining posts
                if current_batch:
                    yield current_batch

            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    def search_posts(self, criteria: Dict, max_results: int = 100) -> List[Dict]:
        """
        Search through posts using criteria and return matches
        """
        matches = []
        for batch in self.load_posts_batch():
            for post in batch:
                if self._matches_criteria(post, criteria):
                    matches.append(post)
                    if len(matches) >= max_results:
                        return matches
        return matches

    def _matches_criteria(self, post: Dict, criteria: Dict) -> bool:
        """
        Check if a post matches the search criteria
        """
        if criteria['type'] == 'user':
            return any(username.lower().strip() in post['author'].lower() 
                      for username in criteria['usernames'])

        elif criteria['type'] in ['topic', 'job']:
            content = post['content'].lower()
            keywords = criteria.get('keywords', [])

            # For job searches, include default job-related keywords
            if criteria['type'] == 'job':
                keywords = list(keywords) + ['hiring', 'looking for', 'job opportunity']

            # Print debug information
            print(f"Keywords to match: {keywords}")
            print(f"Post content: {content[:100]}...")  # Print first 100 chars for readability

            matched_keywords = [kw for kw in keywords if kw.lower().strip() in content]
            if matched_keywords:
                print(f"Matched keywords: {matched_keywords}")
                return True

            return False

        return False