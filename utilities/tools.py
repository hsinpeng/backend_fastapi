def parse_boolean(value):
    if value is None:
        return False
    return value.lower() in ('true', '1', 'yes', 'on')