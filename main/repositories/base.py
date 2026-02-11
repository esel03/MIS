from dataclasses import dataclass


@dataclass
class RepositoryBase:
    """Базовый класс для бд."""
    def record_one(self, model, **kwargs):
        """Запись одного экземпляры модели."""
        return model.objects.create(**kwargs)

    def record_many(self, model, data):
        """Запись многих экземпляров модели."""
        return model.objects.bulk_create([model(**kwargs) for kwargs in data])
        

    def update_one(self, model, **kwargs):
        """Обновление одного экземпляра модели."""
        return model.objects.update(**kwargs)

    def update_many(self, model, data):
        """Обновление многих экземпляров модели."""
        return model.objects.bulk_update([model(**kwargs) for kwargs in data])
       
