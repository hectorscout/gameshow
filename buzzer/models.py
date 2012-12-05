from django.db import models

class Setting(models.Model):
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.value)

class Player(models.Model):
    name = models.CharField(max_length=128)
    score = models.IntegerField()

    def __unicode__(self):
        return '%s: %s' % (self.name, self.score)

class Buzz(models.Model):
    name = models.CharField(max_length=128)
    retrieved = models.BooleanField()
    def __unicode__(self):
        return '%s: %s' % (self.name, self.retrieved and 'Retrieved' or 'New')

