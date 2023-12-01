import base64


def break_file(filepath, chunk_size):

    with open(filepath, 'rb') as file:
        content = file.read()
        i = 0
        parts = []
        while True:
            part = b''
            if i + chunk_size >= len(content):
                part = content[i:]
                part = base64.b64encode(part).decode('utf-8')
                parts.append(part)
                break
            else:
                part = content[i:i+chunk_size]
                part = base64.b64encode(part).decode('utf-8')
            parts.append(part)
            i += chunk_size
        return parts


# Send byte string, to covnert utf-8 to string use utf8_str.encode('utf-8')
def stitch_file(file_parts):
    x = b''
    for part in file_parts:
        x += base64.b64decode(part.encode('utf-8'))
    return x


