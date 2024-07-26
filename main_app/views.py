from django.shortcuts import render, redirect

# Import HttpResponse to send text-based responses
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy

# Import the FeedingForm
from .forms import FeedingForm


class CatCreate(CreateView):
    model = Cat
    # all inherits from CreateView to create our own CBV used to create cats
    # fields = '__all__'
    # alter we can specify the fields we want
    fields = ["name", "breed", "description", "age"]


class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ["breed", "description", "age"]


class CatDelete(DeleteView):
    model = Cat
    success_url = "/cats/"


class ToyCreate(CreateView):
    model = Toy
    fields = "__all__"


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyUpdate(UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys/"


# Create your views here.
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def cat_index(request):
    cats = Cat.objects.all()
    return render(request, "cats/index.html", {"cats": cats})


# def cat_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id)
#     return render(request, "cats/detail.html", {"cat": cat})
# { inside curly brackets is a dictionary}


# update this view function to include feeding form
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


def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


def remove_toy(request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    toy = Toy.objects.get(id=toy_id)
    cat.toys.remove(toy)
    return redirect("cat-detail", cat_id=cat_id)
