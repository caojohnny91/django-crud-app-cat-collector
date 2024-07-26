from django.db import models
from django.urls import reverse


# Create your models here.

MEALS = (("B", "Breakfast"), ("L", "Lunch"), ("D", "Dinner"))


class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    # Define a method to get the URL for this particular cat instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse("cat-detail", kwargs={"cat_id": self.id})


class Feeding(models.Model):
    date = models.DateField("Feeding Date")
    # adding "Feeding Date" changes title on admin page for the input form
    meal = models.CharField(
        max_length=1,
        # Note that we’re going to use just a single-character to represent what meal the feeding is for: "B"reakfast, "L"unch or "D"inner.
        # add the 'choices' field option
        choices=MEALS,
        # set the default value for meal to be 'B'
        default=MEALS[0][0],
    )
    # Create a cat_id column for each feeding in the database
    # As you can see, the ForeignKey field-type is used to create a one-to-many relationship.

    # The first argument provides the parent Model, Cat.
    # In a one-to-many relationship, the on_delete=models.CASCADE is required. It ensures that if a Cat record is deleted, all of the child Feedings will be deleted automatically as well - thus avoiding orphan records for feedings that are no longer tied to an existing Cat.
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    # In the database, the column in the feedings table for the FK will actually be called cat_id instead of "cat" because Django by default appends _id to the name of the attribute used in the Model.

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"
