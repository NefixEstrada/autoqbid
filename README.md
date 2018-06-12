# AutoQbid
AutoQbid is a tool that automatizes the time insertion into Qbid





## Example:

```python
from autoqbid import AutoQbid

qbid = AutoQbid(browser="Chrome")
qbid.login("username", "password")

form_data = [
    ["8217", "4.0"]
]
qbid.fill_day("2018/5/19", form_data)
```

If you want more examples, check out `autoqbid_example.py`



## Tecnologies used:

- Python3
- Selenium
- Tabulate

