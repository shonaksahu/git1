
from ast import Pass, pattern
import email
import string
from turtle import update
from unicodedata import name
import graphene
from graphene_django import DjangoObjectType
import empapp
from empapp.models import Employee 
# class CreatePerson(graphene.Mutation):
#     class Arguments:
#         name = graphene.String()

#     ok = graphene.Boolean()
#     person = graphene.Field(lambda: Person)

#     def mutate(root, info, name):
#         person = Person(name=name)
#         ok = True
#         return CreatePerson(person=person, ok=ok)
class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee
        fields = ("name", "email", "username", "password")

class EmployeeDetail(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    username = graphene.String()
    
# class Query(graphene.ObjectType):
#     all_emp = graphene.List(EmployeeDetail)

#     def resolve_all_emp(root, info):
#         return Employee.objects.all()
class Query(graphene.ObjectType):
    all_emp = graphene.List(EmployeeDetail)

    def resolve_all_emp(root, info):
        return Employee.objects.filter(name__startswith='sh')

class CreateEmployee(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        username = graphene.String()
        password = graphene.String()
    ok = graphene.Boolean()
    employee = graphene.Field(lambda: EmployeeDetail)


    def mutate(root, info, name, email, username, password):
        employee = EmployeeDetail(name=name, email=email, username=username, password=password)
        Employee.objects.create(name=name, email=email, username=username, password=password)

        ok = True
        return CreateEmployee(employee=employee, ok=ok)
    
class EmployeeMutations(graphene.ObjectType):
    create_emp = CreateEmployee.Field()

class UpdateEmployee(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()
    employee = graphene.Field(EmployeeType)
                                                         
    def mutate(root, info, name, id):
        employee = Employee.objects.get(pk=id)
        employee.name = name
        employee.save()
        return UpdateEmployee(employee=employee)

class UpdateEmployeeMutations(graphene.ObjectType):
    update_emp = UpdateEmployee.Field()

class DeleteEmployee(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    employee = graphene.Field(EmployeeType)
    
    @staticmethod
    def mutate(root, info, id):
        shonak = Employee.objects.get(pk=id)
        shonak.delete()
        return None

class DeleteEmployeeMutations(graphene.ObjectType):
    delete_emp = DeleteEmployee.Field()

# class Query(graphene.ObjectType):
#     all_emp = graphene.List(EmployeeDetail)

#     def resolve_all_emp(root, info):
#         return Employee.objects.filter(pattern in string)

class Mutation(
    EmployeeMutations,
    UpdateEmployeeMutations,
    DeleteEmployeeMutations
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)