# Feature Toggles

This repo provides functionality for feature toggles in python code.


## What does this package do?

1. It allows to access the configured toggles like `toggles.feature1`
2. It logs all uses of the toggle
3. It logs a warning when toggles have exceeded their maximum lifetime

## How to use

The toggles are configured in yaml and instantiated using:

```python
from featuretoggles import TogglesList

class ReleaseToggles(TogglesList):
    feature1: bool
    feature2: bool


toggles = ReleaseToggles('toggles.yaml')
```

The toggle can be used to gate particular bits of code like this:

```python
if toggles.feature1:
    print("Feature One Activated")
else:
    print("Feature One Deactivated")
```

See [demo](demo/demo.py) for a working example
