from django.core.management.base import BaseCommand
from django.db.models import Count

from catalog.core.models import Publication

import unicodecsv as csv
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Exports data to a csv file'

    def find_max(self, attribute):
        return Publication.objects.annotate(num=Count(attribute)).order_by('-num')[0].num

    def get_attribute_headers(self, title, max_attribute):
        header = []
        for i in range(0, max_attribute):
            header.append(title + str(i+1))
        return header

    def get_attribute_values(self, attributes, max_value):
        c = []
        for attr in attributes:
            c.append(str(attr))
        if len(c) != max_value:
            c.extend([""] * (max_value-len(c)))
        return c

    def handle(self, *args, **options):
        logger.debug("Starting to export data. Hang tight, this may take a while.")
        header = ["Publication Year", "Publication Title", "Journal Title", "Primary Author", "Code Url", "Docs"]
        max_platforms = self.find_max('platforms')
        max_sponsors = self.find_max('sponsors')
        header.extend(self.get_attribute_headers("Platform", max_platforms))
        header.extend(self.get_attribute_headers("Sponsor", max_sponsors))
        publications = Publication.objects.all().prefetch_related('sponsors', 'platforms').select_subclasses()

        filename = 'data.csv'
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            for pub in publications:
                row = [pub.date_published.year or pub.date_published_text, pub.title, str(pub.journal),
                        str(pub.creators.all()[0]), pub.code_archive_url, str(pub.model_documentation)]
                row.extend(self.get_attribute_values(pub.platforms.all(), max_platforms))
                row.extend(self.get_attribute_values(pub.sponsors.all(), max_sponsors))
                writer.writerow(row)
        logger.debug("Data export completed.");
