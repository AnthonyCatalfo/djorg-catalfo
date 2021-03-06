from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import Note as NoteModel

class Note(DjangoObjectType):
    class Meta:
        model=NoteModel
        interfaces=(graphene.relay.Node, ) #tuple (x, )
class Query(graphene.ObjectType):
    notes=graphene.List(Note)


    def resolve_notes(self,info):
        """Decide which notes to return."""
        user=info.context.user
        
        if settings.DEBUG:
            return NoteModel.objects.all()
        elif user.is_anonymous:
            return NoteModel.objects.none()
        else: 
            return NoteModel.objects.filter(user=user)
schema=graphene.Schema(query=Query)


