from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Custom User Model
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    physical_address = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # Store as a JSON object
    is_subscribed = models.BooleanField(default=False)

        # Add unique related names to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change this to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Change this to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

# Skill Model
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(help_text="Rate from 1 to 10")

    def __str__(self):
        return f"{self.name} ({self.proficiency}/10)"

# Experience Model
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title

# Blog Model
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Comment Model
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"

# Like Model
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.blog.title}"

# Contact Message Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"

# Subscription Model
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.email})"


# Signal to handle email notification when a new blog is posted
#from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail

# @receiver(post_save, sender=Blog)
# def send_new_blog_notification(sender, instance, created, **kwargs):
#     if created:
#         subscribers = User.objects.filter(is_subscribed=True)
#         for subscriber in subscribers:
#             send_mail(
#                 subject=f"New Blog Post: {instance.title}",
#                 message=f"Check out the new blog post: {instance.title}\n\n{instance.content[:200]}...",
#                 from_email="noreply@yourblog.com",
#                 recipient_list=[subscriber.email],
#             )