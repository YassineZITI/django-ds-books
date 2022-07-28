# django-ds-books
this repo presents a website where you can look for data science books and discuss data science topics.
the website is built using Django3 Bootstrap4 with Postgresql database.
i hosted a lite version of this project on heroku platform see it [here](https://ds-book.herokuapp.com/)
# Machine Learning in this project
there is two applications of machine learning algorithms in this project:
1. Content Based Recommander System to similars to each book you can see the notebook where i build this recommander system using nlp(in this repo).
2. Super users can uppload new books so to ensure that they uppload only it books i built a book classifier that can classify books based on their descriptions on IT books or Not you can find more details about this classifier in this [repo](https://github.com/YassineZITI/IT-or-Not-Books-)
# Demo
- ## home page : ![1](https://user-images.githubusercontent.com/76163895/181345920-2e0f7d3b-963e-42c1-9813-41257331ffb2.png)
- ## category books page : ![2](https://user-images.githubusercontent.com/76163895/181345934-9a6cf008-e56b-4a9b-932a-6077821525d8.png)
![4](https://user-images.githubusercontent.com/76163895/181345967-089d6552-c26a-4195-9cea-2c9d41390611.png)
- ## book detail : ![book_details](https://user-images.githubusercontent.com/76163895/181346060-acbcf170-975a-4b9a-949e-c1a8988749b4.png)
- ## discussions : ![5](https://user-images.githubusercontent.com/76163895/181345972-93b4031e-3f56-4172-89b6-e622402d5922.png)
- ## category posts : ![category_posts](https://user-images.githubusercontent.com/76163895/181498492-0a731e90-31fe-4915-965c-f5755d8d92bd.png)
- ## topic posts :![topic_posts](https://user-images.githubusercontent.com/76163895/181498468-39d28a5f-7b58-4a83-a727-8b7099b0e2d5.png)
- ## post detail : ![post_detail](https://user-images.githubusercontent.com/76163895/181346072-9e9911cd-aecf-4f90-baa1-9cb40a9a0391.png)
- ## login form : ![login](https://user-images.githubusercontent.com/76163895/181346068-3838909f-b3d3-4e85-a372-20a77c9320dd.png)
- ## register form : ![register_form](https://user-images.githubusercontent.com/76163895/181346079-8a07ea0b-b97c-4bd5-9aae-75d095489339.png)
- ## review form : ![review_form](https://user-images.githubusercontent.com/76163895/181346081-cce2b795-aff7-4d8e-a367-58fe0cd56aa6.png)
- ## search form : ![search](https://user-images.githubusercontent.com/76163895/181346083-34f2e815-2e0c-4b04-a3a2-31c844b13b68.png)
# Installation
1. clone the repo:
- if you have git installed: `git clone https://github.com/YassineZITI/django-ds-books/edit/main/README.md`
- if you don't. use this [website](https://minhaskamal.github.io/DownGit/) to download the repo.
2. set up envirement:
- `pip install virtualenv`
- `virtualenv venv`
- `pip install -r requirements.txt`
3. Database:
- you need a postgres database for this project(we use an array field wich is available only in postgres django).
- replace the database configuration in settings.py file with yours.
- `python manage.py makemigrations`
- `python manage.py migrate`
- now you need some data(books) see next step.
4. populate database:
### first method:
in this repo there are files called books.json and categories.json you will use those files to populate your database.
- `py manage.py loaddata categories.json `
- `py manage.py loaddata books.json`
### second method:
if you didn't succeed with the 1st method you can use app_data.pkl and categories.pkl with the following steps instead.
- open your commande prompt and type `py manage.py shell`
- `from blog.models import Book,Category`
- `import pickle`
- `with open('app_data.pkl','rb') as f:`
- indentation`    books = pickle.load(f) `
- `with open('categories.pkl','rb') as f:`
- indentation `    categories = pickle.load(f) `
- `for i in categories:`
- indentation `   category = Category(name=i)`
- indentation `   category.save()
- `for i in books:`
- indentation  `book=Book(ISBN=i['isbn13'],title=i['title'],description=i['description'],author=i['authors'],publisher=i['publisher'],published=i['year'],pages=i['pages'],stars=i['rating'],price=i['price'],image=i['image'],category=Category.objects.get(name=i['category']),similar_books=i['similar'],embedding=i['embedding'])`
- indentation `book.save()`
5. start server:
`py manage.py runserver`
# Improvements
- add like option on posts and comments.
- add models for machine learning models.
- add profile section for users.
- add admin dashboard.
- ...
# Contribution
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.
Please star the repo and feel free to use it.
....
