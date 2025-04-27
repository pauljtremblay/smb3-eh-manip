import time
from typing import Dict, List

def timed(func_to_time):
    """Decorator used to time how long a task takes to execute."""
    def wrapper(*func_args, **func_kwargs):
        formatted_args = _format_arglist_kwargs(list(func_args), func_kwargs)
        start_ts = time.perf_counter_ns()
        try:
            result = func_to_time(*func_args, **func_kwargs)
            end_ts = time.perf_counter_ns()
            nanoseconds = end_ts - start_ts
            print(f"Function '{func_to_time.__name__}({formatted_args})' took {format_ns(nanoseconds)}")
            return result
        except Exception as ex:
            end_ts = time.perf_counter_ns()
            nanoseconds = end_ts - start_ts
            print(f"Function '{func_to_time.__name__}({formatted_args})' failed, took {format_ns(nanoseconds)}")
            raise ex
    return wrapper

def _format_arglist_kwargs(args: List[any], kwargs: Dict[str, any]) -> str:
    if len(args) == 0 and len(kwargs) == 0:
        return ""
    args_str = "" if len(args) == 0 else ",".join([str(arg) for arg in args])
    kwargs_str = ""
    if len(kwargs) > 0:
        kwarg_pairs = [f"{key}={value}" for (key, value) in kwargs.items()]
        kwargs_str = ",".join(kwarg_pairs)
    joiner = "" if args_str == "" or kwargs_str == "" else ","
    return joiner.join([args_str, kwargs_str])


def format_ns(nanos: int) -> str:
    millis = nanos / 1000000.0
    # most computer clocks do not provide better clock resolution than hundreds of ns
    return f"{millis:.4f} ms"