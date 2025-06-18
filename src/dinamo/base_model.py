from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Date, Double, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, SmallInteger, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid

class Base(DeclarativeBase):
    pass


class Entity(Base):
    __tablename__ = 'entity'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='entity_pk_1'),
        UniqueConstraint('ENT_Name', name='entity_unique_1'),
        {'schema': 'config'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    ENT_Name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    end_ts: Mapped[datetime.date] = mapped_column(Date, server_default=text("'infinity'::date"))
    description: Mapped[Optional[str]] = mapped_column(String)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    create_ts: Mapped[Optional[datetime.date]] = mapped_column(Date)
    update_ts: Mapped[Optional[datetime.date]] = mapped_column(Date)

    fields: Mapped[List['Fields']] = relationship('Fields', back_populates='entity')


class Links(Base):
    __tablename__ = 'links'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='links_pk'),
        {'schema': 'config'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String)
    entity_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    field_id: Mapped[uuid.UUID] = mapped_column(Uuid)


class ListValues(Base):
    __tablename__ = 'list_values'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='list_values_pk'),
        {'schema': 'config'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    value: Mapped[str] = mapped_column(String)
    field_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    is_default: Mapped[Optional[bool]] = mapped_column(Boolean)


class Settings(Base):
    __tablename__ = 'settings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='settings_pk'),
        UniqueConstraint('code', name='settings_unique'),
        {'schema': 'config'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    code: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String)
    text_value: Mapped[Optional[str]] = mapped_column(String)
    number_value: Mapped[Optional[float]] = mapped_column(Double(53))
    annotation: Mapped[Optional[str]] = mapped_column(String)


class Fields(Base):
    __tablename__ = 'fields'
    __table_args__ = (
        ForeignKeyConstraint(['entity_id'], ['config.entity.id'], name='fields_entity_fk'),
        PrimaryKeyConstraint('id', name='fields_pk'),
        {'schema': 'config'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    FLD_Name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    entity: Mapped['Entity'] = relationship('Entity', back_populates='fields')
    field_extention: Mapped[List['FieldExtention']] = relationship('FieldExtention', back_populates='field')


class FieldExtention(Base):
    __tablename__ = 'field_extention'
    __table_args__ = (
        ForeignKeyConstraint(['field_id'], ['config.fields.id'], name='field_extention_fields_fk'),
        PrimaryKeyConstraint('id', name='field_extention_pk'),
        {'schema': 'config'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    field_id: Mapped[int] = mapped_column(BigInteger)
    position: Mapped[int] = mapped_column(SmallInteger)
    width: Mapped[int] = mapped_column(SmallInteger, server_default=text('1'))

    field: Mapped['Fields'] = relationship('Fields', back_populates='field_extention')
