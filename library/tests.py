from django.test import TestCase

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
            available=20,
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
            available=10,
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


class Customer(TestCase):
   pass 