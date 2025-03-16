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
            # Skip the first line which is '['
            f.readline()
            
            for line in f:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Remove trailing comma if present
                line = line.rstrip(',\n')
                
                # Skip the last line which is ']'
                if line == ']':
                    continue
                    
                try:
                    post = json.loads(line)
                    # Extract only needed fields
                    simplified_post = {
                        'id': str(post.get('id', '')),
                        'author': post.get('user_id', ''),
                        'content': post.get('post_text', ''),
                        'timestamp': post.get('date_posted', '')
                    }
                    current_batch.append(simplified_post)
                    
                    if len(current_batch) >= self.batch_size:
                        yield current_batch
                        current_batch = []
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line")
                    continue
            
            # Yield remaining posts
            if current_batch:
                yield current_batch

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
            
            return any(keyword.lower().strip() in content 
                      for keyword in keywords)
        
        return False
