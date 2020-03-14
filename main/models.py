from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True, default=None)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    # why doesn't this work without setting default?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lecture, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=128)
    question = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reply = models.CharField(max_length=512)
    user = models.ForeignKey(Tutor, on_delete=models.CASCADE, default=None)

    def __str__(self):
        # identify by primary key
        return "Reply: " + str(self.pk)


class Forum(models.Model):
    # why doesn't this work without setting default?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=128)
    post = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=512)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        # identify by primary key
        return "Reply: " + str(self.pk)


class Upvote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Upvote: " + str(self.pk)


class Enrollment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "Enrollment: " + str(self.pk)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=512)
    picture = models.ImageField(upload_to='images/', default="images/29511773_1650373861750562_982140361914727316_n.jpg")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()