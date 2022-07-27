from db.crud.base import CRUDBase
from db.models.auto import Auto
from db.schemas.auto import AutoCreate, AutoUpdate


class CRUDAuto(CRUDBase[Auto, AutoCreate, AutoUpdate]):
    ...


crud_auto = CRUDAuto(Auto)
