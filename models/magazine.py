# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        if name:
            self.name = name  # Use the setter to validate and set name
        if category:
            self.category = category  # Use the setter to validate and set category

    # Property for the id attribute
    @property
    def id(self):
        return self._id

    # Property and setter for the name attribute
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")
        self._name = value

    # Property and setter for the category attribute
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be a string.")
        if len(value.strip()) == 0:
            raise ValueError("Category cannot be empty.")
        self._category = value

        # Update the category in the database if id is set
        if self._id:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self._id))
            conn.commit()
            conn.close()

    # Method to fetch articles associated with the magazine
    def articles(self):
        from models.article import Article  # Import Article inside the method to avoid circular imports
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [
            Article(article['id'], article['title'], article['content'], 
                    article['author_id'], article['magazine_id']) for article in articles
        ]

    # Method to fetch contributors (authors) for the magazine
    def contributors(self):
        from models.author import Author  # Import Author inside the method to avoid circular imports
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]

    # Method to fetch titles of articles associated with the magazine
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles

    # Method to fetch authors who contributed more than two articles to the magazine
    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) AS article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]

    # String representation of Magazine instances
    def __repr__(self):
        return f'<Magazine {self.name}>'
