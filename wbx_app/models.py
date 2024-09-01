from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} | {self.name}"
        else:
            return self.name

    class Meta:
        verbose_name_plural = "categories"


class Lot(models.Model):
    id = models.AutoField(primary_key=True)
    id_tlg = models.IntegerField()
    dt_create = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    categories = models.ManyToManyField(Category, related_name="lots")
    url_photos = models.JSONField()
    url_chat = models.URLField(null=True)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    region = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    working_time_start = models.TimeField(default="08:00:00")
    working_time_end = models.TimeField(default="22:00:00")
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    id_tlg = models.IntegerField(unique=True)
    timer = models.DateTimeField(auto_now_add=True)
    coordinates = models.JSONField(null=True)
    locations = models.JSONField(null=True)
    region = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    working_time_start = models.TimeField(default="08:00:00")
    working_time_end = models.TimeField(default="22:00:00")
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.id_tlg}"
