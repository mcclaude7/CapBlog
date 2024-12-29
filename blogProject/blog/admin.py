from django.contrib import admin
from .models import User, Skill, Experience, Blog, Comment, Like, ContactMessage, Subscription

admin.site.register(User), 
admin.site.register(Skill),
admin.site.register(Experience),
admin.site.register(Blog),
admin.site.register(Comment),
admin.site.register(Like),
admin.site.register(ContactMessage),
admin.site.register(Subscription),
# Register your models here.
