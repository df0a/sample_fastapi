from .. import crud, schemas , oauth2
from ..database import  get_db
from fastapi import    status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db) ):
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user