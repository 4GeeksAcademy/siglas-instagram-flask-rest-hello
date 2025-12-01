from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import String, Boolean
#from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Column, ForeignKey, Table, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="comment")
 
    followers: Mapped[list["Follower"]] = relationship(foreign_keys="Follower.user_to_id", back_populates="followed")
    following: Mapped[list["Follower"]] = relationship(foreign_keys="Follower.user_from_id", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False) 
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
        }
    
class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment": self.comment,
        }
    

class Follower(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column (ForeignKey("user.id"), nullable=False)   

    follower: Mapped["User"] = relationship(foreign_keys=[user_from_id], back_populates="following")
    followed: Mapped["User"] = relationship(foreign_keys=[user_to_id], back_populates="follower")
 
    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }