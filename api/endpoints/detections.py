from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.core.settings import get_logger
from api.db import schemas
from api.db.auth import get_db
from api.db.crud import crud_auto


router = APIRouter()
logger = get_logger('endpoints detections')
logger.getChild('endpoints detections')


@router.get("/search/", status_code=200, response_model=schemas.Auto)
def search_recipes(
    *,
    keyword: str = Query(None, min_length=3, example="auto"),
    min_results: Optional[int] = 1,
    max_results: Optional[int] = 10,
    db: Session = Depends(get_db),
) -> dict:
    """
    Search for recipes based on label keyword
    """
    recipes = crud_auto.auto.get_multi(db=db, skip=min_results,  limit=max_results)
    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)

    return {"results": list(results)}

