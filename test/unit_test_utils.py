class TrueOnNthIteration:
    """Iterable that returns False until Nth iteration, then it returns True."""

    def __init__(self, n):
        """Set the iteration to return True on."""
        self.n = n

    def __iter__(self):
        self.current = 1
        return self

    def __next__(self):
        if self.current > self.n:
            raise StopIteration
        elif self.current == self.n:
            result = True
        else:
            result = False

        self.current += 1

        return result


class BooleanToggle:
    """Iterable that returns a toggling boolean."""

    def __init__(self, initial_value):
        """Set the initial state (i.e. False or True)."""
        self.initial_value = initial_value

    def __iter__(self):
        self.current = self.initial_value
        return self

    def __next__(self):
        result = self.current
        self.current = not self.current

        return result
