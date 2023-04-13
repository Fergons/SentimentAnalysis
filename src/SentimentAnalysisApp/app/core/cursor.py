from datetime import datetime
import json
import base64
import struct


def encode_cursor(last_row=None):
    """
    Encode the given order_by fields into a hashed cursor string.
    :param last_row: A dictionary of last fetched row fields and respective values
    :return: A hashed cursor string.
    """
    name = last_row.get('name', '*')
    release_date = float(last_row.get('release_date', '-1.0'))
    score = float(last_row.get('score', '-1.0'))
    num_reviews = float(last_row.get('num_reviews', -1.0))
    id = int(last_row.get('id'))

    name_bytes = name.encode('utf-8')
    name_length = len(name_bytes)
    # Create a format string to handle the combination of data types
    fmt = f'I{name_length}sdddI'
    # Convert values into a compact binary format
    binary_data = struct.pack(fmt, name_length, name_bytes, release_date, score, num_reviews, id)
    # Encode the binary data using URL-safe Base64
    encoded_data = base64.urlsafe_b64encode(binary_data).rstrip(b'=')
    return encoded_data.decode('utf-8')


def decode_cursor(*, cursor):
    """
    Decode the given hashed cursor string into a list of last_row values to filter by
    if supplied filter and sort dictionariues doesn't match up with the encoded cursor values returns None.
    :param cursor: A hashed cursor string.
    :return: A dictionary of last fetched row fields and respective values
    """
    if cursor is None:
        return None
    # Decode the URL-safe Base64 encoded data
    padding = b'=' * (-len(cursor) % 4)
    binary_data = base64.urlsafe_b64decode(cursor.encode('utf-8') + padding)

    # Extract the length of the name_bytes
    name_length = struct.unpack('I', binary_data[:4])[0]

    # Create a format string to handle the combination of data types
    fmt = f'I{name_length}sdddI'

    # Convert the binary data back into the original values
    _, name_bytes, release_date, score, num_reviews, id = struct.unpack(fmt, binary_data)

    name = name_bytes.decode('utf-8')
    result = {
        'id': id
    }

    if name != '*':
        result['name'] = name
    if release_date != -1.0:
        result['release_date'] = datetime.fromtimestamp(release_date)
    if score != -1.0:
        result['score'] = score
    if num_reviews != -1.0:
        result['num_reviews'] = int(num_reviews)

    return result
