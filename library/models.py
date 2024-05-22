from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=80, default='Unknown', help_text="Author's name")
    country = models.CharField(max_length=150, default='Unknown', help_text="Author's address")
    age = models.IntegerField(max_length=100, help_text="Author's age")
   
    
    def __str__(self) -> str:
        return f'Author: {self.name}'



class Book(models.Model):
    
    class Category(models.TextChoices):
        Fantasy = 'FS', 'Fantasy'
        Drama = 'DM', 'Drama'
        Thriller = 'TH', 'Thriller'
        Romance = 'RM', 'Romance',
        ScienceF = 'SF', 'Science Fiction'
        Comedy = 'CM', 'Comedy'
    
    title = models.CharField(max_length=120, help_text="Book's title", null=False)
    ISBN = models.CharField(max_length=250, help_text="Book's ISBN", null=False)
    description = models.TextField(help_text="Book's detailed description")
    category = models.CharField(max_length=2, choices=Category.choices) 
    available = models.IntegerField(help_text='Books available to take', null=False)
    pub_date = models.DateTimeField(help_text="Date when book was published", null=False)
    edited = models.DateTimeField(auto_now_add=True, help_text="Date when the book was edited")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='library_book')
    
    
    
    class Meta:
        ordering = ['pub_date' ,'title']
        
        indexes = [
            models.Index(fields=['title', 'author'])
        ]
    
    def __str__(self) -> str:
        return f'title: {self.title} description:{self.description[:30]}'
    

class Customer(models.Model):
    username = models.CharField(max_length=80, help_text="Customer's name", null=False)
    email = models.EmailField(max_length=100, null=False, help_text="Customer's email")
    membership = models.DateTimeField(null=False, help_text="Customer membeship")
    
    class Meta:
        
        indexes = [
            models.Index(fields=['username', 'email'])
        ]
        
    def __str__(self) -> str:
        return f'{self.username}'
    


class CustomerBook(models.Model):
    book = models.ForeignKey(Book, help_text="Book ID", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, help_text="Customer Id", on_delete=models.CASCADE)
    borrowed = models.DateTimeField(auto_now=True, help_text="Date time when the book was taken by the customer")
    returned = models.DateTimeField(default="not delivered", help_text="Date time when book was returned by the customer")
    
    # Create save custom handling to only record books from customer that have memebership
    def save(self, *args, **kargs):
        if self.customer.memebership.day - timezone.now().day > 30 :
            raise Exception("Only customers with membership can take books")
        
        super().save(*args, **kargs)
        
    
    class Meta:
        indexes = [
            models.Index(fields=['customer', 'borrowed'])
        ]
        
    def __str__(self) -> str:
        return f'The book {self.book} was borrowed {self.borrowed} and returned {self.returned}'
