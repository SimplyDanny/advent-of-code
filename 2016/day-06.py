from common import print_results, read


def get_message(function, messages):
    return ''.join(map(lambda x: function(x, key=x.count), messages))

#### Main part.

flipped_messages = list(zip(*read(__file__).split()))

print_results(
    get_message(max, flipped_messages),
    get_message(min, flipped_messages)
)
