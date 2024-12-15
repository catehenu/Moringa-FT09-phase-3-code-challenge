from database.connection import get_db_connection

class Author:
    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name  # This will use the setter method

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        if not (2 <= len(value) <= 50):  # Assuming a length validation
            raise ValueError("Name must be between 2 and 50 characters.")
        self._name = value



    def _retrieve_name_from_db(self):
        if self.author_id is None:
            raise ValueError("Author ID is required to retrieve the name from the database.")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM authors WHERE id = ?', (self.author_id,))

        result = cursor.fetchone()
        if result:
            self.full_name = result[0]
        else:
            raise ValueError(f"No author found with ID {self.author_id}.")

        connection.close()

    def fetch_articles(self):
        from models.article import Article

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.author_id,))
        articles_data = cursor.fetchall()
        connection.close()

        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles_data]

    def fetch_magazines(self):
        from models.magazine import Magazine

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.author_id,))

        magazines_data = cursor.fetchall()
        connection.close()

        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines_data]

    def __repr__(self):
        return f"<Author: {self.name}>"
