
from audioop import reverse
from unicodedata import category
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from blog.models import Category
from .models import Topic,Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .forms import CommentForm,TopicForm
# Create your views here.




def discussion(request,category):
	category_id = Category.objects.get(name=category).id
	topics = Topic.objects.filter(category = category_id )
	topic_posts = [ (topic ,Post.objects.filter(topic=topic).count())  for topic in topics]
	return render(request,'discussion/topics.html',context={'object':topic_posts,'category':category})



class PostListView(ListView):
	model = Post
	template_name = 'discussion/posts.html' #<app>/<model>_<viewtype>.html
	ordering = ['-date_posted']
	paginate_by = 4
	
	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

class CategoryPostListView(ListView):
	model = Post
	template_name = 'discussion/category_posts.html' #<app>/<model>_<viewtype>.html
	ordering = ['-date_posted']
	paginate_by = 4
	
	def get_queryset(self):
		category_name = self.kwargs['category']
		category = Category.objects.get(name=category_name)
		topics = Topic.objects.filter(category=category)
		posts = Post.objects.filter(topic__in=topics)
		
		return posts
	def get_context_data(self, **kwargs):
		context = super(CategoryPostListView, self).get_context_data(**kwargs)
		category_name = self.kwargs['category']
		category = Category.objects.get(name=category_name)
		topics = Topic.objects.filter(category=category)
		context['topics'] = topics 
		context['category'] = category
		return context
	def post(self, request, *args, **kwargs):
		url = request.META.get('HTTP_REFERER')
		form = TopicForm(request.POST)
		if form.is_valid():
			data = Topic()
			data.title = form.cleaned_data['title']
			data.description = form.cleaned_data['description']
			data.category_id = Category.objects.get(name=self.kwargs['category']).id
			data.save()
		return redirect(url)
	
		
class TopicPostListView(ListView):
	model = Post
	template_name = 'discussion/topic_posts.html' #<app>/<model>_<viewtype>.html
	ordering = ['-date_posted']
	paginate_by = 4
	def get_queryset(self):
		topic = self.kwargs['topic'] 
		try:
			topic_posts = Post.objects.filter(topic=Topic.objects.get(title=topic))
		except:
			topic_posts = Post.objects.all()
		return topic_posts
	def get_context_data(self, **kwargs):
		context = super(TopicPostListView, self).get_context_data(**kwargs)
		category_name = self.kwargs['category']
		category = Category.objects.get(name=category_name)
		topics = Topic.objects.filter(category=category) 
		context['topic'] = self.kwargs['topic']
		context['topics'] = topics 
		context['category'] = category
		return context
	



class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','content']
    
	def form_valid(self,form):
		form.instance.author = self.request.user
		form.instance.topic = Topic.objects.get(title=self.kwargs['topic'])
		return super().form_valid(form)

class PostDetailView(DetailView):
	model = Post 

	def get_context_data(self,**kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		comments = Comment.objects.filter(post=self.get_object())
		context['comments'] = comments
		return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	
	def get_success_url(self):
		post  = self.get_object()
		topic = Topic.objects.get(title=post.topic)
		category = Category.objects.get(name=topic.category)
		return reverse_lazy('posts')

	def test_func(self):
		post  = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def submit_comment(request, post_id):
	url = request.META.get('HTTP_REFERER')
	if request.method == 'POST':
		
		form = CommentForm(request.POST)
		if form.is_valid():

			data = Comment()
			data.content = form.cleaned_data['content']
			data.post_id = post_id
			data.user_id = request.user.id
			data.save()
			return redirect(url)




		