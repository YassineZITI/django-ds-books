from django.shortcuts import render,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import DetailView, ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from bs4 import BeautifulSoup
import datetime
from .models import Book,Category,ReviewRating
from .forms import ReviewForm
from django.db.models import Q
from django.contrib import messages
from .classifier import predict,similars



def Home(request):
	#year = str(datetime.date.today().year)
	#books = Book.objects.filter(published = year )[:16]
	return render(request,'blog/home1.html',)#context={'books':books})

def category(request,category):
	category_id = Category.objects.get(name=category).id
	books = Book.objects.filter(category = category_id )
	paginator = Paginator(books, 8) # Show 8 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'blog/category.html',context={'page_obj':page_obj,'category':category})	

def Free(request):
	search_query = ''
	books = Book.objects.filter(price = '$0.00' )
	paginator = Paginator(books, 8) # Show 8 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request,'blog/free.html',context={'page_obj':page_obj})

def SearchBook(request):
	search_query = ''
	if request.GET.get('search'):
		search_query = request.GET.get('search')
	
	
	
	books = Book.objects.filter(Q(title__icontains=search_query) | Q(ISBN=search_query))

	paginator = Paginator(books, 8) # Show 8 contacts per page.
	page_number = request.GET.get('page')
	try:
		page_obj = paginator.get_page(page_number)
	except PageNotAnInteger:
		page_number = 10
		page_obj = paginator.get_page(page_number)
	except EmptyPage:
		page_obj = paginator.get_page(paginator.num_pages)
	count = len(books)
	if count == 1:
		messages.info(request,'great!! this is the book you look for')
		return redirect('book-detail',books.first().id)
	return render(request,'Blog/search_books.html',{
		'search_query':search_query,
        'page_obj':page_obj,
        'count' : count
        })
	
	

class CategoryListView(ListView):
	model = Category
	ordering = ['name']
	template_name = 'blog/categories.html'
	def get_context_data(self, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		num_books = [ (category ,Book.objects.filter(category=category).count())  for category in Category.objects.all()]
		context['object'] = num_books
		return context

class BookCreateView(LoginRequiredMixin,CreateView):
	model = Book
	fields = ['ISBN','title','description','author','publisher','published','pages','stars','price','image','category']
	
	def form_valid(self,form):
		url = self.request.META.get('HTTP_REFERER')
		instance = form.save(commit=False)
		prediction, embedding = predict(instance.description)
		if prediction == 'IT':
			instance.similar_books = similars(embedding)
			instance.embedding = embedding
			instance.save()
			messages.success(self.request, "The book uploaded successefully.")
			return redirect('home')
		else:
			
			messages.warning(self.request, "Sorry!! you can't upload this book it's not an it book.")
			return redirect(url)
class BookDetailView(DetailView):
	model = Book

	def get_context_data(self, **kwargs):
		context = super(BookDetailView, self).get_context_data(**kwargs)
		#similar books
		isbns = context['object'].similar_books.split(' ')[:-1]
		similar = [Book.objects.get(ISBN=i.strip()) for i in isbns]
		#reviews
		reviews = ReviewRating.objects.filter(book__id=context['object'].id)
		#down_link
		down_link = ''
		if context['object'].price == "$0.00":
			response = requests.get('https://itbook.store/books/' + context['object'].ISBN).content
			try:
				soup = BeautifulSoup(response,'html.parser')
				down_link = soup.find('a',title='Free Download')['href']
			except:
				pass

		context['down_link'] = down_link
		context['buy_link'] = 'https://itbook.store/go/buy/' + context['object'].ISBN
		context['similar'] = similar
		context['reviews'] = reviews
		return context

def submit_review(request, book_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, book__id=book_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.book_id = book_id
                data.user_id = request.user.id
                data.save()
                return redirect(url)


