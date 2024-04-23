from django.db import models

# Create your models here.
class Chats(models.Model):
	username = models.CharField(max_length = 255, null = False)
	chatted_with = models.CharField(max_length = 255, null = False)
	sent_messages = models.JSONField(default = dict, null = True, blank = True)
	time = models.CharField(max_length = 255, null = True, blank = True)
