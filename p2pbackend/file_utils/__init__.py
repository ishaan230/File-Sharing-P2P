
def break_file(filepath, chunk_size):

    with open(filepath, 'rb') as file:
        content = file.read()
        i = 0
        parts = []
        while True:
            part = None
            if i + chunk_size >= len(content):
                part = content[i:]
                parts.append(part)
                break
            else:
                part = content[i:i+chunk_size]
            parts.append(part)
            i += chunk_size
        return parts


def stitch_file(file_parts):
    x = b''
    for part in file_parts:
        x += part
    print(x)
    return x
