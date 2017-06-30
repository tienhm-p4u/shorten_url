"""
Utilities for working with SQLAlchemy.
"""
import functools

from sqlalchemy import inspect


def from_dict(model, data, allow_pk=False):
    """
    Populate specified SQLAlchemy models object from specified dict.

    :param model: the models object to populate.
    :param data: the dict to populate the models with
    :param allow_pk: if False (default), modification of primary keys is
    disallowed. Raise ValueError if data dict contains primary keys.

    >>> from sqlalchemy import Column, Integer, Unicode
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> class Animal(declarative_base()):
    ...     __tablename__ = "animal"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(Unicode(100))
    >>> cat = Animal()
    >>> assert from_dict(cat, {"name": "grumpy"}).name == "grumpy"
    >>> assert from_dict(cat, {"id": 1}, allow_pk=True).id == 1
    >>> from_dict(cat, {"id": 1})  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Modification of PK is disallowed
    """
    info = inspect(model)
    columns = {c.key for c in info.mapper.column_attrs}
    primary_keys = {c.key for c in info.mapper.primary_key}

    if not allow_pk and (primary_keys & data.keys()):
        raise ValueError("Modification of PK is disallowed")

    update_keys = columns & data.keys()
    for k in update_keys:
        setattr(model, k, data[k])

    return model


def auto_manage_session(meth):
    """
    Decorator to wrap method inside an automatically managed session.

    The logic is as follows:
    - Wrapped method is called inside a sub-transaction
    - If method executes successfully (meaning no exception raised), the
    sub-transaction is committed and method result is returned, otherwise
    rollback and re-raise exception.
    - If sub-transaction is top-level (meaning its parent transaction is not a
    sub-transaction), also commit parent transaction so that every modification
    made inside is actually persisted into database
    - If sub-transaction is top-level, parent transaction must not having any
    uncommitted modification because we don't want to accidentally commit
    uncommitted changes made elsewhere

    To understand sub-transaction, see
    http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
    #using-subtransactions-with-autocommit
    """

    @functools.wraps(meth)
    def wrapper(cls, *args, **kwargs):  # pylint: disable=missing-docstring
        session = cls.session
        session_is_dirty = is_dirty(session)
        tx = session.begin(subtransactions=True)
        # whether this subtransaction is a top-level one (meaning its
        # parent transaction is NOT a subtransaction)
        is_top = tx._parent._parent is None
        if is_top and session_is_dirty:
            session.close()
            raise RuntimeError("Top-level transaction is not allowed to "
                               "begin when its parent is dirty")
        try:
            ret = meth(cls, *args, **kwargs)
            session.commit()
            if is_top:
                # also commit parent transaction when top-level
                # subtransaction is committed
                session.commit()
            return ret
        except:
            session.rollback()
            if is_top:
                session.rollback()
            raise

    return wrapper


def is_dirty(session):
    """
    Check whether a session is dirty i.e. having pending operations.

    Note: session should be dirty even when it has flushed its operations, but
    implementation is non-trivial and will proably produce a hard-to-use API.
    We will fix this later when https://fab.app360.vn/T898 and
    https://fab.app360.vn/T907 is fixed.
    """
    return bool(session.new or session.deleted or session.dirty)
