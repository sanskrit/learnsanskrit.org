from flask.ext.principal import Permission, RoleNeed
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from lso import app
from ..database import Base, SimpleBase


class UserRoleAssoc(Base):
    __tablename__ = 'user_role_assoc'
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    role_id = Column(ForeignKey('role.id'), primary_key=True)


class User(SimpleBase, UserMixin):
    email = Column(String, unique=True)
    password = Column(String(255))
    active = Column(Boolean)

    roles = relationship('Role', secondary='user_role_assoc', backref='users')

    def has_role(self, role):
        p = Permission(RoleNeed(role))
        return p.can()

    def is_admin(self):
        return self.has_role('admin')


class Role(SimpleBase, RoleMixin):
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return '<Role(%s, %s)>' % (self.id, self.name)


def drop():
    """Drop the tables defined above."""

    import sqlalchemy
    order = [UserRoleAssoc, User, Role]
    for o in order:
        try:
            o.__table__.drop()
        except sqlalchemy.exc.ProgrammingError:
            print '(table %s does not exist.)' % o.__tablename__
