def fun()->int:
    return 1

import typing
a = typing.cast(float, fun())

print(a)