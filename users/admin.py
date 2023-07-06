from django.contrib import admin
from .models import User, Profile

# profile admin display all the fields


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'short_intro',
                    'get_display_credits', 'profile_image')
    readonly_fields = ('user', 'get_display_credits', 'profile_image')
    # change the name of the get_display_credits to credits


admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
