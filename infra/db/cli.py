from infra.db.connection import create_tables


def setup():
    print("Creating database tables...")
    create_tables()
    print("✓ Database tables created successfully!")
