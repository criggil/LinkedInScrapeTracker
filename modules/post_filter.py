class PostFilter:
    def filter_posts(self, posts, criteria):
        """
        Filter posts based on search criteria
        """
        matches = []
        search_type = criteria['type']

        for post in posts:
            if self._matches_criteria(post, criteria):
                matches.append(post)

        return matches

    def _matches_criteria(self, post, criteria):
        """
        Check if a post matches the given criteria
        """
        if criteria['type'] == 'user':
            return post['author'].lower() in [u.lower().strip() for u in criteria['usernames']]
        
        elif criteria['type'] == 'topic' or criteria['type'] == 'job':
            content = post['content'].lower()
            return any(keyword.lower().strip() in content 
                      for keyword in criteria['keywords'])
        
        return False

    def _contains_keywords(self, text, keywords):
        """
        Check if text contains any of the keywords
        """
        text = text.lower()
        return any(keyword.lower().strip() in text for keyword in keywords)
