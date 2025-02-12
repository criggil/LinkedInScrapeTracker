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
                    'author': post.get('title', ''),  # Using 'title' as author name
                    'content': post.get('post_text', ''),  # Using 'post_text' as content
                    'timestamp': post.get('date_posted', '')
                })

        return matches

    def _matches_criteria(self, post, criteria):
        """
        Check if a post matches the given criteria
        """
        if criteria['type'] == 'user':
            return any(username.lower().strip() in post.get('title', '').lower() 
                      for username in criteria['usernames'])

        elif criteria['type'] == 'topic' or criteria['type'] == 'job':
            content = post.get('post_text', '').lower()
            return any(keyword.lower().strip() in content 
                      for keyword in criteria['keywords'])

        return False

    def _contains_keywords(self, text, keywords):
        """
        Check if text contains any of the keywords
        """
        text = text.lower()
        return any(keyword.lower().strip() in text for keyword in keywords)