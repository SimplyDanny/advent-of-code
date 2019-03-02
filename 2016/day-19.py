from common import print_results, readline


NUMBER_ELVES = int(readline(__file__))

def get_winner_of_game_1():
    number_participants = 1
    winner = 1
    while number_participants < NUMBER_ELVES:
        number_participants += 1
        winner = winner + 2 if winner + 2 <= number_participants else 1
    return winner

def get_winner_of_game_2():
    participants = list(range(1, NUMBER_ELVES + 1))
    turn = 0
    number_participants = NUMBER_ELVES
    while number_participants > 1:
        elf_to_kick = (int(number_participants/2) + turn) % number_participants
        del participants[elf_to_kick]
        number_participants = len(participants)
        turn = (turn if elf_to_kick < turn else turn + 1) % number_participants
    return participants[0]

#### Main part.

print_results(get_winner_of_game_1(), get_winner_of_game_2())
