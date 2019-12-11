from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
class BookListView(generic.ListView):
    model = Book
    paginate_by = 1
    #template_name = 'abc.html'
    # def get_context_data(self, **kwargs):
    # 	# Call the base implementation first to get the context
    # 	context = super(BookListView, self).get_context_data(**kwargs)
    # 	# Create any data and add it to the context
    # 	context['books'] = Book.objects.all()
    # 	return context
class AuthorListView(generic.ListView):
	model = Author

class BookDetailView(generic.DetailView):
    model = Book
    # def book_detail_view(request, pk):

    # 	try:
    #     	book = Book.objects.get(pk=pk)
    # 	except Book.DoesNotExist:
    #     	raise Http404('Book does not exist')
    
    # 	return render(request, 'catalog/book_detail.html', context={'the_book': book})

class AuthorDetailView(generic.DetailView):
	model = Author



# @login_required
# def test(request):
#     return HttpResponse("Welcome to test page");

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



class BorrowedBooksListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
    model =  BookInstance
    template_name ='catalog/bookinstance_list_librarians.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')