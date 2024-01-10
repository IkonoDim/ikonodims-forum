import re
import exceptions.database


class User:
    def __init__(self, user_identifier: int = None, username: str = None,
                 user_password: str = None):
        self.user_identifier = user_identifier
        self.liked_posts = []
        self.disliked_posts = []
        self.viewed_posts = []

        self.username = username
        if not re.match("^[a-z_]+$", username.__str__()) and username:
            raise exceptions.database.UsernameNotAvailableException("some characters in the specified username are "
                                                                    "not allowed.")
        self.user_password = user_password


class Session:
    def __init__(self, session_identifier: str = None, session_user: User = None,
                 session_expiration: int = None, session_creation: int = None):
        self.session_identifier = session_identifier
        self.session_user = session_user
        self.session_expiration = session_expiration
        self.session_creation = session_creation


class Post:
    def __init__(self, post_id: int = None, title: str = None, content: str = None, likes: int = None,
                 dislikes: int = None, timestamp: int = None, views: int = None, user: User = None):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.likes = likes
        self.dislikes = dislikes
        self.timestamp = timestamp
        self.views = views
        self.user = user
        self.comments: list[Comment] = []


class Comment:
    def __init__(self, comment_identifier: int = None, post: Post = None, content: str = None, timestamp: int = None, user: User = None):
        self.comment_identifier = comment_identifier
        self.post = post
        self.content = content
        self.timestamp = timestamp
        self.user = user
