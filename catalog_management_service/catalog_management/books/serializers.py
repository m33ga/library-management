from rest_framework import serializers
from .models import Book, Author, Institution, Genre, BookCopy

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].title()
        
        existing_book = Book.objects.filter(
            title=validated_data['title'],
            release_year=validated_data['release_year'],
            institution=validated_data['institution']
        ).first()
        
        if existing_book:

            existing_book.total_books += 1
            existing_book.available_books += 1
            existing_book.save()
            BookCopy.objects.create(book=existing_book, status='available')
            return existing_book
        else:
            book = super().create(validated_data) 
            BookCopy.objects.create(book=book, status='available') 
            return book

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].upper()
        
        if Institution.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Institution with this name already exists.")
        
        return super().create(validated_data)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].upper()
        
        if Genre.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Genre with this name already exists.")
        
        return super().create(validated_data)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].title()
        
        if Author.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Author with this name already exists.")
        
        return super().create(validated_data)

class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'
    

