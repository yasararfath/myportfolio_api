from fastapi import APIRouter,status,Depends
from app.models import About
from app.schema.about_schema import CreateAbout,CreateAboutResponse
from sqlalchemy.orm.session import Session
from app.models import About
from app.database import get_db
from typing import List
from app.oauth2 import get_current_user
router = APIRouter(prefix='/about',
                tags=['About'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CreateAboutResponse)
def create_about(about:CreateAbout,db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    about_data = About(user_id=current_user.id,**about.dict())
    db.add(about_data)
    db.commit()
    db.refresh(about_data)

    return about_data

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[CreateAboutResponse])
def get_about(db:Session=Depends(get_db)):
    res = db.query(About).all()
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Data Found")
    
    return res
