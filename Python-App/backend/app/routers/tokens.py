from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Product, TokenRecord, User
from ..schemas import SpendIn, EarnIn
from ..auth import get_current_user, require_role

router = APIRouter(prefix="/tokens", tags=["tokens"])

@router.post("/earn")
def earn(data: EarnIn, current=Depends(get_current_user), session: Session = Depends(get_session)):
    require_role(current, "beneficiary")
    current.token_balance += data.amount
    session.add(TokenRecord(user_id=current.id, amount=data.amount, type="earn"))
    session.add(current); session.commit()
    return {"msg": "Tokens earned", "balance": current.token_balance}

@router.post("/spend")
def spend(data: SpendIn, current=Depends(get_current_user), session: Session = Depends(get_session)):
    require_role(current, "beneficiary")
    product = session.get(Product, data.product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    if current.token_balance < product.cost:
        raise HTTPException(400, "Not enough tokens")
    current.token_balance -= product.cost
    session.add(TokenRecord(user_id=current.id, amount=product.cost, type="spend", product_id=product.id))
    session.add(current); session.commit()
    return {"msg": f"Bought {product.name}", "balance": current.token_balance}