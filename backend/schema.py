from graphene import Schema
from apps.outlet import schema as outlet_schema
from apps.kitchen import schema as kitchen_schema
from apps.product import schema as product_schema




class Query(
    outlet_schema.Query,
    kitchen_schema.Query,
    product_schema.Query
):
    pass


class Mutation(
    outlet_schema.Mutation,
    kitchen_schema.Mutation,
    product_schema.Mutation
    ):
    pass


schema = Schema(query=Query, mutation=Mutation)
