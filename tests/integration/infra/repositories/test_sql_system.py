from app.domain.models.system import Counter, CounterName
from app.external.adapters.repositories import SQLCounterRepository


class TestLifecycle:
    def test_create(self, counter_repository: SQLCounterRepository):
        counter = Counter(name=CounterName.product_sku_counter, current_value=0)
        saved_counter = counter_repository.save(counter)
        counter_repository.session.commit()

        assert saved_counter.name == CounterName.product_sku_counter
        assert saved_counter.current_value == 0

    def test_read(self, counter_repository: SQLCounterRepository):
        counter = counter_repository.find_by_name(CounterName.product_sku_counter)

        assert counter is not None
        assert counter.name == CounterName.product_sku_counter
        assert counter.current_value == 0

    def test_delete(self, counter_repository: SQLCounterRepository):
        counter = counter_repository.find_by_name(CounterName.product_sku_counter)

        counter_repository.delete(counter)
        counter_repository.session.commit()

        deleted_counter = counter_repository.find_by_name(CounterName.product_sku_counter)

        assert deleted_counter is None


class TestUpdateCases:
    UPDATE_VALUE = 100

    def test_update_counter_value(self, counter_repository: SQLCounterRepository):
        counter = Counter(name=CounterName.product_sku_counter, current_value=0)
        counter_repository.save(counter)
        counter_repository.session.commit()

        found_counter = counter_repository.find_by_name(CounterName.product_sku_counter)
        found_counter.current_value = self.UPDATE_VALUE
        updated_counter = counter_repository.save(found_counter)
        counter_repository.session.commit()

        assert updated_counter.current_value == self.UPDATE_VALUE

        refetched_counter = counter_repository.find_by_name(CounterName.product_sku_counter)

        assert refetched_counter.current_value == self.UPDATE_VALUE

    def test_find_by_name_for_update(self, counter_repository: SQLCounterRepository):
        locked_counter = counter_repository.find_by_name_for_update(CounterName.product_sku_counter)

        assert locked_counter is not None
        assert locked_counter.name == CounterName.product_sku_counter
        assert locked_counter.current_value == self.UPDATE_VALUE

        locked_counter.current_value += 1
        counter_repository.save(locked_counter)
        counter_repository.session.commit()

        updated_counter = counter_repository.find_by_name(CounterName.product_sku_counter)

        assert updated_counter is not None
        assert updated_counter.current_value == self.UPDATE_VALUE + 1

    def test_multiple_updates(self, counter_repository: SQLCounterRepository):
        initial_counter_value = counter_repository.find_by_name(
            CounterName.product_sku_counter
        ).current_value
        for n in range(1, 5):
            locked_counter = counter_repository.find_by_name_for_update(
                CounterName.product_sku_counter
            )
            locked_counter.current_value += 1
            updated_counter = counter_repository.save(locked_counter)
            counter_repository.session.commit()
            assert updated_counter.current_value == initial_counter_value + n

    # def test_update_locked_counter_fails(self, counter_repository: SQLCounterRepository):
    #     counter = counter_repository.find_by_name_for_update(CounterName.product_sku_counter)
    #     second_engine = create_engine(url=str(counter_repository.session.bind.url))
    #     second_session = sessionmaker(
    #         autocommit=False, autoflush=False, bind=second_engine, class_=Session
    #     )
    #     second_repository = SQLCounterRepository(second_session())
    #     second_counter = second_repository.find_by_name_for_update(CounterName.product_sku_counter)
