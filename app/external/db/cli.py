from app.external.db.connection import create_tables, drop_tables


def db_setup():
    print("Creating database tables...")
    create_tables()
    print("✓ Database tables created successfully!")


def db_drop():
    print("Dropping database tables...")
    drop_tables()
    print("✓ Database tables dropped successfully!")
