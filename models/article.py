from database.connection import get_db_connection

class Article:
    def __init__(self, article_id=None, title=None, content=None, author=None, magazine=None):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.author = author
        self.magazine = magazine

        if self.article_id is None and self.title is not None:
            self.create_article()
        elif self.article_id is not None:
            self.load_article_data()

    def create_article(self):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            'INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
            (self.title, self.content, self.author, self.magazine)
        )

        self.article_id = cursor.lastrowid

        connection.commit()
        connection.close()

    @property
    def article_title(self):
        if not hasattr(self, '_title') and self.article_id is not None:
            self.load_article_data()
        return self.title

    @article_title.setter
    def article_title(self, new_title):
        if self.article_id is not None:
            raise ValueError("Cannot modify title of an existing article.")
        if isinstance(new_title, str) and 5 <= len(new_title) <= 50:
            self.title = new_title
        else:
            raise ValueError("Title must be a string with 5-50 characters.")

    @property
    def article_content(self):
        if not hasattr(self, '_content') and self.article_id is not None:
            self.load_article_data()
        return self.content

    @article_content.setter
    def article_content(self, new_content):
        if self.article_id is not None:
            raise ValueError("Cannot modify content of an existing article.")
        if isinstance(new_content, str):
            self.content = new_content
        else:
            raise ValueError("Content must be a string.")

    def load_article_data(self):
        if self.article_id is None:
            raise ValueError("Cannot load data without an article ID.")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            'SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?',
            (self.article_id,)
        )
        row = cursor.fetchone()

        if row:
            self.title, self.content, self.author, self.magazine = row
        else:
            raise ValueError("No article found with the given ID.")

        connection.close()

    def __repr__(self):
        return f"<Article: {self.title}>"
