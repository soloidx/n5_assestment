from django.contrib import admin

from transit_tickets.models import Officer, Driver, Vehicle, OfficerToken

# Register your models here.


admin.site.register(Officer)
admin.site.register(Driver)
admin.site.register(Vehicle)


class OfficerTokenAdmin(admin.ModelAdmin):
    readonly_fields = ('token', 'expiration_date')
    raw_id_fields = ('officer', )


admin.site.register(OfficerToken, OfficerTokenAdmin)
