import hashlib

from common import print_results, readline


INPUT = readline(__file__)
ZEROS = 5

def compute_ids():
    id_1 = []
    id_2 = list(8 * '_')
    nextPart = get_next_part()
    while '_' in id_2:
        position, value = nextPart.__next__()
        id_1.append(position)
        try:
            if id_2[int(position)] == '_':
                id_2[int(position)] = value
        except:
            pass
    return ''.join(id_1[:8]), ''.join(id_2)

def get_next_part():
    suffix = 0
    while True:
        md5 = hashlib.md5(str.encode(INPUT + str(suffix))).hexdigest()
        if md5.startswith('0' * ZEROS):
            yield md5[5], md5[6]
        suffix += 1

#### Main part.

print_results(*compute_ids())
