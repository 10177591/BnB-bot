import json
from collections import namedtuple

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

# Parse JSON into an object with attributes corresponding to dict keys.
print data.keys
x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
print x.name, x.hometown.name, x.hometown.id
