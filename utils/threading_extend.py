from typing import Any, Callable, Iterable, Mapping, TypeVar
from threading import Thread

T = TypeVar('T')


class ThreadResult(Thread):
    result: T
    def __init__(self, group: None = None, target: Callable[..., T] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = {}, *, daemon: bool | None = None) -> None:
        target = self.wrap_func(target)
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
    def wrap_func(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs):
            self.result = func(*args, **kwargs)
            return self.result
        return wrapper
    def join(self, timeout: float | None = None) -> T:
        super().join(timeout)
        return self.result

def startall(threads: Iterable[ThreadResult]):
    for thread in threads:
        thread.start()
    return [thread.join() for thread in threads]