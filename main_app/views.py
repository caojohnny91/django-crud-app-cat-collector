from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat

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


# update this view function to include feeding form
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(
        request,
        "cats/detail.html",
        {
            # include the cat and feeding_form in the context
            "cat": cat,
            "feeding_form": feeding_form,
        },
    )
