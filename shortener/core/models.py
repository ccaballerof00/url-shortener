from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime

# Create your models here.

class LinkQuerySet(models.QuerySet):
    def decode_link(self, idurl):
        decode = Hashids(min_length=10, alphabet='abcdefghijklmnopqrstuvwxyz').decode(idurl)[0]
        self.filter(pk=decode).update(counter=models.F('counter') + 1)
        return self.filter(pk=decode).first().url
    
    def total_links(self):
        return self.count()
    
    def total_redirects(self):
        return self.aggregate(redirects = models.Sum('counter'))
    
    def dates(self, pk):
        return self.values('date').annotate(
            july = models.Sum('counter', filter=models.Q(date__gte=datetime.date(2023,7,1),
             date__lte=datetime.date(2023,7,31)))
        ).filter(pk=pk)

class Link(models.Model):
    url = models.URLField()
    idurl = models.CharField(max_length=10, blank=True)
    date = models.DateField(auto_now_add=True)
    counter = models.IntegerField(default=0)

    links = LinkQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'Links'

    def __str__(self):
        return f"URL: {self.url} ID: {self.idurl}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.idurl:
            self.idurl = Hashids(min_length=10, alphabet='abcdefghijklmnopqrstuvwxyz').encode(self.pk)
            self.save()
    def get_absolute_url(self):
        return reverse('core:detail', kwargs={'pk' : self.pk})
    
