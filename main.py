from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from model import chain, generate_answer
app = FastAPI()


class SpanModel(BaseModel):
    start_index: int
    end_index: int


class EntityModel(BaseModel):
    value: str
    entity_type: str
    span: SpanModel
    entity: str
    source_type: str


class EntityListModel(BaseModel):
    entities: List[EntityModel]


class TextRequestModel(BaseModel):
    texts: List[str]


class EntitiesResponseModel(BaseModel):
    entities_list: List[EntityListModel]



@app.post("/extract_entities", response_model=EntitiesResponseModel)
async def extract_entities(request: TextRequestModel):
    entities_list = []

    for text in request.texts:
        answers = await generate_answer(text,chain)

        entities = []
        for per in answers:
            entity = {
                "value": per[0],
                "entity_type": 'PERSON',
                "span": {
                    "start_index": per[1][0],
                    "end_index": per[1][1]
                },
                "entity": per[0],
                "source_type": "SLOVNET"
            }
            entities.append(entity)

        entities_list.append({"entities": entities})

    return EntitiesResponseModel(entities_list=entities_list)