from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupAdminForm
from .models import User

admin.site.site_header = "ESUG Admin"
admin.site.site_title = "ESUG Voter Admin Area"
admin.site.index_title = "Welcome to the ESUG Voter Admin Area"

# Unregister the original Group admin.
admin.site.unregister(Group)


# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email',)

    fieldsets = ((None,
                  {'fields': ('email', 'username', 'password',)}),
                 ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
                 )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
                'is_active'
            )}
         ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)
