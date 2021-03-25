import os, time

def find_paths(directory, suffix):
    """""

     Arguments:
         directory {str} -- taranmak istenen ust dizin
         suffix {str} -- taranan uzanti

     Returns:
        path_list {list} -- path list for suffix
    """
    if suffix.islower():
        suffix_u = suffix.upper()
    else:
        suffix_u = suffix.lower()

    if directory:
        path_list = []
        for root, subdirectory, files in os.walk(directory):
            for f in files:
                if f.endswith(suffix) or f.endswith(suffix_u):
                    path_list.append(os.path.join(root, f))

        return path_list
    else:
        return None


def timerfunc(func):
    """
    A timer decorator
    """

    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "\tThe runtime for {func} took {time} seconds to complete"
        print(msg.format(func=func.__name__,
                         time=runtime))
        return value

    return function_timer
