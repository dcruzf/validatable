from functools import partial

from sqlalchemy.engine import create_engine as sa_create_engine

create_engine = partial(
    sa_create_engine,
    json_deserializer=lambda x: x,
    json_serializer=lambda x: x,
)

# import json
# from pydantic.json import pydantic_encoder
# create_engine = partial(
#     sa_create_engine,
#     json_deserializer=lambda x: x,
#     json_serializer=lambda obj: json.dumps(obj, default=pydantic_encoder),
# )
