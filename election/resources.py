from import_export import resources

from .models import Voter


class VoterResource(resources.ModelResource):
    class Meta:
        model = Voter
        import_id_fields = ('full_name', 'email',)
        fields = ('full_name', 'email',)
        export_order = ('full_name', 'email',)
        exclude = ('id', )
