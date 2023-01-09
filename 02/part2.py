INPUT_FILE = r'input_file.txt'


def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')


def get_opponent_action(opponent_key):
    opponent_key = opponent_key.upper()
    opponent_action = {
        'A':'ROCK',
        'B':'PAPER',
        'C':'SCISSOR',
    }
    return opponent_action[opponent_key]


def get_own_action(own_key, opponent_action):
    own_key = own_key.upper()
    own_action = {
        'X':get_lose_response_action,
        'Y':get_draw_response_action,
        'Z':get_win_response_action,
    }
    return own_action[own_key](opponent_action)


def is_draw(opponent_action, own_action):
    if opponent_action == own_action:
        return True
    return False


def is_win(opponent_action, own_action):
    if opponent_action=='ROCK' and own_action=='PAPER':
        return True
    if opponent_action=='PAPER' and own_action=='SCISSOR':
        return True
    if opponent_action=='SCISSOR' and own_action=='ROCK':
        return True
    return False


def get_draw_response_action(action):
    result = {
        'ROCK':'ROCK',
        'PAPER':'PAPER',
        'SCISSOR':'SCISSOR',
    }
    return result[action]


def get_lose_response_action(action):
    result = {
        'ROCK':'SCISSOR',
        'PAPER':'ROCK',
        'SCISSOR':'PAPER',
    }
    return result[action]


def get_win_response_action(action):
    result = {
        'ROCK':'PAPER',
        'PAPER':'SCISSOR',
        'SCISSOR':'ROCK',
    }
    return result[action]


def get_result_score(opponent_key, own_key):
    opponent_action = get_opponent_action(opponent_key)
    own_action = get_own_action(own_key, opponent_action)
    additional_score = {
        'ROCK':1,
        'PAPER':2,
        'SCISSOR':3,
    }

    if is_draw(opponent_action, own_action):
        return 3 + additional_score[own_action]

    if is_win(opponent_action, own_action):
        return 6 + additional_score[own_action]
    
    return additional_score[own_action]


def main():
    total_score = 0

    for line in iterate_input_file_lines(INPUT_FILE):
        x = line.strip().split()
        total_score += get_result_score(x[0], x[1])
    
    print(total_score)


if __name__=='__main__':
    main()