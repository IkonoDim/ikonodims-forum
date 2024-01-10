"""
This module defines a class DatabaseConnection that extends sqlite3.Connection.
This class includes various methods for interacting with a SQLite database, including creating tables,
checking identifier availability, validating login information, creating sessions, posts, comments,
and handling user interactions such as liking and disliking posts.
"""

import copy
import secrets
import sqlite3
import time
import exceptions.database
import exceptions.universal
import models.database
import utils.keygen


class DatabaseConnection(sqlite3.Connection):
    def __init__(self, database: str):

        # Calling of the sqlite initializer, check same thread is set to false, so the db can be used in other
        # processes, not only in the first that opens / creates it.
        super().__init__(database, check_same_thread=False)
        self.__base_struct()

    def __base_struct(self):
        # The base structure of the database

        cursor = self.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                    uniqueUserIdentifier INTEGER UNIQUE PRIMARY KEY NOT NULL,
                    uniqueUsername TEXT UNIQUE NOT NULL,
                    userPassword TEXT NOT NULL,
                    userLikedPosts TEXT NOT NULL DEFAULT 0,
                    userDislikedPosts TEXT NOT NULL DEFAULT 0,
                    userViewedPosts TEXT NOT NULL DEFAULT 0
                )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS sessions (
                    uniqueSessionIdentifier TEXT UNIQUE PRIMARY KEY NOT NULL,
                    sessionUserUniqueIdentifier INTEGER NOT NULL,
                    sessionExpirationDate INTEGER NOT NULL,
                    sessionCreationDate INTEGER NOT NULL
                )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
                uniquePostIdentifier INTEGER UNIQUE NOT NULL,
                postUserIdentifier TEXT NOT NULL,
                postTitle TEXT NOT NULL,
                postContent TEXT NOT NULL,
                postCreationDate INTEGER NOT NULL,
                postLikes INTEGER NOT NULL DEFAULT 0,
                postDislikes INTEGER NOT NULL DEFAULT 0,
                postViews INTEGER NOT NULL DEFAULT 0
                )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS comments (
                uniqueCommentIdentifier INTEGER UNIQUE NOT NULL,
                commentPostIdentifier INTEGER NOT NULL,
                commentUserIdentifier TEXT NOT NULL,
                commentContent TEXT NOT NULL,
                commentCreationDate INTEGER NOT NULL
                )""")

    def check_if_user_identifier_is_available(self, identifier: int) -> bool:
        cursor = self.cursor()

        cursor.execute("SELECT uniqueUserIdentifier FROM user")
        fetched_values = [i[0] for i in cursor.fetchall()]
        # the for-loop is needed because the values are displayed in this format: [(a,), (b,), (c,)]

        return False if int(identifier) in fetched_values else True

    def check_if_post_identifier_is_available(self, identifier: int) -> bool:
        cursor = self.cursor()

        cursor.execute("SELECT uniquePostIdentifier FROM posts")
        fetched_values = [i[0] for i in cursor.fetchall()]

        return False if int(identifier) in fetched_values else True

    def check_if_comment_identifier_is_available(self, identifier: int) -> bool:
        cursor = self.cursor()

        cursor.execute("SELECT uniqueCommentIdentifier FROM comments")
        fetched_values = [i[0] for i in cursor.fetchall()]

        return False if int(identifier) in fetched_values else True

    def check_if_session_identifier_is_available(self, identifier: str) -> bool:
        cursor = self.cursor()

        cursor.execute("SELECT uniqueSessionIdentifier FROM sessions")
        fetched_values = [i[0] for i in cursor.fetchall()]

        return False if identifier in fetched_values else True

    def check_if_username_is_available(self, username: str) -> bool:
        cursor = self.cursor()

        cursor.execute("SELECT uniqueUsername FROM user")
        fetched_values = [i[0] for i in cursor.fetchall()]
        return False if username in fetched_values else True

    def validate_login_information(self, user: models.database.User) -> bool:
        if not user.username or not user.user_password:
            raise exceptions.universal.InvalidArgumentsException("'username', 'password' have to be specified.")

        cursor = self.cursor()

        cursor.execute("""SELECT uniqueUserIdentifier FROM user WHERE (uniqueUsername, userPassword) = (?, ?)""",
                       (str(user.username), str(user.user_password)))
        fetched_values = cursor.fetchall()

        if len(fetched_values) == 0:
            raise exceptions.database.InvalidLoginDetails("specified login details are invalid!")

        return True

    def get_user_identifier(self, user: models.database.User) -> int:
        if not user.username:
            raise exceptions.universal.InvalidArgumentsException("'username' has to be specified.")

        cursor = self.cursor()

        cursor.execute("""SELECT uniqueUserIdentifier FROM user WHERE uniqueUsername = ?""",
                       (str(user.username),))
        fetched_values = cursor.fetchone()

        return fetched_values[0]

    def get_user(self, user: models.database.User) -> models.database.User:
        new_user = copy.deepcopy(user)
        if not new_user.user_identifier:
            raise exceptions.universal.InvalidArgumentsException("'user_identifier' has to be specified!")
        cursor = self.cursor()
        cursor.execute("""SELECT * FROM user WHERE uniqueUserIdentifier = ?""", (str(new_user.user_identifier),))
        fetched_values = cursor.fetchone()

        new_user = models.database.User(new_user.user_identifier, fetched_values[1])

        new_user.liked_posts = fetched_values[3].split(",")
        new_user.disliked_posts = fetched_values[4].split(",")
        new_user.viewed_posts = fetched_values[5].split(",")

        return new_user

    def create_user(self, user: models.database.User):
        if not user.username or not user.user_password or user.user_identifier:
            raise exceptions.universal.InvalidArgumentsException("'username', 'password' have to be specified. "
                                                                 "'user_identifier' has to be None.")

        if not self.check_if_username_is_available(user.username):
            raise exceptions.database.UsernameNotAvailableException(f"username '{user.username}' is not available!")

        # For the uniqueUserIdentifier, a 32-bit number is generated.
        # ! This number DOES NOT NECESSARILY HAVE TO BE 10 digits "long" since zero-padding is also generated
        while True:
            user.user_identifier = secrets.randbits(32)

            if self.check_if_user_identifier_is_available(user.user_identifier):
                break

        cursor = self.cursor()
        cursor.execute("""INSERT INTO user (uniqueUserIdentifier, uniqueUsername, userPassword) 
                        VALUES (?, ?, ?)""", (int(user.user_identifier), str(user.username), str(user.user_password)))
        self.commit()

    def get_session(self, session: models.database.Session) -> models.database.Session:
        if not session.session_identifier:
            raise exceptions.universal.InvalidArgumentsException("'session_identifier' has to be specified.")

        cursor = self.cursor()
        cursor.execute("""SELECT * FROM sessions WHERE uniqueSessionIdentifier = ?""",
                       (session.session_identifier.__str__(),))
        fetched_data = cursor.fetchone()

        if not fetched_data:
            raise exceptions.database.InvalidSessionIdentifier("the specified session_identifier is invalid.")

        if int(time.time()) > fetched_data[2]:
            raise exceptions.database.InvalidSessionIdentifier("the specified session_identifier is invalid.")

        cursor.execute("""SELECT uniqueUsername FROM user WHERE uniqueUserIdentifier = ?""", (fetched_data[1],))
        fetched_username = cursor.fetchone()

        session_user = models.database.User(fetched_data[1], fetched_username[0])
        return models.database.Session(session.session_identifier, session_user, fetched_data[2], fetched_data[3])

    def create_session(self, user: models.database.User) -> models.database.Session:
        if not user.user_identifier:
            raise exceptions.universal.InvalidArgumentsException("'user_identifier' has to be specified.")

        cursor = self.cursor()
        while True:
            session_identifier = user.user_identifier.__str__() + "." + utils.keygen.generate_session_key()

            if self.check_if_session_identifier_is_available(session_identifier):
                break

        session = models.database.Session(
            session_identifier=session_identifier,
            session_user=user,
            session_creation=int(time.time()),
            session_expiration=int(time.time()) + 48 * 60 * 60
        )

        cursor.execute("""INSERT INTO sessions (uniqueSessionIdentifier, sessionUserUniqueIdentifier, 
        sessionExpirationDate, sessionCreationDate) VALUES (?, ?, ?, ?)""", (
            session.session_identifier.__str__(), session.session_user.user_identifier.__str__(),
            session.session_expiration.__int__(), session.session_creation.__int__()
        ))
        self.commit()

        return session

    def create_post(self, post: models.database.Post):
        while True:
            post.post_id = secrets.randbits(32)
            if self.check_if_post_identifier_is_available(post.post_id):
                break

        cursor = self.cursor()
        cursor.execute("""INSERT INTO posts (
        uniquePostIdentifier, postUserIdentifier, postTitle, postContent, postCreationDate) VALUES (?, ?, ?, ?, ?)""",
                       (post.post_id, str(post.user.user_identifier), post.title,
                        post.content, int(time.time())))
        self.commit()
        return post.post_id

    def create_comment(self, comment: models.database.Comment):
        if not comment.content or not comment.post.post_id or not comment.user.user_identifier:
            raise exceptions.universal.InvalidArgumentsException("some or one argument(s) are missing.")

        while True:
            comment.comment_identifier = secrets.randbits(32)
            if self.check_if_post_identifier_is_available(comment.comment_identifier):
                break

        cursor = self.cursor()

        cursor.execute("INSERT INTO comments (uniqueCommentIdentifier, commentPostIdentifier, "
                       "commentUserIdentifier, commentContent, commentCreationDate) VALUES (?, ?, ?, ?, ?)",
                       (comment.comment_identifier, comment.post.post_id, str(comment.user.user_identifier),
                        comment.content, int(time.time())))
        self.commit()

    def view_post(self, post: models.database.Post, user: models.database.User):
        if not user.user_identifier:
            raise exceptions.universal.InvalidArgumentsException("'user_identifier' has to be specified")
        cursor = self.cursor()
        cursor.execute("""UPDATE user SET userViewedPosts = user.userViewedPosts || ? WHERE uniqueUserIdentifier = ?""",
                       ("," + str(post.post_id), int(user.user_identifier)))
        cursor.execute("""UPDATE posts SET postViews = postViews + 1 WHERE uniquePostIdentifier = ?""",
                       (post.post_id,))

    def like_post(self, post: models.database.Post, user: models.database.User):
        cursor = self.cursor()
        cursor.execute("""UPDATE user SET userLikedPosts = userLikedPosts || ? WHERE uniqueUserIdentifier = ?""",
                       ("," + str(post.post_id), int(user.user_identifier)))
        cursor.execute("""UPDATE posts SET postLikes = postLikes + 1 WHERE uniquePostIdentifier = ?""",
                       (post.post_id,))
        self.commit()

    def remove_like_post(self, post: models.database.Post, user: models.database.User):
        cursor = self.cursor()
        cursor.execute(
            """UPDATE user SET userLikedPosts = REPLACE(userLikedPosts, ?, '') WHERE uniqueUserIdentifier = ?""",
            ("," + str(post.post_id), int(user.user_identifier)))
        cursor.execute("""UPDATE posts SET postLikes = postLikes - 1 WHERE uniquePostIdentifier = ?""",
                       (post.post_id,))
        self.commit()

    def dislike_post(self, post: models.database.Post, user: models.database.User):
        cursor = self.cursor()
        cursor.execute(
            """UPDATE user SET userDislikedPosts = user.userDislikedPosts || ? WHERE uniqueUserIdentifier = ?""",
            ("," + str(post.post_id), int(user.user_identifier)))
        cursor.execute("""UPDATE posts SET postDislikes = postDislikes + 1 WHERE uniquePostIdentifier = ?""",
                       (post.post_id,))
        self.commit()

    def remove_dislike_post(self, post: models.database.Post, user: models.database.User):
        cursor = self.cursor()
        cursor.execute(
            """UPDATE user SET userDislikedPosts = REPLACE(userDislikedPosts, ?, '') WHERE uniqueUserIdentifier = ?""",
            ("," + str(post.post_id), int(user.user_identifier)))
        cursor.execute("""UPDATE posts SET postDislikes = postDislikes - 1 WHERE uniquePostIdentifier = ?""",
                       (post.post_id,))
        self.commit()

    def get_post(self, post_id: int):
        cursor = self.cursor()
        cursor.execute("""SELECT * FROM posts WHERE uniquePostIdentifier = ?""", (post_id,))
        fetched_data = cursor.fetchone()

        if fetched_data is None:
            raise exceptions.database.InvalidPostException("Invalid post id")
        user = self.get_user(models.database.User(user_identifier=fetched_data[1]))
        post = models.database.Post(post_id, fetched_data[2], fetched_data[3], fetched_data[5], fetched_data[6],
                                    fetched_data[4], fetched_data[7], self.get_user(user))

        cursor.execute("""SELECT * FROM comments WHERE commentPostIdentifier = ?""", (post.post_id,))
        fetched_data = cursor.fetchall()
        for comment in fetched_data:
            post.comments.append(models.database.Comment(comment[0], post, comment[3], comment[4],
                                                         self.get_user(models.database.User(comment[2]))))
        return post

    def grab_posts(self, amount: int, offset: int):
        cursor = self.cursor()

        cursor.execute("""SELECT uniquePostIdentifier FROM posts ORDER BY postCreationDate DESC LIMIT ? OFFSET ?""",
                       (amount, offset))
        fetched_data = cursor.fetchall()
        posts = []
        for post in fetched_data:
            posts.append(self.get_post(post[0]))

        return posts
