# Database Schema Documentation

This document describes the database schema for the LinkedIn Scrape Tracker application.

## Overview

The application uses SQLAlchemy ORM to interact with a relational database. The schema consists of five main tables:

1. **Users** - Stores information about LinkedIn users
2. **Companies** - Stores information about LinkedIn companies
3. **Posts** - Stores LinkedIn posts with relationships to users and companies
4. **Searches** - Stores search configurations for monitoring LinkedIn content
5. **Matches** - Stores matches between searches and posts

## Tables

### Users Table

| Column           | Type         | Constraints                | Description                                |
|------------------|--------------|----------------------------|--------------------------------------------|
| id               | Integer      | Primary Key                | Unique identifier for each user            |
| linkedin_id      | Integer      | Unique, Not Null          | LinkedIn's unique identifier for the user  |
| username         | String(255)  | Unique, Not Null          | Unique username for the user               |
| first_name       | String(255)  | Not Null                  | First name of the user                     |
| last_name        | String(255)  | Not Null                  | Last name of the user                      |
| email            | String(255)  | Unique, Not Null          | Email address of the user                  |
| profile_picture  | String(1024) |                           | URL of the user's profile picture          |
| headline         | String(1024) |                           | User's current job title or summary        |
| location         | String(255)  |                           | User's current location                    |
| industry         | String(255)  |                           | User's industry                            |
| connection_count | Integer      | Default: 0                | Number of connections the user has         |

### Companies Table

| Column        | Type         | Constraints       | Description                           |
|---------------|--------------|-------------------|---------------------------------------|
| id            | Integer      | Primary Key       | Unique identifier for each company    |
| linkedin_id   | Integer      | Unique, Not Null  | LinkedIn's unique identifier for the company |
| company_name  | String(255)  | Not Null          | Name of the company                   |
| industry      | String(255)  |                   | Industry of the company               |
| location      | String(255)  |                   | Location of the company               |
| description   | Text         |                   | Description of the company            |
| website       | String(1024) |                   | Website URL of the company            |

### Posts Table

| Column      | Type      | Constraints                    | Description                                   |
|-------------|-----------|-------------------------------|-----------------------------------------------|
| id          | Integer   | Primary Key                   | Unique identifier for each post               |
| user_id     | Integer   | Foreign Key (users.id), Not Null | Reference to the user who created the post   |
| company_id  | Integer   | Foreign Key (companies.id)    | Reference to the company associated with the post |
| content     | Text      | Not Null                      | Text content of the post                      |
| timestamp   | DateTime  | Not Null                      | Date and time when the post was created       |
| likes       | Integer   | Default: 0                    | Number of likes received by the post          |
| comments    | Integer   | Default: 0                    | Number of comments on the post                |
| shares      | Integer   | Default: 0                    | Number of times the post has been shared      |

### Searches Table

| Column      | Type         | Constraints   | Description                                   |
|-------------|--------------|---------------|-----------------------------------------------|
| id          | Integer      | Primary Key   | Unique identifier for each search             |
| name        | String(255)  | Not Null      | Name of the search                            |
| type        | String(50)   | Not Null      | Type of search (user, company, topic, or job) |
| keyword     | Text         |               | Keywords or usernames to search for           |
| notify      | Boolean      | Default: False| Whether to send notifications for matches     |

### Matches Table

| Column      | Type      | Constraints                        | Description                                   |
|-------------|-----------|-----------------------------------|-----------------------------------------------|
| id          | Integer   | Primary Key                       | Unique identifier for each match              |
| search_id   | Integer   | Foreign Key (searches.id), Not Null | Reference to the search that matched         |
| post_id     | Integer   | Foreign Key (posts.id), Not Null | Reference to the post that matched           |
| matched_at  | DateTime  | Not Null                          | Date and time when the match occurred         |

## Relationships

- A **User** can have multiple **Posts** (one-to-many relationship)
- A **Company** can have multiple **Posts** (one-to-many relationship)
- A **Post** belongs to one **User** and optionally to one **Company**
- A **Search** can have multiple **Matches** (one-to-many relationship)
- A **Post** can have multiple **Matches** (one-to-many relationship)
- A **Match** belongs to one **Search** and one **Post**

## Usage Example

```python
from database.database import setup_database
from database.User import User
from database.Models import Company
from database.Post import PostModel
from database.Search import Search
from database.Match import Match
from datetime import datetime

# Set up the database
engine, Session = setup_database()
session = Session()

# Create a user
user = User(
    linkedin_id=12345,
    username="johndoe",
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    profile_picture="https://example.com/profiles/johndoe.jpg",
    headline="Software Engineer",
    location="San Francisco, CA",
    industry="Technology",
    connection_count=500
)

# Create a company
company = Company(
    linkedin_id=67890,
    company_name="Tech Company",
    industry="Technology",
    location="San Francisco, CA",
    description="A leading technology company",
    website="https://techcompany.example.com"
)

# Add to session and commit
session.add_all([user, company])
session.commit()

# Create a post
post = PostModel(
    user_id=user.id,
    company_id=company.id,
    content="Excited to announce our new product launch!",
    timestamp=datetime.now(),
    likes=100,
    comments=25,
    shares=10
)

session.add(post)
session.commit()

# Create a search
search = Search(
    name="Product Launch",
    type="topic",
    keywords="product launch",
    notify=True
)

session.add(search)
session.commit()

# Create a match
match = Match(
    search_id=search.id,
    post_id=post.id,
    matched_at=datetime.now()
)

session.add(match)
session.commit()

# Query posts by a specific user
user_posts = session.query(PostModel).filter(PostModel.user_id == user.id).all()

# Query matches for a specific search
search_matches = session.query(Match).filter(Match.search_id == search.id).all()
```

## Database Setup

The database is set up using the `setup_database()` function in `database/database.py`. By default, it uses SQLite with a file named `linkedin_data.db` in the current directory, but this can be customized by passing a different connection string.
