from abc import ABC, abstractmethod


class AbstractFilesStorage(ABC):
    @abstractmethod
    async def put_file(self, file_name: str, content: bytes):
        raise NotImplementedError()

    @abstractmethod
    async def get_file(self, file_name: str) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    async def delete_file(self, file_name: str):
        raise NotImplementedError()
