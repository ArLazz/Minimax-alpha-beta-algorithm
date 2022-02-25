from math import inf
from collections import Counter
import itertools
from time import time


def take_input(state, bm):
    aof = False
    if bm == -1 or len(posmov(bm)) > 9:
        aof = True
    if aof:
        print("Ставьте X куда хотите.")
    else:
        box_dict = {0: "Верхний левый", 1: "Верхний центральный", 2: "Верхний правый",
                    3: "Центральный левый", 4: "Центральный центральный", 5: "Центральный правый",
                    6: "Нижний Левый", 7: "Нижний центральный", 8: "Нижний правый"}
        print("Куда хотите поставить X в " + box_dict[bm % 9] + " квадрат?")
    x = int(input("Строка = "))
    if x == -1:
        raise SystemExit
    y = int(input("Столбец = "))
    print()
    if bm != -1 and index(x, y) not in posmov(bm):
        raise ValueError
    if not valid_input(state, (x, y)):
        raise ValueError
    return (x, y)


def output_tic_tac(state):
    for row in range(1, 10):
        row_str = ["|"]
        for col in range(1, 10):
            row_str += [state[index(row, col)]]
            if (col) % 3 == 0:
                row_str += ["|"]
        if (row - 1) % 3 == 0:
            print("-" * (len(row_str) * 2 - 1))
        print(" ".join(row_str))
    print("-" * (len(row_str) * 2 - 1))


def a_p(state, move, player):
    if not isinstance(move, int):
        move = index(move[0], move[1])
    return state[: move] + player + state[move + 1:]


def upd_won(state):
    temp_box_win = [" "] * 9
    for b in range(9):
        i_b = list(range(b * 9, b * 9 + 9))
        box_str = state[i_b[0]: i_b[-1] + 1]
        temp_box_win[b] = sm_box(box_str)
    return temp_box_win


def index(x, y):
    return (((x - 1) // 3) * 27) + (((x - 1) % 3) * 3) + (((y - 1) // 3) * 9) + ((y - 1) % 3)


def sm_box(box_str):
    global posgo
    for idxs in posgo:
        (x, y, z) = idxs
        if (box_str[x] == box_str[y] == box_str[z]) and box_str[x] != " ":
            return box_str[x]
    return " "


def posmov(last_move):
    global box_won
    if not isinstance(last_move, int):
        last_move = index(last_move[0], last_move[1])
    box_to_play = last_move % 9
    idxs = list(range(box_to_play * 9, box_to_play * 9 + 9))
    if box_won[box_to_play] != " ":
        pi_2d = [list(range(b * 9, b * 9 + 9)) for b in range(9) if box_won[b] == " "]
        pos_indic = list(itertools.chain.from_iterable(pi_2d))
    else:
        pos_indic = idxs
    return pos_indic


def succs(state, player, last_move):
    succ = []
    moves_idx = []
    pos_index = posmov(last_move)
    for idx in pos_index:
        if state[idx] == " ":
            moves_idx.append(idx)
            succ.append(a_p(state, idx, player))
    return zip(succ, moves_idx)


def out_succ(state, player, last_move):
    for st in succs(state, player, last_move):
        output_tic_tac(st[0])


def opp(p):
    return "O" if p == "X" else "X"


def eval_sm(box_str, player):
    global posgo
    score = 0
    three = Counter(player * 3)
    two = Counter(player * 2 + " ")
    one = Counter(player * 1 + " " * 2)
    three_opponent = Counter(opp(player) * 3)
    two_opponent = Counter(opp(player) * 2 + " ")
    one_opponent = Counter(opp(player) * 1 + " " * 2)
    for idxs in posgo:
        (x, y, z) = idxs
        current = Counter([box_str[x], box_str[y], box_str[z]])
        if current == three:
            score += 100
        elif current == two:
            score += 10
        elif current == one:
            score += 1
        elif current == three_opponent:
            score -= 100
            return score
        elif current == two_opponent:
            score -= 10
        elif current == one_opponent:
            score -= 1
    return score


def eval(state, last_move, player):
    global box_won
    score = 0
    score += eval_sm(box_won, player) * 200
    for b in range(9):
        idxs = list(range(b * 9, b * 9 + 9))
        box_str = state[idxs[0]: idxs[-1] + 1]
        score += eval_sm(box_str, player)
    return score


def minimax(state, last_move, player, depth, s_time):
    succ = succs(state, player, last_move)
    best_move = (-inf, None)
    for s in succ:
        val = min_turn(s[0], s[1], opp(player), depth - 1, s_time, -inf, inf)
        if val > best_move[0]:
            best_move = (val, s)
    return best_move[1]


def min_turn(state, last_move, player, depth, s_time, alpha, beta):
    global box_won
    if depth <= 0 or sm_box(box_won) != " ":
        return eval(state, last_move, opp(player))
    succ = succs(state, player, last_move)
    for s in succ:
        val = max_turn(s[0], s[1], opp(player), depth - 1, s_time, alpha, beta)
        if val < beta:
            beta = val
        if alpha >= beta:
            break
    return beta


def max_turn(state, last_move, player, depth, s_time, alpha, beta):
    global box_won
    if depth <= 0 or sm_box(box_won) != " ":
        return eval(state, last_move, player)
    succ = succs(state, player, last_move)
    for s in succ:
        val = min_turn(s[0], s[1], opp(player), depth - 1, s_time,
                       alpha, beta)
        if alpha < val:
            alpha = val
        if alpha >= beta:
            break
    return alpha


def valid_input(state, move):
    global box_won
    if not (0 < move[0] < 10 and 0 < move[1] < 10):
        return False
    if box_won[index(move[0], move[1]) // 9] != " ":
        return False
    if state[index(move[0], move[1])] != " ":
        return False
    return True


def game(state=" " * 81, depth=20):
    global box_won, posgo
    posgo = [(0, 4, 8), (2, 4, 6)]
    posgo += [(i, i + 3, i + 6) for i in range(3)]
    posgo += [(3 * i, 3 * i + 1, 3 * i + 2) for i in range(3)]
    box_won = upd_won(state)
    output_tic_tac(state)
    bm = -1
    while True:
        try:
            user_move = take_input(state, bm)
        except ValueError:
            print("Ошибка!")
            output_tic_tac(state)
            continue
        except SystemError:
            print("Игра остановлена!")
            break
        user_state = a_p(state, user_move, "X")
        output_tic_tac(user_state)
        box_won = upd_won(user_state)

        game_won = sm_box(box_won)
        if game_won != " ":
            state = user_state
            break
        print("Бот крутит шестеренки...")
        s_time = time()
        bot_state, bm = minimax(user_state, user_move, "O", depth, s_time)
        print("Бот поставил O в", bm, "позицию.")
        output_tic_tac(bot_state)
        state = bot_state
        box_won = upd_won(bot_state)
        game_won = sm_box(box_won)
        if game_won != " ":
            break
    if game_won == "X":
        print("Вы победили")
    else:
        print("Вы проиграли")
    return state


final_state = game(" " * 81, depth=5)
