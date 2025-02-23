from graphene import Schema
from apps.product import schema as product_schema
from apps.accounts import schema as accounts_schema




class Query(
    product_schema.Query,
    accounts_schema.Query
):
    pass


class Mutation(
    product_schema.Mutation,
    accounts_schema.Mutation
    ):
    pass


schema = Schema(query=Query, mutation=Mutation)
