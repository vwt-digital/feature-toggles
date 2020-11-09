# Feature Toggles

This repo provides functionality for feature toggles in python code.


## What does this package do?

1. It allows to access the configured toggles like `toggles.feature1`
2. It logs all uses of the toggle
3. It logs a warning when toggles have exceeded their maximum lifetime

## How to use

### Configure the toggles
The toggles are configured in yaml.
```yaml
feature1:
    value: true
    name: New Thing Toggler
    description: This toggles the new thing on
    jira: DAN-123
    creation_date: 2020-10-12
    max_lifetime: 14
```
Required fields:
* `value`: a boolean setting the value of the toggle
* `name`: a human readable name for the toggle
* `jira`: the JIRA ticket that this toggle is linked to.
* `creation_date`: the date this toggle is introduced.

Optional fields:
* `description`: A description of the purpose and use of the toggle
* `max_lifetime`: The number of days this toggle is supposed to be in the code. 
A warning will be logged when this lifetime is exceeded. The default is 14 days.


### Declare the toggles
To use the configured toggles they need to be declared in the code like this:

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

## Demo
See [demo](demo/main.py) for a working example
