from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db.models import DateTimeField, DateField, F
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class Command(BaseCommand):
    args = "<rebase_date>"
    help = """
    Rebases all date and datetime fields such that their offset from today is the
    same as their offset from the specified <rebase_date>.
    Requires d.c.contenttypes and Django>1.4.
    """

    def handle(self, *args, **options):
        rebase_date = self.parse_rebase_date(args[0])
        now = timezone.now().date()
        delta = now - rebase_date

        self.ignores = getattr(settings, 'DEMO_DATE_RESET_IGNORES', { })
        
        for model in ContentType.objects.all():
            klass = model.model_class()
            fields = self.get_date_fields_for_klass(klass)
            if fields:
                update_kwargs = dict([
                    (field_name, F(field_name) + delta) for field_name in fields
                    ])
                klass.objects.update(**update_kwargs)

    def parse_rebase_date(self, rebase_date_str):
        """
        Parse the supplied rebase_date using a DateField
        """
        field = DateField()
        try:
            return field.to_python(rebase_date_str)
        except ValidationError:
            raise CommandError('Cannot parse date from "%s"' % rebase_date_str)

    def get_date_fields_for_klass(self, klass):
        """
        Lookup the date/datetime fields in the specified model class
        Returns a list of the field names to be updated
        """
        klass_name = '.'.join((klass.__module__, klass.__name__))
        klass_ignores = self.ignores.get(klass_name, [ ])
        return [
                field.name
                for field in klass._meta.fields
                if (
                    isinstance(field, (DateTimeField, DateField))
                    and field.name not in klass_ignores
                )
            ]

