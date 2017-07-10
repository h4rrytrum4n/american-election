# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Hashtag(models.Model):
    hash_id = models.AutoField(primary_key=True)
    tweet_id = models.IntegerField(blank=True, null=True)
    text = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'hashtag'


class Tweet(models.Model):
    tweet_id = models.AutoField(primary_key=True)
    handle = models.CharField(max_length=20)
    body = models.CharField(max_length=200)
    time = models.DateTimeField()
    retweet_count = models.IntegerField(blank=True, null=True)
    favorite_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tweet'
