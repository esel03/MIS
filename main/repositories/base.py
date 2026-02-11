from dataclasses import dataclass


@dataclass
class RepositoryBase:
    """Базовый класс для работы с бд."""
# Блок записи в бд
    def record_one(self, model, **kwargs):
        """Запись одного экземпляры модели."""
        return model.objects.create(**kwargs)

    def record_many(self, model, data):
        """Запись многих экземпляров модели."""
        return model.objects.bulk_create([model(**kwargs) for kwargs in data])
        
# Блок обновления в бд
    def update_one(self, model, **kwargs):
        """Обновление одного экземпляра модели."""
        return model.objects.update(**kwargs)

    def update_many(self, model, data):
        """Обновление многих экземпляров модели."""
        return model.objects.bulk_update([model(**kwargs) for kwargs in data])
    
# Блок чтения из бд
    def get_one(self, model, **kwargs):
        """Получение одного экземпляра модели."""
        return model.objects.get(**kwargs)

    def get_many(self, model, **kwargs):
        """Получение многих экземпляров модели."""
        return model.objects.filter(**kwargs)

    def get_all(self, model):
        """Получение всех экземпляров модели."""
        return model.objects.all()
    
# Блок удаления из бд
    def delete_one(self, model, **kwargs):
        """Удаление одного экземпляра модели."""
        return model.objects.filter(**kwargs).delete()
    
    def delete_many(self, model, **kwargs):
        """Удаление многих экземпляров модели."""
        return model.objects.filter(**kwargs).delete()
    
    def delete_all(self, model):
        """Удаление всех экземпляров модели."""
        return model.objects.all().delete()