from dataclasses import fields
from .models import Comment, Topic
from django.forms import ModelForm



class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['content']


class TopicForm(ModelForm):
	class Meta:
		model = Topic
		fields = ['title','description']