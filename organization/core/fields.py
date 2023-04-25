try:
    from django.db.models import JSONField as OrigJSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField as OrigJSONField


class JSONField(OrigJSONField):
    def deconstruct(self):
        # the original path was 'django.db.models.JSONField' or 'django.contrib.postgres.fields....'
        name, path, args, kwargs = super().deconstruct()
        # Substitute 'my_app' by your application name everywhere.
        path = 'my_app.fields.JSONField'
        return name, path, args, kwargs