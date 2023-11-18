import timeit

def check_time(func):
    def _inner_func(*args, **kwargs):
        print(f"Затраченное время на {func.__name__}:", 
              timeit.timeit(lambda: func(*args, **kwargs),number=1))
    return _inner_func