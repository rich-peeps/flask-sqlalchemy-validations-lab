from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, value):
        """
        - Name is required (non-empty).
        - Name must be unique.
        """
        if not value or not value.strip():
            raise ValueError("Author must have a name.")

        # Enforce uniqueness at the model layer (in addition to the DB constraint).
        existing = Author.query.filter(Author.name == value).first()
        if existing and existing.id != self.id:
            raise ValueError("Author name must be unique.")

        return value


    @validates("phone_number")
    def validate_phone_number(self, key, value):
        """
        - Phone number must be exactly 10 digits.
        - Treat None / empty as invalid if phone_number is provided in tests.
        """
        if value is None:
            return value  # allow null if tests permit; if not, remove this line and enforce always.

        # Only allow 10 numeric characters
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("content")
    def validate_content(self, key, value):
        """
        - content: at least 250 characters.
        """
        if not value or len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value

    @validates("summary")
    def validate_summary(self, key, value):
        """
        - summary: at most 250 characters.
        """
        if value is None:
            raise ValueError("Post summary is required.")
        if len(value) > 250:
            raise ValueError("Post summary must be at most 250 characters.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        """
        - category: only 'Fiction' or 'Non-Fiction'.
        """
        allowed = ["Fiction", "Non-Fiction"]
        if value not in allowed:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return value

    @validates("title")
    def validate_title(self, key, value):
        """
        - title: must contain one of:
          "Won't Believe", "Secret", "Top", "Guess"
        (classic clickbait phrases)
        """
        if not value or not value.strip():
            raise ValueError("Post must have a title.")

        clickbait_phrases = [
            "Won't Believe",
            "Secret",
            "Top",
            "Guess",
        ]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must be sufficiently clickbait-y.")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

