from django.db import models
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    name = models.CharField(max_length=80, default='Unknown', help_text="Author's name")
    country = models.CharField(max_length=150, default='Unknown', help_text="Author's address")
    age = models.IntegerField(help_text="Author's age")
   
    
    def __str__(self) -> str:
        return f'{self.name}'



class Book(models.Model):
    
    class Category(models.TextChoices):
        Fantasy = 'FS', 'Fantasy'
        Drama = 'DM', 'Drama'
        Thriller = 'TH', 'Thriller'
        Romance = 'RM', 'Romance',
        ScienceF = 'SF', 'Science Fiction'
        Comedy = 'CM', 'Comedy'
    
    title = models.CharField(max_length=120, help_text="Book's title", null=False)
    ISBN = models.CharField(max_length=250, help_text="Book's ISBN", null=False, unique=True)
    description = models.TextField(help_text="Book's detailed description")
    category = models.CharField(max_length=2, choices=Category.choices) 
    available = models.IntegerField(help_text='Books available to take', null=False)
    pub_date = models.DateField(help_text="Date when book was published", null=False)
    edited = models.DateTimeField(auto_now_add=True, help_text="Date when the book was edited")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='library_book')
    
    
    
    class Meta:
        ordering = ['pub_date' ,'title']
        
        indexes = [
            models.Index(fields=['title', 'author'])
        ]
    
    def __str__(self) -> str:
        return f'title: {self.title} description:{self.description[:30]}....'
    

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
    returned = models.DateTimeField(null=True, blank=True, default=None, help_text="Date time when book was returned by the customer")
    
    # Create save custom handling to only record books from customer that have memebership
    def save(self, *args, **kargs):
        """
            There are two possible cases
            1- Object is created
            2- Object is updated
            When object is created can have returned then increase available book of intance by 1
            but if object is created but is not returned yet then decrease a vailable books
            
            When object already exists but the instance is updated for example customer but the book
            is already returned then do not decrease or increase
            but if the object already exists and is returned increase books by 1
            
        """
        
        from_date = self.customer.membership
        to_date = timezone.now()
        result = to_date - from_date
        
        exists = CustomerBook.objects.filter(id=self.id).first()
        
        if not exists or exists.book.id != self.book.id:
            if result.days > 30:
                raise Exception("Only customers with membership can take books")
            
            if not self.returned or exists.book.id != self.book.id: # since book is taken and not returned yet
               self.book.available -= 1 
        else:
            if self.returned != None and exists.returned == None \
            or self.book.id != exists.book.id and exists.returned == None: # the book is returned
                self.book.available += 1
                   
               
        super().save(*args, **kargs)
        
    
    class Meta:
        indexes = [
            models.Index(fields=['customer', 'borrowed'])
        ]
        
    def __str__(self) -> str:
        return f'The book {self.book} was borrowed {self.borrowed} to {self.customer} and returned {self.returned}'
