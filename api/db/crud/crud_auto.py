from api.db.crud.base import CRUDBase
from api.db.models.auto import Auto
from api.db.schemas.auto import AutoCreate, AutoUpdate


class CRUDAuto(CRUDBase[Auto, AutoCreate, AutoUpdate]):
   ...


auto = CRUDAuto(Auto)
