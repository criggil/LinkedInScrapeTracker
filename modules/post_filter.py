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
                    'content': post.get('content', '') or post.get('post_text', ''),  # Try both field names
                    'timestamp': post.get('timestamp', '') or post.get('date_posted', '')  # Try both field names
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
            # Try both possible content field names
            content = (post.get('content', '') or post.get('post_text', '') or '').lower()
            keywords = criteria.get('keywords', [])

            # For job searches, include default job-related keywords
            if criteria['type'] == 'job':
                keywords = list(keywords) + ['hiring', 'looking for', 'job opportunity']

            # Print debug information for keywords and content
            print(f"Keywords to match: {keywords}")
            print(f"Post content: {content}")

            matches = [kw for kw in keywords if kw.lower().strip() in content]
            if matches:
                print(f"Matched keywords: {matches}")

            return bool(matches)

        return False

    def _contains_keywords(self, text, keywords):
        """
        Check if text contains any of the keywords
        """
        text = text.lower()
        return any(keyword.lower().strip() in text for keyword in keywords)