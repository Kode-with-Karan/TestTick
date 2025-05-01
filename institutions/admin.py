# institutions/admin.py
from django.contrib import admin
from .models import Institution, Student

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_type', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('institution_type',)

admin.site.register(Student)