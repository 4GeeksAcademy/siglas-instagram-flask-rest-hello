from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Boolean
# from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Column, ForeignKey, Table, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # RELACIONES (más abajo se explican)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

    followers: Mapped[list["Follower"]] = relationship(
        foreign_keys="Follower.user_to_id",
        back_populates="followed"
    )
    following: Mapped[list["Follower"]] = relationship(
        foreign_keys="Follower.user_from_id",
        back_populates="follower"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # RELACIONES
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    comment: Mapped[str] = mapped_column(Text, nullable=False)

    # RELACIONES
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )

    # RELACIONES
    follower: Mapped["User"] = relationship(
        foreign_keys=[user_from_id],
        back_populates="following"
    )
    followed: Mapped["User"] = relationship(
        foreign_keys=[user_to_id],
        back_populates="followers"
    )


###################################3
follower = Table(
    "follower",
    db.Model.metadata,
    Column("user_from_id", ForeignKey("user.id"), primary_key=True),
    Column("user_to_id", ForeignKey("user.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Many-to-Many a si mismo
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower,
        primaryjoin=id == follower.c.user_from_id,
        secondaryjoin=id == follower.c.user_to_id,
        backref="followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
