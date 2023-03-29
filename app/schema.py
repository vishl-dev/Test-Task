import graphene
from graphene_django import DjangoObjectType
from .models import Component


class ComponentType(DjangoObjectType):
    class Meta:
        model = Component
        fields = '__all__'


# Fetch All Components API
class Query(graphene.ObjectType):
    tasks = graphene.List(ComponentType)

    def resolve_tasks(root, info, **kwargs):
        return Component.objects.all()


# Create API
class CreateComponent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        status = graphene.String(required=True)

    task = graphene.Field(ComponentType)

    @classmethod
    def mutate(cls, root, info, name, status):
        task = Component()
        task.name = name
        task.status = status
        task.save()
        
        return CreateComponent(task=task)


# Update API   
class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
        status = graphene.String(required=True)

    post = graphene.Field(ComponentType)
   
    @classmethod
    def mutate(cls, self, info, id, name, status):
        post = Component.objects.get(id=id)
        post.name = name
        post.status = status
        post.save()
        return UpdatePost(post=post)


class Mutation(graphene.ObjectType):
    create_new_post = CreateComponent.Field()
    update_post = UpdatePost.Field()


# Delete API
class DeleteComponent(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    task = graphene.Field(ComponentType)

    @staticmethod
    def mutate(root, info, id):
        task_instance = Component.objects.get(pk=id)
        task_instance.delete()

        return Component.objects.all()


# Change Status
class ChangeStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        status = graphene.String(required=True)
 
    post = graphene.Field(ComponentType)
   
    @classmethod
    def mutate(cls, self, info, id, status):
        post = Component.objects.get(id=id)
        post.status = status
        post.save()
        return UpdatePost(post=post)


# Bulk Delete API
class BulkDeleteMutation(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.ID, required=True)
    
    success = graphene.Boolean()
    def mutate(self, info, ids):
        queryset = Component.objects.filter(id__in=ids)
        queryset.delete()
        return BulkDeleteMutation(success=True)


# Register Mutation
class Mutation(graphene.ObjectType):
    create_task = CreateComponent.Field()
    update_task = UpdatePost.Field()
    delete_task = DeleteComponent.Field()
    change_status = ChangeStatus.Field()
    bulk_delete = BulkDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)