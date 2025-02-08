from graphene import Schema
from apps.outlet import schema as outlet_schema
from apps.kitchen import schema as kitchen_schema
from apps.product import schema as product_schema
from apps.accounts import schema as accounts_schema
from apps.inventory import schema as inventory_schema


class Query(
    outlet_schema.Query,
    kitchen_schema.Query,
    product_schema.Query,
    accounts_schema.Query,
    inventory_schema.Query
):
    pass


class Mutation(
    outlet_schema.Mutation,
    kitchen_schema.Mutation,
    product_schema.Mutation,
    accounts_schema.Mutation,
    inventory_schema.Mutation
    ):
    pass


schema = Schema(query=Query, mutation=Mutation)
