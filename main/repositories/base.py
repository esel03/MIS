from dataclasses import dataclass


@dataclass
class RepositoryBase:
    def get_info(self, model, **kwargs):
        """
        Возвращает запись из модели
        """
        return model.objects.get(**kwargs)
