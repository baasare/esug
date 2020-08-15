import random

import names
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from users.models import User


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        # parser.add_argument('total', type=int, help='Indicates the number of users to be created')

        parser.add_argument('-t', '--total', type=int, help='Indicates the number of users to be created')
        parser.add_argument('-a', '--admin', action='store_true', help='Create an admin account')

    def handle(self, *args, **options):

        total = options['total']
        admin = options['admin']

        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^#&*().,?0123456789'

        if total:
            for i in range(total):
                password = ''
                for c in range(8):
                    password += random.choice(chars)

                full_name = names.get_full_name()
                username = get_random_string()
                if admin:
                    User.objects.create_superuser(username="super_admin", email='admin@mail.com', password='be19RRY98')
                else:
                    User.objects.get_or_create(username=username, email=slugify(full_name) + '@esug.com',
                                               password=password)
        else:
            password = ''
            for c in range(8):
                password += random.choice(chars)

            full_name = names.get_full_name()
            username = get_random_string()
            if admin:
                User.objects.create_superuser(username="super_admin", email='admin@mail.com', password='be19RRY98')
            else:
                User.objects.get_or_create(username=username, email=slugify(full_name) + '@esug.com', password=password)
