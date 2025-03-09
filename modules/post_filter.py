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
                    'id': post.get('id', ''),
                    'author': post.get('author', ''),
                    'content': post.get('content', ''),
                    'timestamp': post.get('timestamp', '')
                })

        return matches

    def _matches_criteria(self, post, criteria):
        """
        Check if a post matches the given criteria
        """
        if criteria['type'] == 'user':
            return any(username.lower().strip() in post.get('author', '').lower() 
                      for username in criteria['usernames'])

        elif criteria['type'] == 'topic' or criteria['type'] == 'job':
            content = post.get('content', '').lower()  # Changed from 'post_text' to 'content'
            keywords = criteria.get('keywords', [])

            # For job searches, include default job-related keywords
            if criteria['type'] == 'job':
                keywords = list(keywords) + ['hiring', 'looking for', 'job opportunity']

            return any(keyword.lower().strip() in content 
                      for keyword in keywords)

        return False

    def _contains_keywords(self, text, keywords):
        """
        Check if text contains any of the keywords
        """
        text = text.lower()
        return any(keyword.lower().strip() in text for keyword in keywords)