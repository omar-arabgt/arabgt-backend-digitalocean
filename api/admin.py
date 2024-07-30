from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(FavoritePresenter)
admin.site.register(FavoriteShow)
admin.site.register(Post)
admin.site.register(SavedPost)
admin.site.register(DeletedUser)
