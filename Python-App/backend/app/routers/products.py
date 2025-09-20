from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..auth import get_current_user, require_role
from ..models import Product
from ..schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductRead)
def add_product(data: ProductCreate, current=Depends(get_current_user), session: Session = Depends(get_session)):
    require_role(current, "donor")
    p = Product(name=data.name, description=data.description, cost=data.cost, owner_id=current.id)
    session.add(p); session.commit(); session.refresh(p)
    return ProductRead(id=p.id, name=p.name, description=p.description, cost=p.cost, owner_name=current.name, owner_email=current.email)

@router.get("", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    rows = session.exec(select(Product)).all()
    out: list[ProductRead] = []
    for p in rows:
        owner = p.owner
        out.append(ProductRead(id=p.id, name=p.name, description=p.description, cost=p.cost, owner_name=owner.name if owner else "", owner_email=owner.email if owner else ""))
    return out