from abc import ABC, abstractmethod

from django.db import models


class BaseRepository(ABC):

    @property
    @abstractmethod
    def model(self) -> models.Model:
        pass

    def create(self, use_get_or_create=True, *args, **kwargs) -> models.Model:
        if use_get_or_create:
            return self.model.objects.get_or_create(**kwargs)
        else:
            return self.model.objects.create(**kwargs)
