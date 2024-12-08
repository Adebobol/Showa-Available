from django.contrib import admin
from .models import Restaurant, Dish, OpeningHour


from django.contrib import admin
from .models import Restaurant, OpeningHour


class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 1  # Number of blank entries to show in admin


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [OpeningHourInline]
    # Display restaurant name and owner in the admin list view
    list_display = ('name', 'owner')
    # Enable search by name and owner's username
    search_fields = ('name', 'owner__username')


class OpeningHourAdmin(admin.ModelAdmin):
    pass
    # Display these fields in the list view
    list_display = ('restaurant', 'day', 'open_time', 'close_time')
    list_filter = ('day', 'restaurant')
    # Add filters for days and restaurants


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)


# Register your models here.
# admin.site.register(Restaurant)
admin.site.register(Dish)
# admin.site.register(OpeningHour)
