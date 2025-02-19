https://pyyaml.org/wiki/PyYAMLDocumentation

| YAML tag                       | Python type                      |
| ------------------------------ | -------------------------------- |
| Standard YAML tags             |                                  |
| !!null                         | None                             |
| !!bool                         | bool                             |
| !!int                          | int or long (int in Python 3)    |
| !!float                        | float                            |
| !!binary                       | str (bytes in Python 3)          |
| !!timestamp                    | datetime.datetime                |
| !!omap, !!pairs                | list of pairs                    |
| !!set                          | set                              |
| !!str                          | str or unicode (str in Python 3) |
| !!seq                          | list                             |
| !!map                          | dict                             |
| Python-specific tags           |                                  |
| !!python/none                  | None                             |
| !!python/bool                  | bool                             |
| !!python/bytes                 | (bytes in Python 3)              |
| !!python/str                   | str (str in Python 3)            |
| !!python/unicode               | unicode (str in Python 3)        |
| !!python/int                   | int                              |
| !!python/long                  | long (int in Python 3)           |
| !!python/float                 | float                            |
| !!python/complex               | complex                          |
| !!python/list                  | list                             |
| !!python/tuple                 | tuple                            |
| !!python/dict                  | dict                             |
| Complex Python tags            |                                  |
| !!python/name:module.name      | module.name                      |
| !!python/module:package.module | package.module                   |
| !!python/object:module.cls     | module.cls instance              |
| !!python/object/new:module.cls | module.cls instance              |
| !!python/object/apply:module.f | value of f(...)                  |
