from django.contrib import admin
from  .models import Author, Book, Course, Student, Topic

# Register your models here.
admin.site.register(Author)
#admin.site.register(Book)
admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Topic)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','numpages', 'in_stock')

def upper_case_name(obj):
    courselist=Course.objects.filter(students=obj)
    courseStr=obj.first_name + ":" + obj.last_name + " => "
    for course in courselist:
        courseStr=courseStr+ course.title + " / "
    return ("%s" % (courseStr))

class StudentAdmin(admin.ModelAdmin):
    list_display = (upper_case_name,)

admin.site.register(Student,StudentAdmin)
admin.site.register(Book,BookAdmin)