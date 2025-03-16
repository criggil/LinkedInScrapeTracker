# Database Schema Documentation

This document describes the database schema for the LinkedIn Scrape Tracker application.

## Overview

The application uses SQLAlchemy ORM to interact with a relational database. The schema consists of three main tables:

1. **Posts** - Stores LinkedIn posts with user information
2. **Searches** - Stores search configurations for monitoring LinkedIn content
3. **Matches** - Stores matches between searches and posts

## Tables

### Posts Table

| Column      | Type         | Constraints                    | Description                                   |
|-------------|--------------|-------------------------------|-----------------------------------------------|
| id          | Integer      | Primary Key                   | Unique identifier for each post               |
| post_url    | String(2048) | Unique, Not Null             | URL of the LinkedIn post                      |
| user_name   | String(255)  | Nullable                      | Name of the user who created the post         |
| user_url    | String(2048) | Nullable                      | URL of the user's LinkedIn profile            |
| content     | Text         | Not Null                      | Text content of the post                      |
| timestamp   | DateTime     | Not Null                      | Date and time when the post was created       |
| likes       | Integer      | Default: 0                    | Number of likes received by the post          |
| comments    | Integer      | Default: 0                    | Number of comments on the post                |
| shares      | Integer      | Default: 0                    | Number of times the post has been shared      |

### Searches Table

| Column      | Type         | Constraints       | Description                                   |
|-------------|--------------|-------------------|-----------------------------------------------|
| id          | Integer      | Primary Key       | Unique identifier for each search             |
| name        | String(255)  | Not Null          | Name of the search                            |
| type        | String(50)   | Not Null          | Type of search (user, company, topic, or job) |
| usernames   | Text         | Nullable          | Usernames to search for (for user searches)   |
| keywords    | Text         | Nullable          | Keywords to search for (for topic/job searches)|
| notify      | Boolean      | Default: False    | Whether to send notifications for matches     |

### Matches Table

| Column      | Type      | Constraints                        | Description                                   |
|-------------|-----------|-----------------------------------|-----------------------------------------------|
| id          | Integer   | Primary Key                       | Unique identifier for each match              |
| search_id   | Integer   | Foreign Key (searches.id), Not Null | Reference to the search that matched         |
| post_id     | Integer   | Foreign Key (posts.id), Not Null  | Reference to the post that matched            |
| matched_at  | DateTime  | Not Null                          | Date and time when the match occurred         |

## Relationships

- A **Post** can have multiple **Matches** (one-to-many relationship)
- A **Search** can have multiple **Matches** (one-to-many relationship)
- A **Match** belongs to one **Search** and one **Post**

## Usage Example

```python
from database.database import setup_database
from database.Models import Post, Search, Match
from datetime import datetime

# Set up the database
engine, Session = setup_database()
session = Session()

# Create a post
post = Post(
    post_url="https://www.linkedin.com/posts/johndoe_product-launch-activity-123456789",
    user_name="John Doe",
    user_url="https://www.linkedin.com/in/johndoe/",
    content="Excited to announce our new product launch!",
    timestamp=datetime.now(),
    likes=100,
    comments=25,
    shares=10
)

session.add(post)
session.commit()

# Create a search for a specific user
user_search = Search(
    name="John Doe's Posts",
    type="user",
    usernames="John Doe",
    notify=True
)

# Create a search for a specific topic
topic_search = Search(
    name="Product Launch",
    type="topic",
    keywords="product launch, new product",
    notify=True
)

session.add_all([user_search, topic_search])
session.commit()

# Create matches
user_match = Match(
    search_id=user_search.id,
    post_id=post.id,
    matched_at=datetime.now()
)

topic_match = Match(
    search_id=topic_search.id,
    post_id=post.id,
    matched_at=datetime.now()
)

session.add_all([user_match, topic_match])
session.commit()

# Query posts by a specific user name
user_posts = session.query(Post).filter(Post.user_name == "John Doe").all()

# Query matches for a specific search
search_matches = session.query(Match).filter(Match.search_id == user_search.id).all()

# Get all posts that match a specific search
matched_posts = session.query(Post).join(Match).filter(Match.search_id == topic_search.id).all()
```

## Database Setup

The database is set up using the `setup_database()` function in `database/database.py`. By default, it uses SQLite with a file named `linkedin_data.db` in the current directory, but this can be customized by passing a different connection string.
