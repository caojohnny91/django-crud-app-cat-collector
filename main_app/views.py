from django.shortcuts import render, redirect
# Import HttpResponse to send text-based responses
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
# Import the FeedingForm
from .forms import FeedingForm
# import auth
from django.contrib.auth.views import LoginView
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

# Finally, we can protect class-based views like this with loginMixin
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    # all inherits from CreateView to create our own CBV used to create cats
    # fields = '__all__'
    # alter we can specify the fields we want
    fields = ["name", "breed", "description", "age"]

    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual. super is parent class
        return super().form_valid(form)
    # We’re overriding the CreateView’s form_valid method to assign the logged in user, self.request.user. Yes, the built-in auth automatically assigns the user to the request object similarly our middleware in Express.
    # In Python, methods inherited by the superclass can be invoked by prefacing the method name with super(). Accordingly, after updating the form to include the user, we’re calling super().form_valid(form) to let the CreateView do its usual job of creating the model in the database and redirecting.


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ["breed", "description", "age"]


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = "/cats/"


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = "__all__"


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = "/toys/"


# Create your views here.
# def home(request):
#     return render(request, "home.html")
# And use it in a class based view that replaces the current home view function.
# django auth is imported and need to update Home
class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, "about.html")

# Now we can simply “decorate” any view function that requires a user to be logged in like this:
@login_required
def cat_index(request):
    # cats = Cat.objects.all()
    cats = Cat.objects.filter(user=request.user)
    # You could also retrieve the logged in user's cats like this
    # cats = request.user.cat_set.all()
    return render(request, 'cats/index.html', { 'cats': cats })

# def cat_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id)
#     return render(request, "cats/detail.html", {"cat": cat})
# { inside curly brackets is a dictionary}


# update this view function to include feeding form
@login_required
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # toys = Toy.objects.all()  # Fetch all toys
    # Updating to Only get the toys the cat does not have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list("id"))
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(
        request,
        "cats/detail.html",
        {
            # include the cat and feeding_form in the context
            "cat": cat,
            "feeding_form": feeding_form,
            # "toys": toys,  # Pass toys to the template
            # updating toys
            "toys": toys_cat_doesnt_have,
        },
    )


@login_required
def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        # wait to save the relationship ID first
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect("cat-detail", cat_id=cat_id)

# First we capture data from the user via the FeedingForm(request.POST) and prepare it for the database.
# The method form.is_valid() checks if the submitted form data is valid according to the form’s specifications, such as required fields being filled and data types matching the model’s requirements.
# After ensuring that the form contains valid data, we save the form with the commit=False option, which returns an in-memory model object so that we can assign the cat_id before actually saving to the database.
# Finally we will redirect instead of render since data has been changed in the database.


@login_required
def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


@login_required
def remove_toy(request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    toy = Toy.objects.get(id=toy_id)
    cat.toys.remove(toy)
    return redirect("cat-detail", cat_id=cat_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            # login is a function on the auth app that is imported at the top
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )

