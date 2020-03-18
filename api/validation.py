sign_up_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'format': 'email', 'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'amount': {'type': 'number'},
        'currency': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'amount', 'currency', 'password'],
    'additionalProperties': False
}

sign_in_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'format': 'email',
                  'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password'],
    'additionalProperties': False
}

transfer_schema = {
    'type': 'object',
    'properties': {
        'targetEmail': {'type': 'string', 'format': 'email',
                        'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'amount': {'type': 'number'}
    },
    'required': ['targetEmail', 'amount'],
    'additionalProperties': False
}
