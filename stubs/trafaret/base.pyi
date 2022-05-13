from typing import Any as _Any, Hashable, Optional, NoReturn

from trafaret.dataerror import DataError


class TrafaretMeta(type):
    def __or__(cls, other): ...
    def __and__(cls, other): ...
    def __rshift__(cls, other): ...

class Trafaret(metaclass=TrafaretMeta):
    def check(self, value: _Any, context: Optional[_Any] = ...) -> _Any: ...
    def _failure(self, error: str = None, value: _Any = ...) -> NoReturn: ...
    def append(self, other): ...
    def __or__(self, other): ...
    def __and__(self, other): ...
    def __rshift__(self, other): ...
    def __call__(self, val, context=None): ...

class Key:
    def __init__(self, name: Hashable,
                 default: _Any = ...,
                 optional: bool = False,
                 to_name: Hashable = None,
                 trafaret: Trafaret = None) -> None: ...
    def get_name(self) -> Hashable: ...
    ...

def ensure_trafaret(trafaret): ...

class TypeMeta(TrafaretMeta):
    def __getitem__(self, type_): ...

class SquareBracketsMeta(TrafaretMeta):
    def __getitem__(self, args): ...

class OnError(Trafaret):
    def __init__(self, trafaret: Trafaret, message: str, code: str = None) -> None: ...
    def transform(self, value: _Any, context: _Any = None): ...
class WithRepr(Trafaret): ...

class TypingTrafaret(Trafaret, metaclass=TypeMeta): ...
class Subclass(TypingTrafaret): ...
class Type(TypingTrafaret): ...

class Any(Trafaret): ...
class And(Trafaret): ...
class Or(Trafaret): ...

class Dict(Trafaret):
    def __init__(self, *args, **trafarets) -> None: ...
    def allow_extra(self, *names: str, **kw) -> Dict: ...
    def ignore_extra(self, *names: str) -> Dict: ...
    def merge(self, other: Dict | list | tuple | dict) -> Dict: ...
class DictKeys(Trafaret): ...
class Mapping(Trafaret):
    def __init__(self, key, value) -> None: ...
class Enum(Trafaret):
    def __init__(self, *variants) -> None: ...
class Callable(Trafaret): ...
class Call(Trafaret):
    def __init__(self, fn) -> None: ...
class Forward(Trafaret): ...
class List(Trafaret, metclass=SquareBracketsMeta):
    def __init__(self, trafaret: Trafaret,
                 min_length: int = 0, max_length: int = None) -> None: ...
class Iterable(Trafaret):
    def __init__(self, trafaret: Trafaret,
                 min_length: int = 0, max_length: int = None) -> None: ...
class Tuple(Trafaret):
    def __init__(self, *args): ...
class Atom(Trafaret):
    def __init__(self, value: str) -> None: ...
class String(Trafaret):
    def __init__(self, allow_blank: bool = False,
                 min_length: int = None, max_length: int = None): ...
class Bytes(Trafaret): ...
class FromBytes(Trafaret):
    def __init__(self, encoding: str = 'utf-8') -> None: ...
class Null(Trafaret): ...
class Bool(Trafaret): ...
class ToBool(Trafaret): ...

class Date(Trafaret): ...
class ToDate(Trafaret): ...
class DateTime(Trafaret): ...
class ToDateTime(Trafaret): ...

def guard(trafaret: Trafaret = None, **kwargs): ...
def ignore(val): ...
def catch(checker, *a, **kw): ...
def extract_error(checker, *a, **kw): ...

class GuardError(DataError): ...
