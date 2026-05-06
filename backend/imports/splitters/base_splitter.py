from abc import ABC, abstractmethod
from langchain_core.documents import Document
from typing import Type, Dict


class BaseSplitter(ABC):
    registry: Dict[str, Type["BaseSplitter"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.get_name():
            BaseSplitter.registry[cls.get_name()] = cls

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_support_prompt(cls) -> str:
        pass

    @abstractmethod
    def split_documents(self, document: Document) -> list[Document]:
        pass
