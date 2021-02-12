from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    review = models.CharField(
        max_length=1000,
        help_text='Enter your review'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def get_reviewer(self):
        return self.reviewer.name

    def __str__(self):
        return self.review
