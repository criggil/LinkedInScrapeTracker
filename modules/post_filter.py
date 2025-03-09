class PostFilter:
    def filter_posts(self, posts, criteria):
        """
        Filter posts based on search criteria
        """
        matches = []
        search_type = criteria['type']

        for post in posts:
            if self._matches_criteria(post, criteria):
                matches.append({
                    'id': post['id'],
                    'author': post['author'],
                    'content': post['content'],
                    'timestamp': post['timestamp']
                })

        return matches

    def _matches_criteria(self, post, criteria):
        """
        Check if a post matches the given criteria
        """
        if criteria['type'] == 'user':
            return any(username.lower().strip() in post['author'].lower() 
                      for username in criteria['usernames'])

        elif criteria['type'] == 'topic' or criteria['type'] == 'job':
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