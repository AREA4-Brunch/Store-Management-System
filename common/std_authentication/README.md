Features offered by `AuthenticationService`, even its staticmethods,
as well as the decorators from `./decorators.py` rely on the `AuthenticationService`
object being created, hence initialized, only then will those features be usable.

Distributed as source distribution: ```python setup.py sdist```

Distributed as binary distribution: ```python setup.py bdist_wheel```

To pip install source distribution or add path to file in requirements.txt:
``` cmd
    pip install std-authentication-0.1.0.tar.gz
```

To pip install binary distribution or add path to file in requirements.txt:
``` cmd
    pip install std-authentication-0.1.0-py3-none-any.whl
```
