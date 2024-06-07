from django.test import TestCase
from datetime import datetime
import pytz
from django.utils import timezone
# Create your tests here.
from library.models import Author, Book, Customer, CustomerBook

class TestAuthor(TestCase):
    
    def setUp(self):
        Author.objects.create(name='Zane Gray', country='United States', age=47)
        Author.objects.create(name='R.L Stine', country='England', age=60)
        Author.objects.create(name='James Morton', country='Canda', age=40)
        
        
    def test_authors_list(self):
        authors = Author.objects.all()
        
        for author in authors:
            print(author)
            
        print("Insertion database was sucessfully")

class TestBook(TestCase):
    def setUp(self):
        Author.objects.create(name='Zane Gray', country='United States', age=47)  
        Author.objects.create(name='R.L Stine', country='England', age=60)        
        Author.objects.create(name='James Morton', country='Canda', age=40)      
                                                                                       
    def test_books(self):
        authors = Author.objects.all()
        books = []
        Book.objects.create(title="Mobility: A Novel", ISBN="9781638930563",
            description=" A fictional work centered around themes of movement and change.",
            category=Book.Category.ScienceF,
            available=1,
            pub_date='2018-03-23',
            author= authors[0]
        )
        
        Book.objects.create(
            title="Quantum Horizons",
            ISBN="9781408888774",
            description="A deep dive into the mysteries of quantum mechanics and its implications for our understanding of the universe.",
            category=Book.Category.ScienceF,
            available=15,
            pub_date='2019-08-15',
            author=authors[1]
        )

        Book.objects.create(
            title="Whispers of the Forest",
            ISBN="9780399590504",
            description="An enchanting tale set in a mystical forest, exploring the bond between humans and nature.",
            category=Book.Category.Fantasy,
            available=1,
            pub_date='2020-11-01',
            author=authors[2]
        )

        Book.objects.create(
            title="The Last Algorithm",
            ISBN="9780670020553",
            description="A gripping techno-thriller about the race to develop the most advanced AI.",
            category=Book.Category.Thriller,
            available=25,
            pub_date='2021-03-03',
            author=authors[0]
        )

        Book.objects.create(
           title="Cooking with Passion",
           ISBN="9780345542125",
           description="A culinary journey through exotic flavors and cooking techniques from around the world.",
           category=Book.Category.Fantasy,
           available=30,
           pub_date='2017-06-04',
           author=authors[2]
        )
        
        for book in Book.objects.all():
            print(book)
            
            
        print("Books where inserted succesfully")


class TestCustomer(TestCase):
   
   def test_customer(self):
        Customer.objects.create(username='john_doe', email='john.doe@example.com', membership=datetime(2023, 1, 1, 10, 0))
        Customer.objects.create(username='jane_smith', email='jane.smith@example.com', membership=datetime(2023, 2, 15, 14, 30))
        Customer.objects.create(username='alice_jones', email='alice.jones@example.com', membership=datetime(2023, 3, 20, 9, 15))
        Customer.objects.create(username='bob_brown', email='bob.brown@example.com', membership=datetime(2023, 4, 25, 16, 45))
        Customer.objects.create(username='charlie_clark', email='charlie.clark@example.com', membership=datetime(2023, 5, 30, 11, 0))
        
        customers = Customer.objects.all() 
        
        for customer in customers:
            print(customer)
        
        print("Customers created sucessfully")
        

class TestCustomerBook(TestCase):
    def setUp(self):
        Customer.objects.create(username='john_doe', email='john.doe@example.com', membership=datetime(2023, 1, 1, 10, 0, tzinfo=pytz.UTC))
        Customer.objects.create(username='jane_smith', email='jane.smith@example.com', membership=datetime.now(tz=pytz.UTC))
        Author.objects.create(name='Zane Gray', country='United States', age=47)  
        Author.objects.create(name='R.L Stine', country='England', age=60)        
        Author.objects.create(name='James Morton', country='Canda', age=40)
        authors = Author.objects.all()
        Book.objects.create(
            title="Whispers of the Forest",
            ISBN="9780399590504",
            description="An enchanting tale set in a mystical forest, exploring the bond between humans and nature.",
            category=Book.Category.Fantasy,
            available=1,
            pub_date='2020-11-01',
            author=authors[2]
        )

        Book.objects.create(
            title="The Last Algorithm",
            ISBN="9780670020553",
            description="A gripping techno-thriller about the race to develop the most advanced AI.",
            category=Book.Category.Thriller,
            available=25,
            pub_date='2021-03-03',
            author=authors[0]
        )

        Book.objects.create(
           title="Cooking with Passion",
           ISBN="9780345542125",
           description="A culinary journey through exotic flavors and cooking techniques from around the world.",
           category=Book.Category.Fantasy,
           available=0,
           pub_date='2017-06-04',
           author=authors[2]
        )
        
        
    
    def test_create(self):
        book1 = Book.objects.get(id=1)
        customer = Customer.objects.get(id=2)
        CustomerBook.objects.create(book=book1,
                                    customer=customer,
                                    borrowed=timezone.now(),
                                    )
        
        borrowed_books = CustomerBook.objects.all()
        
        for book in borrowed_books:
            print(book)
            
        print("Test for borrowed books runned sucessfully")
    
    def test_outdated_memebeship(self):
        book1 = Book.objects.get(id=2)
        customer = Customer.objects.get(id=1)
        customer_book1 = CustomerBook(book=book1,
                                    customer=customer,
                                    borrowed=timezone.now(),
                                    )
        try: 
            customer_book1.save()
        except Exception as e:
            self.assertEqual(str(e), "Only customers with membership can take books") 
            print("A book without membership was registered, exception raised successfully.")

        
    def test_book_stock_limit(self):
        book1 = Book.objects.get(id=3)
        customer = Customer.objects.get(id=2)
        customer_book1 = CustomerBook(book=book1,
                                      customer=customer,
                                      borrowed=timezone.now())
        try:
            customer_book1.save()
        except Exception as e:
            self.assertEqual(str(e), "There are no more books available")
            print("Stock limit books were tried to be registered, exception raised successfully")
            
    
    def test_returned_book(self):
        """
        Test when book is returned increase available books to books list
        """
        
        book1 = Book.objects.get(id=1)
        customer = Customer.objects.get(id=2)
        book2 = Book.objects.get(id=2)
        customer_book1 = CustomerBook(book=book1,
                                      customer=customer,
                                      borrowed=timezone.now())
        
        
        self.assertEqual(book1.available, 1)
        customer_book1.save()
        self.assertEqual(book1.available, 0)
        customer_book1.save() #only update
        self.assertEqual(book1.available, 0)
        customer_book1.returned = timezone.now()
        customer_book1.save()
        self.assertEqual(book1.available, 1)
        customer_book1.returned = timezone.now() 
        customer_book1.save()
        self.assertEqual(book1.available, 1) # same 1 since was previously returned
        customer_book1.book = book2
        customer_book1.save()
        self.assertEqual(book1.available, 1) # when book updated keep the book the same if was delivered
        self.assertEqual(book2.available, 24) # decrease the new book
        
        customer_book1.book = book2
        print("the book is", customer_book1.returned)
        customer_book1.save() 
        self.assertEqual(book1.available, 1)
        self.assertEqual(book2.available, 24)
        
