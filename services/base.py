from abc import ABC, abstractmethod


class CRUDServiceBase(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def list(self, page=1, per_page=10, **kwargs):
        pass

    @abstractmethod
    def retrieve(self, pk, **kwargs):
        pass

    @abstractmethod
    def destroy(self, pk, **kwargs):
        pass

    @abstractmethod
    def update(self, pk, **kwargs):
        pass
