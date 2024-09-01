from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Category, User, Lot
from .resource import CategoryResource, UserResource, LotResource

class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


class LotAdmin(ImportExportModelAdmin):
    resource_class = LotResource


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Lot, LotAdmin)
