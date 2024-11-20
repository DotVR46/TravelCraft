import strawberry


@strawberry.type
class Query:
    hello: str = "Hello from TravelCraft!"


schema = strawberry.Schema(query=Query)
