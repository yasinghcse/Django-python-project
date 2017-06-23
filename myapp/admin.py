from django.contrib import admin
from  .models import Author, Book, Course, Student, Topic

# Register your models here.
admin.site.register(Author)
#admin.site.register(Book)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Topic)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','numpages', 'in_stock')

admin.site.register(Book,BookAdmin)