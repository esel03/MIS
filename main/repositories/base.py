from dataclasses import dataclass


@dataclass
class RepositoryBase:
    """Базовый класс для работы с бд."""

# Блок записи в бд
    @staticmethod
    def record_one(model, **kwargs):
        """Запись одного экземпляры модели."""
        return model.objects.create(**kwargs)

    @staticmethod
    def record_many(model, data):
        """Запись многих экземпляров модели."""
        return model.objects.bulk_create([model(**kwargs) for kwargs in data])


# Блок обновления в бд
    @staticmethod
    def update_one(model, **kwargs):
        """Обновление одного экземпляра модели."""
        return model.objects.update(**kwargs)

    @staticmethod
    def update_many(model, data):
        """Обновление многих экземпляров модели."""
        return model.objects.bulk_update([model(**kwargs) for kwargs in data])


# Блок чтения из бд
    @staticmethod
    def get_one(model, pk):
        """Получение одного экземпляра модели."""
        return model.objects.get(pk = pk)

    @staticmethod
    def get_many(model, **kwargs):
        """Получение многих экземпляров модели."""
        return model.objects.filter(**kwargs)

    @staticmethod
    def get_all(model):
        """Получение всех экземпляров модели."""
        return model.objects.all()


# Блок check из бд
    # TODO: обобщить функции для email, id, phone
    @staticmethod
    def is_exists(model, field, value) -> bool:
        return model.objects.filter(field=value).exists()


# Блок удаления из бд
    @staticmethod
    def delete_one(model, pk):
        """Удаление одного экземпляра модели."""
        return model.objects.filter(pk = pk).update(is_delete = True)

    @staticmethod
    def delete_many(model, pk):
        """Удаление многих экземпляров модели."""
        # TODO: Реализовать выбор ряда юзеров для удаления
        return model.objects.filter(pk = pk).bulk_update(is_delete = True)

    @staticmethod
    def delete_all(model):
        """Удаление всех экземпляров модели."""
        # TODO: Реализовать удаление всех сразу без перечисления, нужно ли?
        return model.objects.all().bulk_update(is_delete = True)