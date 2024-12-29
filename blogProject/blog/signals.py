# Signal to handle email notification when a new blog is posted
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

#from CapBlog.blogProject.blog.models import Blog, User
from .models import Blog, User
@receiver(post_save, sender=Blog)
def send_new_blog_notification(sender, instance, created, **kwargs):
    if created:
        subscribers = User.objects.filter(is_subscribed=True)
        for subscriber in subscribers:
            send_mail(
                subject=f"New Blog Post: {instance.title}",
                message=f"Check out the new blog post: {instance.title}\n\n{instance.content[:200]}...",
                from_email="noreply@yourblog.com",
                recipient_list=[subscriber.email],
            )