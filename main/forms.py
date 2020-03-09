from django import forms
from main.models import Course, Lecture, Question, Reply, Comment, Tutor, Student
from django.contrib.auth.models import User


# Creates a User creation form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# Creates a from for a course tuple to add to database
class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor


# Creates a from for a course tuple to add to database
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student


# Creates a from for a course tuple to add to database
class CourseForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the course name")

    class Meta:
        model = Course
        fields = 'name'


# Creates a form for a Lecture tuple to add to database
class LectureFrom(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter lecture name")

    class Meta:
        model = Lecture
        exclude = 'course'


# Creates a form for a Lecture tuple to add to database
class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    question = forms.CharField(max_length=512)
    upvotes = forms.IntegerField(default=0)

    class Meta:
        model = Question
        exclude = 'lecture'


# Creates a form for a Lecture tuple to add to database
class ReplyForm(forms.ModelForm):
    reply = forms.CharField(max_length=512)

    class Meta:
        model = Reply
        exclude = 'question'


# Creates a form for a Lecture tuple to add to database
class CommentForm(forms.ModelFrom):
    comment = forms.CharField(max_length=512)

    class Meta:
        model = Comment
        exclude = ('question', 'user')
