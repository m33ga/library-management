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
    title = models.CharField(max_length=255)
    release_year = models.PositiveIntegerField()
    total_books = models.PositiveIntegerField(default=0)
    available_books = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

# Tabela intermediária BookAuthor (relacionamento muitos-para-muitos entre livros e autores)
class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="authors")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    class Meta:
        unique_together = ("book", "author")

    def __str__(self):
        return f"{self.book.title} - {self.author.name}"

# Tabela BookStatus (status de cópias de livros)
class BookStatus(models.Model):
    status = models.CharField(max_length=255)  # Ex: Disponível, Emprestado, Reservado

    def __str__(self):
        return self.status

# Tabela BookCopy (cópias físicas dos livros)
class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    status = models.ForeignKey(BookStatus, on_delete=models.SET_NULL, null=True, related_name="copies")

    def __str__(self):
        return f"Cópia de '{self.book.title}' - Status: {self.status}"
