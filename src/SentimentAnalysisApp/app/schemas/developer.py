"""
Created by Frantisek Sabol
"""
from pydantic import BaseModel


class DeveloperBase(BaseModel):
    name: str


class DeveloperCreate(DeveloperBase):
    name: str


class DeveloperUpdate(DeveloperBase):
    name: str


class DeveloperInDBBase(DeveloperBase):
    id: int

    class Config:
        orm_mode = True


class Developer(DeveloperInDBBase):
    pass
