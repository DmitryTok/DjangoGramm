from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @property
    @abstractmethod
    def model(self):
        pass

    def create(self, use_get_or_create=True, *args, **kwargs):
        if use_get_or_create:
            return self.model.objects.get_or_create(**kwargs)
        else:
            return self.model.objects.create(**kwargs)
