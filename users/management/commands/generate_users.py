import secrets
import string

import xlrd
from django.core.management import BaseCommand

from election.models import Voter


class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **options):

        workbook = xlrd.open_workbook("names.xlsx")
        sheet = workbook.sheet_by_index(0)

        alphabet = string.ascii_letters + string.digits + string.punctuation

        for row in range(sheet.nrows)[1:]:
            values = sheet.row_values(row)
            full_name = values[0]

            email = values[2]

            while True:
                pass_code = ''.join(secrets.choice(alphabet) for i in range(8))
                if (any(c.islower() for c in pass_code) and any(c.isupper() for c in pass_code) and
                        any(c.isdigit() for c in pass_code) and any(c in string.punctuation for c in pass_code)):
                    break

            if not (full_name and email):
                raise ValueError(f'Invalid User data!')

            v, voter = Voter.objects.get_or_create(
                full_name=full_name,
                email=email,
                pass_code=pass_code
            )

            v.save()
