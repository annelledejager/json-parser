# Json parser

Given an input as json array (each element is a flat dictionary) write a program that will parse this json, and return a
nested dictionary of dictionaries of arrays, with keys specified in command line arguments and the leaf values as arrays
of flat dictionaries matching appropriate groups.

E.g run the following command from project directory.
```
>>> cat input.json | python nest.py currency country city
```

## Additions

A Django application is created to accept the input json array and return the nested dictionary of dictionaries of 
arrays. The application runs using the Docker Compose tool. Using a single command, one can create and start the service
from the configuration file. No need to setup the virtualenv etc.

To start the Django application run the following commands from project directory.
```
>>> docker-compose -f docker-compose.yml build
>>> docker-compose -f docker-compose.yml up
```

The application is a backend application with a POST endpoint '/api/v1/parse-json/'. My suggestion is to use E.g Postman
to query the endpoint. Basic authentication applies with username - user and password - pass.

django-auth-wall is used for basic authentication. Its a very basic Basic Auth middleware that uses a username/password
defined in settings.py to protect the whole site (https://github.com/theskumar/django-auth-wall).

The content type is application/json. The required fields are args and json_input.
E.g
```
{
"args": ["country", "city"],
"json_input":
[
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  }
]
}
```

## Testing

To run the tests, run the following commands in root directory.
```
>>> docker-compose -f docker-compose.test.yml build
>>> docker-compose -f docker-compose.test.yml up
```

```
test_1  | Name                              Stmts   Miss  Cover   Missing
test_1  | ---------------------------------------------------------------
test_1  | json_parser                               0      0   100%
test_1  | json_parser.api                          21      0   100%
test_1  | json_parser.serializers                   0      0   100%
test_1  | json_parser.serializers.json_parser       4      0   100%
test_1  | json_parser.settings                     24     24     0%   14-123
test_1  | json_parser.urls                          4      0   100%
test_1  | json_parser.views                         0      0   100%
test_1  | json_parser.views.json_parser            36      0   100%
test_1  | ---------------------------------------------------------------
test_1  | TOTAL                                89     24    73%
test_1  | ----------------------------------------------------------------------
```

## Improvements

- I am definitely not a postgres expert. If I had more time, I would have liked to focus more on the SQL section to
  improve my query for #1 as well as to implement #2 and #3 of the section.

- Improvements to the REST service includes reading/writing to/from the DB. Currently no queries are saved can can
  therefore not be retrieved. I would have liked to extend the endpoint to include a GET request.

- If I had more time, I would have liked to implement a less temporary Basic authentication which uses the Django auth.
  The current solution is handy for quickly securing an entire site during development and should only be used during
  development and testing.

- Further improvements include adding configuration files for local, preprod and production environments to store the
  basic auth username and password per environment. The values will then be read during service start time according to
  the environment.
