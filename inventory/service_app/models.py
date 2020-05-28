from djongo import models


class Film(models.Model):
    title_alphanum = models.CharField(max_length=60)
    primary_title = models.CharField(max_length=60)
    is_adult = models.BooleanField()
    start_year = models.IntegerField(default=0)
    runtime_minutes = models.IntegerField()
    genres = models.ListField(default=[])
    directors = models.ListField(default=[])
    average_rating = models.FloatField()
    num_votes = models.IntegerField(default=0)

    objects = models.DjongoManager()

    def __str__(self):
        return self.primary_title

    # class Meta:
    #    db_table = 'films'
