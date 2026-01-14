from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    duration: str
    fees: int

class CourseCreate(CourseBase):
    name: str
    fee: int
    duration: str

class CourseUpdate(CourseBase):
    pass
class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    id: int
    name: str
    fee: int
    duration: str

    class Config:
        from_attributes = True
