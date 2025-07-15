from flask import current_app, g
import sqlite3
from datetime import datetime
import click


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema_init.sql') as f:
        cmd = f.read().decode('utf8')
        db.executescript(cmd)
        click.echo(cmd)


def fill_db():
    db = get_db()

    with current_app.open_resource('schema_fill.sql') as f:
        cmd = f.read().decode('utf8')
        db.executescript(cmd)
        click.echo(cmd)

# Call: flask --app dvr_scan/ init-db
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('Initializing the database.')
    init_db()
    click.echo('Filling the database with data.')
    fill_db()
    click.echo('Database is ready.')


