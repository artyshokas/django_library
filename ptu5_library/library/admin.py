from django.contrib import admin
from . import models



class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0
    readonly_fields = ('unique_id', )
    can_delete = False
# pagal default 0 eiluciu bookinstance - extra 0

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = (BookInstanceInline, )


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back', 'reader', )
    list_filter = ('status', 'due_back', )
    readonly_fields = ('unique_id', 'is_overdue' )
    search_fields = ('unique_id', 'book__title', 'book__author__last_name__exact', 'reader__last_name', ) # foreign key iseskomas per lookup __ vietoj tasko
    list_editable = ('status', 'due_back', 'reader', )

    fieldsets = (
        ('General', {'fields': ('unique_id', 'book')}),
        # ('Availability', {'fields': ('status', 'due_back')}),
        ('Availability', {'fields': (('status', 'due_back', 'is_overdue'), 'reader')})
        # kad status ir dueback butu horizontalioj eilutej pridedam
        # skliaustus ir kableli po ju nes tupple
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    list_display_links = ('last_name', )


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'created_at', )

admin.site.register(models.BookReview, BookReviewAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookInstance, BookInstanceAdmin)
