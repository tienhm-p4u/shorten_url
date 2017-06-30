import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import endpoint
from models import Base


def make_app():
    main = Flask(__name__)
    main.config.from_envvar("FLASK_CONFIG", silent=True)
    main.config.from_object('conf.config')
    main.config.update(os.environ)

    # POSTGRES
    main.config["SQLALCHEMY_DATABASE_URI"] = \
        "postgresql://{user}:{passwd}@{host}/{db}".format(
            user=main.config["POSTGRES_USER"],
            passwd=main.config["POSTGRES_PASSWD"],
            host=main.config["POSTGRES_HOST"],
            db=main.config["POSTGRES_DB"]
        )
    engine = create_engine(main.config["SQLALCHEMY_DATABASE_URI"])
    session = scoped_session(sessionmaker(bind=engine))
    Base.session = session

    main.register_blueprint(endpoint.api)

    return main


if __name__ == '__main__':
    app = make_app()
    app.run(port=app.config["PORT"])
