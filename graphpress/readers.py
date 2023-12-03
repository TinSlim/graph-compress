import gzip
from abc import ABC, abstractmethod

class AbstractReader():
    """Abstract class for readers."""
    def __init__(self, filename: str):
        self.filename = filename
        self.check_file_extension()

    @abstractmethod
    def check_file_extension(self) -> None:
        """Checks if the file extension is supported."""
        raise NotImplementedError

    @abstractmethod
    def readline(self) -> str:
        """Reads a line from the file."""
        raise NotImplementedError

class Reader_NT(AbstractReader):
    """Reads a .nt file line by line."""

    def check_file_extension(self) -> None:
        if not self.filename.endswith('.nt'):
            raise ValueError('File extension not supported.')    
    
    def readline(self) -> str:
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                yield line.rstrip()

class Reader_NTgz(AbstractReader):
    """Reads a .nt.gz file line by line."""

    def check_file_extension(self) -> None:
        if not self.filename.endswith('.nt.gz'):
            raise ValueError('File extension not supported.')

    def readline(self) -> str:
        with gzip.open(self.filename,'r') as f:
            for line in f:
                yield line.decode().rstrip()

class Reader_CGgz(AbstractReader):
    """Reads a compressed graph (.gz file) line by line."""

    def check_file_extension(self) -> None:
        if not self.filename.endswith('.gz'):
            raise ValueError('File extension not supported.')

    def readline(self) -> str:
        with gzip.open(self.filename,'r') as f:
            for line in f:
                yield line.decode().rstrip()
