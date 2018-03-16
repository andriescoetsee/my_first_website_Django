from django.db import models

# Create your models here.
class PublicHoliday(models.Model):
    name = models.TextField()
    date = models.DateField()

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return self.date.strftime('%Y-%m-%d') + "  --->  " + self.name

class WeekDay(models.Model):

    name = models.TextField()
    nr	= models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return self.name