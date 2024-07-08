import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Quiz, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class QuizType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'category', 'quiz', )


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('title', 'quiz', )
        

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('question', 'answer_text', )


class Query(graphene.ObjectType):
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    
    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)
    
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id).all()

class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    
    Category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return UpdateCategory(category)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    Category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return

class Mutation(graphene.ObjectType):
    add_category = CategoryMutation.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)
