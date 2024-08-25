from django.contrib import admin
from .models import Production, Activity, Comment, Input, Harvesting, Marketing, Processing

admin.site.register(Production)
admin.site.register(Activity)
admin.site.register(Comment)
admin.site.register(Input)
admin.site.register(Harvesting)
admin.site.register(Marketing)
admin.site.register(Processing)

