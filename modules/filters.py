import datetime

from database.Models import Post, Search
from modules.storage import DatabaseStorage

class Processor:
    def __init__(self, storage: DatabaseStorage):
        self.storage = storage

    def filter_by_search(self, posts: list[Post], search: Search):
        matched_posts = list(filter(lambda post: self._match(post, search), posts))
        matches = list(map(lambda post: {
            "search_id": search.id,
            "post_id": post.id,
            "matched_at":datetime.datetime.now()
        }, matched_posts))
        self.storage.save_matches(search.id, matches, True)

    def _match(self, post: Post, search: Search) -> bool:
        content = post.content.lower()
        if search.type == "user" and search.usernames:
            user_names = search.usernames.split(',')
            post_username = post.user_name if post.user_name else ""
            return any(username.lower().strip() in post_username.lower() for username in user_names)

        elif search.type == "topic" or search.type == "job" and search.keywords:
            keywords = search.keywords.split(',')
            matched_keywords = [kw for kw in keywords if kw.lower().strip() in content]
            if matched_keywords:
                print(f"Matched keywords: {matched_keywords}")
                return True

        return False
