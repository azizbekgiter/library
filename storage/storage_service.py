from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def save(self, instance):
        pass

    @abstractmethod
    def retrieve(self, model, **kwargs):
        pass

    @abstractmethod
    def update(self, instance, **kwargs):
        pass

    @abstractmethod
    def delete(self, instance):
        pass


class DatabaseStorageService(StorageService):
    def save(self, instance):
        instance.save()
        return instance

    def retrieve(self, model, **kwargs):
        return model.objects.filter(**kwargs)

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
