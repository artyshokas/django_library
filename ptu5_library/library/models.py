from django.contrib.auth import get_user_model
from django.db import models
import uuid
from django.utils.html import format_html
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField

class Genre(models.Model):
    name = models.CharField(_('name'), max_length=200, help_text=_('Enter the name of the genre'))

    def __str__(self) -> str:
        return self.name

    def link_filtered_books(self):
        link = reverse('books')+ '?genre_id='+str(self.id)
        return format_html('<a class="genre" href="{link}">{name}</a>', link=link, name=self.name)


class Author(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def display_books(self):
        return ', '.join(book.title for book in self.books.all())
    display_books.short_description = _('books')

    # linkas i autoriu teisingesnis
    def link(self) -> str:
        link = reverse('author', kwargs={'author_id': self.id})
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.__str__())

    
class Meta:
    ordering = ['last_name', 'first_name']



class Book(models.Model):
    title = models.CharField(_('title'), max_length=255)
    summary =  HTMLField(_('summary')) # max_length nereikalingas su TextField
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
        help_text=_('<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN kodas</a> consisting of 13 symbols'))
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', )
    genre = models.ManyToManyField(Genre, help_text=_('Choose genre(s) for this book'), verbose_name=_('genre(s)'))
    cover = models.ImageField(_("cover"), upload_to='covers', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"


    def display_genre(self) -> str:
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = _('genre(s)')

    # sudetingesnis budas sukurt linka i autoriu
    def author_link(self) -> str:
        link = reverse(_('author'), kwargs={'author_id': self.author.id})
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.author)



    # on_delete -- PROTECT neleis istrint autho jei turi knygu. 
    # SET_NULL knygose vietoj autor paliks null. 
    # CASCADE istrins ir knygas jei istrini autoriu
    # DO NOTHING - obviously


class BookInstance(models.Model):
    unique_id = models.UUIDField(_('unique ID'), default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name='book', on_delete=models.CASCADE)
    due_back = models.DateField(_('Due Back'), null=True, blank=True)

    LOAN_STATUS = (
        ('m', _("managed")),
        ('t', _("taken")),
        ('a', _("available")),
        ('r', _("reserved")),
    )
    # loan status didz raid yra konstanta, kuria aprasom lauko viduje. tai yra ne laukas
    status = models.CharField(_('status'), max_length=1, choices=LOAN_STATUS, default='m') # nustatom defaultini loan statusa m - managed
    # price = models.DecimalField('price', max_digits=18, decimal_places=2) #  decimal_places - kiek po kablelio
    reader = models.ForeignKey(
        get_user_model(),
        verbose_name=_("reader"), 
        on_delete=models.SET_NULL,
        null=True, blank=True, 
        related_name='taken_books', 
    )

    @property
    def is_overdue(self):
        if self.due_back and self.due_back < datetime.date(datetime.now()):
            return True
        return False

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.book.title}" # mes per sasaja per modeli book, kreipiames i title. per foreign key

    class Meta:
        ordering = ['due_back']



class BookReview(models.Model):
    book = models.ForeignKey(Book, verbose_name=_("book"), on_delete=models.CASCADE, related_name='reviews')
    reader = models.ForeignKey(get_user_model(), verbose_name=_("reader"), on_delete=models.CASCADE, related_name='book_reviews')
    created_at = models.DateField(_("created at"), auto_now_add=True)
    content = models.TextField(_("content"))

    def __str__(self):
        return f"{self.reader} on {self.book} at {self.created_at}"

    class Meta:
        ordering = ('-created_at', )