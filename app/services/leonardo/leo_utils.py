from typing import Annotated
import httpx
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

list_elements_url = "https://cloud.leonardo.ai/api/rest/v1/elements"


class UtilsHeaders(BaseModel):
    accept: str
    authorization: str


@app.get(list_elements_url)
async def list_elements(headers: Annotated[UtilsHeaders, Header()]) -> None:
    pass
