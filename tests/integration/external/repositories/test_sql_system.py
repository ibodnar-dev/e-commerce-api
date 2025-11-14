from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from app.external.adapters.repositories import SQLCounterRepository
from app.external.db import default_engine


class TestSequenceBasedSKUGeneration:
    """Test PostgreSQL sequence-based SKU value generation."""

    def test_get_next_sku_value_returns_sequential_values(
        self, counter_repository: SQLCounterRepository
    ):
        """Test that get_next_sku_value returns incrementing values."""
        value1 = counter_repository.get_next_sku_value()
        value2 = counter_repository.get_next_sku_value()
        value3 = counter_repository.get_next_sku_value()

        assert value2 == value1 + 1
        assert value3 == value2 + 1

    def test_get_next_sku_value_is_unique_across_sessions(
        self, counter_repository: SQLCounterRepository
    ):
        """Test that multiple sessions get unique sequential values without conflicts."""
        # First session gets a value
        value1 = counter_repository.get_next_sku_value()

        # Second session with different repository
        second_session = sessionmaker(autoflush=False, bind=default_engine, class_=Session)()
        second_repository = SQLCounterRepository(second_session)
        value2 = second_repository.get_next_sku_value()

        # Third session
        third_session = sessionmaker(autoflush=False, bind=default_engine, class_=Session)()
        third_repository = SQLCounterRepository(third_session)
        value3 = third_repository.get_next_sku_value()

        # All values should be unique and sequential
        assert value2 == value1 + 1
        assert value3 == value2 + 1

        # Cleanup
        second_session.close()
        third_session.close()

    def test_concurrent_sku_generation_no_duplicates(self):
        """Test that concurrent SKU generation produces no duplicates."""
        # Simulate concurrent access with multiple repositories
        sessions = []
        repositories = []
        for _ in range(5):
            session = sessionmaker(autoflush=False, bind=default_engine, class_=Session)()
            sessions.append(session)
            repositories.append(SQLCounterRepository(session))

        # Generate values concurrently (within same transaction context)
        values = [repo.get_next_sku_value() for repo in repositories]

        # All values should be unique
        assert len(values) == len(set(values)), "Found duplicate SKU values!"

        # Values should be sequential
        sorted_values = sorted(values)
        for i in range(len(sorted_values) - 1):
            assert sorted_values[i + 1] == sorted_values[i] + 1

        # Cleanup
        for session in sessions:
            session.close()

    def test_get_next_sku_value_works_after_rollback(
        self, counter_repository: SQLCounterRepository
    ):
        """Test that sequence continues after transaction rollback (creates gaps)."""
        value1 = counter_repository.get_next_sku_value()
        counter_repository.session.rollback()

        # After rollback, sequence should still increment (creating a gap)
        value2 = counter_repository.get_next_sku_value()

        # value2 might not be value1 + 1 due to the rollback gap
        # but it should still be a valid value
        assert value2 > value1
