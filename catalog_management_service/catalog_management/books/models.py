from django.db import models

# Tabela Institution (relação com livros)
class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Tabela Genre (gênero dos livros)
class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Tabela Author (autores)
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Tabela Book (livros)
class Book(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="books")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="books")
    title = models.CharField(max_length=255)
    release_year = models.PositiveIntegerField()
    total_books = models.PositiveIntegerField(default=1)
    available_books = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class ReservationStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    RESERVED = 'reserved', 'Reserved'

# Tabela BookCopy (cópias físicas dos livros)
class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    status = models.CharField(
        max_length=10,
        choices=ReservationStatus.choices,
        default=ReservationStatus.AVAILABLE,
    )

    def __str__(self):
        return f"Cópia de '{self.book.title}' - Status: {self.status}"