import datetime

from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


class ShotManager(models.Manager):
	pass


class Shot(models.Model):
	filename = models.CharField(max_length=144, blank=True)
	X = models.IntegerField(blank=False)
	Y = models.IntegerField(blank=False)
	metric = models.BooleanField(default=False)
	follow_through = models.BooleanField(default=False, blank=True)
	hold_release = models.BooleanField(default=False, blank=True)
	legs_straight = models.BooleanField(default=False, blank=True)
	lift_quick = models.BooleanField(default=False, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True)
	objects = ShotManager()


@receiver(post_save, sender=Shot)
def shot_post_save(sender, instance, **kwargs):
	count = Shot.objects.filter(filename=instance.filename).count()
	result = File.objects.update_or_create(name=instance.filename,
		defaults={"last_modified": timezone.now(), "count": count})
	if result[1] and count == 1:
		result[0].created = timezone.now()
		result[0].save()


@receiver(pre_save, sender=Shot)
def shot_pre_save(sender, **kwargs):
	pass


@receiver(pre_delete, sender=Shot)
def shot_pre_delete(sender, instance, using, **kwargs):
	count = Shot.objects.filter(filename=instance.filename).count()
	if count == 1:
		File.objects.filter(name=instance.filename).delete()


class FileManager(models.Manager):
	pass


class File(models.Model):
	name = models.CharField(max_length=144, blank=True, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True)
	count = models.IntegerField(default=0)
	objects = ShotManager()

	def get_absolute_url(self):
		return "/%i/" % self.name
