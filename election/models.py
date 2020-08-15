import random
import secrets
import string

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

alphabet = string.ascii_letters + string.digits + string.punctuation


# Create your models here.
class Queries(models.Model):
    name = models.CharField(_('name'), max_length=30, blank=False)
    email = models.CharField(_('query from'), max_length=30, blank=False)
    subject = models.CharField(_('subject'), max_length=40, blank=False)
    message = models.TextField(_('message'), blank=False)
    sent_at = models.DateTimeField(_('date'), auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _('Query')
        verbose_name_plural = _('Queries')


class Election(models.Model):
    name = models.CharField(max_length=50)
    year = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="positions")
    contestable = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.name


class Candidate(models.Model):
    LEVEL = (
        ('level_400', 'Level 400'),
        ('level_300', 'Level 300'),
        ('level_200', 'Level 200'),
        ('level_100', 'Level 100'),
    )

    COURSE = (
        ('AREN', 'Agricultural Engineering'),
        ('BMEN', 'Biomedical Engineering'),
        ('CPEN', 'Computer Engineering'),
        ('FPEN', 'Food Processing Engineering'),
        ('MTEN', 'Materials Science & Engineering')
    )

    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    avatar = models.ImageField(upload_to='avatars/')
    full_name = models.CharField(max_length=70)
    level = models.CharField(max_length=30, choices=LEVEL, default="level_100")
    course_offering = models.CharField(max_length=70, choices=COURSE, default="AREN")
    bio = models.TextField(blank=True)
    year = models.DateField(auto_now=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return self.full_name

    def total_votes(self, ):
        return self.votes.count()

    def get_absolute_url(self):
        return reverse('candidate_detail', args=[str(self.id)])


class Voter(models.Model):
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=False)
    pass_code = models.CharField(_('pass code'), max_length=30, blank=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['my_order']
        verbose_name = _('Voter')
        verbose_name_plural = _('Voters')

    def get_email(self):
        return '%s' % self.email

    def __str__(self):
        return '%s' % self.full_name

    def save(self, *args, **kwargs):
        while True:
            pass_code = ''.join(secrets.choice(alphabet) for i in range(random.randint(8, 30)))
            if (any(c.islower() for c in pass_code) and any(c.isupper() for c in pass_code) and
                    any(c.isdigit() for c in pass_code) and any(c in string.punctuation for c in pass_code)):
                break

        self.pass_code = pass_code
        super(Voter, self).save(*args, **kwargs)


class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)


class PassCodeEmails(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=200)
    pass_code = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
