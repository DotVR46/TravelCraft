from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from app.schemas.place import schema

router = APIRouter()
graphql_app = GraphQLRouter(schema)
router.include_router(graphql_app, prefix="/graphql")
