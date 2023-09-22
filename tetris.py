import socket
'''FIT THE BRICK'''

board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def column_clear(x, y):

    if x > 9 or x < 0 or y > 19 or y < 0:
        return False

    for row in range(y + 1):
        row = y - row
        if board[row][x] != 0:
            return False

    return True


def convert_move(rot, move, start):
    delt = start - move
    # print(f"move: {move} - start: {start}")
    if delt > 0:
        move = "l" * abs(delt)
    elif delt < 0:
        move = "r" * abs(delt)
    else:
        move = ""

    # move += rot + "\n"
    rot += move + "\n"
    move = rot
    # print(f"{move}")
    return move


class Line():
    up = '\n    O     \n    O     \n    O     \n    O     \n'
    left = '\n   OOOO   \n'

    def get_move(brick):
        u_move_y = 1000
        u_move_x = 1000
        l_move_y = 1000
        l_move_x = 1000

        done_u = False
        done_l = False

        #up
        for y, row in enumerate(board):
            if done_u:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y):
                        u_move_y = y
                        u_move_x = x
                        done_u = True
                        break

        #left
        for y, row in enumerate(board):
            if done_l:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y) and column_clear(x+2, y) and column_clear(x+3, y):
                        l_move_y = y
                        l_move_x = x
                        done_l = True
                        break

        if brick == Line.up:
            rot = 0
            start = 4
        elif brick == Line.left:
            rot = 1
            start = 3
        # print(u_move_x, l_move_x, sep=":")
        # print(u_move_y, l_move_y, sep=":")
        # print(*board, sep="\n")
        if u_move_y > l_move_y:
            # print(f"{u_move_y}:{l_move_y}")
            if rot == 1:
                return convert_move("q", u_move_x, start)
            else:
                return convert_move("", u_move_x, start)
        else:
            if rot == 0:
                return convert_move("q", l_move_x, start)
            else:
                return convert_move("", l_move_x, start)


class Square():
    up = '\n    88    \n    88    \n'

    def get_move(brick):
        move = -69

        for y, row in enumerate(board):
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y):
                        move = x
                        return convert_move("", move, 4)


def set_rotation(rot, desired):
    '''
    0 = up
    1 = left
    2 = down
    3 = right
    '''
    if rot - desired == 0:
        return ""

    if rot == 0:
        if desired == 1:
            return "q"
        elif desired == 2:
            return "qq"
        else:
            return "c"

    elif rot == 1:
        if desired == 2:
            return "q"
        elif desired == 3:
            return "qq"
        else:
            return "c"

    elif rot == 2:
        if desired == 3:
            return "q"
        elif desired == 0:
            return "qq"
        else:
            return "c"

    else:
        if desired == 0:
            return "q"
        elif desired == 1:
            return "qq"
        else:
            return "c"


class Tee():
    right = '\n    B     \n    BB    \n    B     \n'
    left = '\n     B    \n    BB    \n     B    \n'
    up = '\n    B     \n   BBB    \n'
    down = '\n   BBB    \n    B     \n'

    def get_move(brick):
        u_move_x = 1000
        u_move_y = 1000
        d_move_x = 1000
        d_move_y = 1000
        l_move_x = 1000
        l_move_y = 1000
        r_move_x = 1000
        r_move_y = 1000

        done_u = False
        done_d = False
        done_l = False
        done_r = False

        #up
        for y, row in enumerate(board):
            if done_u:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y) and column_clear(x+2, y):
                        u_move_x = x
                        u_move_y = y
                        done_u = True
                        break
        #down
        for y, row in enumerate(board):
            if done_d:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x-1, y-1) and column_clear(x+1, y-1):
                        d_move_x = x
                        d_move_y = y
                        done_d = True
                        break
        #left
        for y, row in enumerate(board):
            if done_l:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x-1, y-1):
                        l_move_x = x
                        l_move_y = y
                        done_l = True
                        break
        #right
        for y, row in enumerate(board):
            if done_r:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                x = (len(row) - 1) - x

                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y-1):
                        r_move_x = x
                        r_move_y = y
                        done_r = True
                        break

        if brick == Tee.up:
            rot = 0
            start = 3
        elif brick == Tee.left:
            rot = 1
            start = 5
        elif brick == Tee.down:
            rot = 2
            start = 4
        else:
            rot = 3
            start = 4
        # print(u_move_x, d_move_x, l_move_x, r_move_x, sep=":")
        # print(u_move_y, d_move_y, l_move_y, r_move_y, sep=":")
        if u_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            # print("up")
            if rot == 2 or rot == 1:
                start -= 1
            return convert_move(set_rotation(rot, 0), u_move_x, start)

        elif l_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            if rot == 3 or rot == 0:
                start += 1
            # print("left")
            return convert_move(set_rotation(rot, 1), l_move_x, start)
        elif r_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            if rot == 2 or rot == 1:
                start -= 1
            # print("right")
            return convert_move(set_rotation(rot, 3), r_move_x, start)
        else:
            if rot == 3 or rot == 0:
                start += 1
            # print("down")
            return convert_move(set_rotation(rot, 2), d_move_x, start)


class rEl():
    up = '\n    %     \n    %     \n    %%    \n'
    down = '\n    %%    \n     %    \n     %    \n'
    left = '\n     %    \n   %%%    \n'
    right = '\n   %%%    \n   %      \n'

    def get_move(brick):
        # return
        u_move_x = 1000
        u_move_y = 1000
        d_move_x = 1000
        d_move_y = 1000
        l_move_x = 1000
        l_move_y = 1000
        r_move_x = 1000
        r_move_y = 1000

        done_u = False
        done_d = False
        done_l = False
        done_r = False

        #up
        for y, row in enumerate(board):
            if done_u:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y):
                        u_move_x = x
                        u_move_y = y
                        done_u = True
                        break

        #down
        for y, row in enumerate(board):
            if done_d:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x-1, y-2):
                        d_move_x = x
                        d_move_y = y
                        done_d = True
                        break

        #left
        for y, row in enumerate(board):
            if done_l:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y) and column_clear(x+2, y):
                        l_move_x = x
                        l_move_y = y
                        done_l = True
                        break

        #right
        for y, row in enumerate(board):
            if done_r:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                x = (len(row) - 1) - x

                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y-1) and column_clear(x+2, y-1):
                        r_move_x = x
                        r_move_y = y
                        done_r = True
                        break

        if brick == rEl.up:
            rot = 0
            start = 4
        elif brick == rEl.left:
            rot = 1
            start = 3
        elif brick == rEl.down:
            rot = 2
            start = 5
        else:
            rot = 3
            start = 3
        # print(u_move_x, d_move_x, l_move_x, r_move_x, sep=":")
        # print(u_move_y, d_move_y, l_move_y, r_move_y, sep=":")

        if l_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            # print("left")
            if rot == 2:
                start -= 1
            return convert_move(set_rotation(rot, 1), l_move_x, start)
        elif r_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            # print("right")
            if rot == 2:
                start -= 1
            return convert_move(set_rotation(rot, 3), r_move_x, start)
        elif u_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            if rot == 2:
                start -= 1
            # print("up")
            return convert_move(set_rotation(rot, 0), u_move_x, start)
        else:
            # print("down")
            if rot == 1 or rot == 3:
                start = 4
            if rot == 0:
                start += 1
            return convert_move(set_rotation(rot, 2), d_move_x, start)


class lEl():
    right = '\n   0      \n   000    \n'
    up = '\n     0    \n     0    \n    00    \n'
    left = '\n   000    \n     0    \n'
    down = '\n    00    \n    0     \n    0     \n'

    def get_move(brick):
        # return
        u_move_x = 1000
        u_move_y = 1000
        d_move_x = 1000
        d_move_y = 1000
        l_move_x = 1000
        l_move_y = 1000
        r_move_x = 1000
        r_move_y = 1000

        done_u = False
        done_d = False
        done_l = False
        done_r = False

        #up
        for y, row in enumerate(board):
            if done_u:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y):
                        u_move_x = x
                        u_move_y = y
                        done_u = True
                        break

        #down
        for y, row in enumerate(board):
            if done_d:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                x = (len(row) - 1) - x
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y-2):
                        d_move_x = x
                        d_move_y = y
                        done_d = True
                        break

        #left
        for y, row in enumerate(board):
            if done_l:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x-1, y-1) and column_clear(x+-2, y-1):
                        l_move_x = x
                        l_move_y = y
                        done_l = True
                        break

        #right
        for y, row in enumerate(board):
            if done_r:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y) and column_clear(x+2, y):
                        r_move_x = x
                        r_move_y = y
                        done_r = True
                        break

        if brick == lEl.up:
            rot = 0
            start = 4
        elif brick == lEl.left:
            rot = 1
            start = 5
        elif brick == lEl.down:
            rot = 2
            start = 4
        else:
            rot = 3
            start = 3
        # print(u_move_x, d_move_x, l_move_x, r_move_x, sep= ":")
        # print(u_move_y, d_move_y, l_move_y, r_move_y, sep=":")

        if r_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            if rot == 1:
                start -= 2
            # print(f"right:{rot}")
            return convert_move(set_rotation(rot, 3), r_move_x, start)
        elif l_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            if rot == 2 or rot == 3 or rot == 0:
                start += 2
            # print("left")
            return convert_move(set_rotation(rot, 1), l_move_x, start)
        elif u_move_y == max(u_move_y, d_move_y, l_move_y, r_move_y):
            if rot == 1:
                start -= 2
            # print("up")
            return convert_move(set_rotation(rot, 0), u_move_x, start)
        else:
            if rot == 1:
                start -= 2
            # print("down")
            return convert_move(set_rotation(rot, 2), d_move_x, start)


class lZe():

    left = '\n    QQ    \n   QQ     \n'
    up = '\n    Q     \n    QQ    \n     Q    \n'

    def get_move(brick):
        # return
        u_move_y = 1000
        u_move_x = 1000
        l_move_y = 1000
        l_move_x = 1000

        done_u = False
        done_l = False

        #up
        for y, row in enumerate(board):
            if done_u:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x-1, y-1):
                        u_move_y = y
                        u_move_x = x
                        done_u = True
                        break

        #left
        for y, row in enumerate(board):
            if done_l:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                x = (len(row) - 1) - x
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y) and column_clear(x+2, y-1):
                        l_move_y = y
                        l_move_x = x
                        done_l = True
                        break

        if brick == lZe.up:
            rot = 0
            start = 5
        elif brick == lZe.left:
            rot = 1
            start = 3
        else:
            raise IndexError
        # print(u_move_x, l_move_x, sep=":")
        # print(u_move_y, l_move_y, sep=":")
        if l_move_y >= u_move_y:
            # print("left")
            if rot == 0:
                start -= 1
                return convert_move("c", l_move_x, start)
            else:
                return convert_move("", l_move_x, start)
        else:

            # print("up")
            if rot == 1:
                start += 1
                return convert_move("c", u_move_x, start)
            else:
                return convert_move("", u_move_x, start)


class rZe():
    left = '\n   XX     \n    XX    \n'
    up = '\n     X    \n    XX    \n    X     \n'

    def get_move(brick):
        # return
        u_move_y = 1000
        u_move_x = 1000
        l_move_y = 1000
        l_move_x = 1000

        done_u = False
        done_l = False

        #up
        for y, row in enumerate(board):
            if done_u:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                x = (len(row) - 1) - x
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y-1):
                        u_move_y = y
                        u_move_x = x
                        done_u = True
                        break

        #left
        for y, row in enumerate(board):
            if done_l:
                break
            y = (len(board) - 1) - y
            for x, cell in enumerate(row):
                if board[y][x] == 0:
                    if column_clear(x, y) and column_clear(x+1, y) and column_clear(x-1, y-1):
                        l_move_y = y
                        l_move_x = x
                        done_l = True
                        break

        if brick == rZe.up:
            rot = 0
            start = 4
        elif brick == rZe.left:
            rot = 1
            start = 4

        # print(u_move_x, l_move_x, sep=":")
        # print(u_move_y, l_move_y, sep=":")
        # print(*board, sep="\n")

        if l_move_y >= u_move_y:
            # print("left")
            if rot == 0:
                start += 1
                return convert_move("c", l_move_x, start)
            else:
                return convert_move("", l_move_x, start)
        else:
            # print("up")
            if rot == 1:
                start -= 1
                return convert_move("c", u_move_x, start)
            else:
                return convert_move("", u_move_x, start)


def get_brick(data: str) -> str:
    brick = ""
    start = data.index("/15")
    start += 3
    end = data.index("----------")
    for c in data[start:end]:
        brick += c

    return brick


def count_line(line: str) -> int:
    count = 0
    for c in line:
        if c != " ":
            count += 1
    return count


def what_brick(data: str):
    brick = get_brick(data)
    return brick
    game = Game()


def get_state(data: str):
    one = "9\n----------"
    two = "--"
    start = data.index(one)
    start += len(one) + 1
    end = data.index(two, start)
    temp_board = data[start:end].split("\n")[:20]
    for x, row in enumerate(board):
        for y, _ in enumerate(row):
            if temp_board[x][y] != " ":
                board[x][y] = 1


def reset_board():
    for i, row in enumerate(board):
        board[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def play():
    bricks = {
        "%": rEl,
        "0": lEl,
        "Q": lZe,
        "X": rZe,
        "8": Square,
        "B": Tee,
        "O": Line
    }

    # completed = ["8", "O", "B", "*"]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("pyctf.class.net", 8086))
    old = ""
    while(1):

        data = sock.recv(1024)
        data = data.decode()

        if "over" in data.lower():
            return old
            print("end")
            break
        old = data
        brick_data = what_brick(data)
        reset_board()
        get_state(data)
        # print(*board, sep="\n")

        for tile in bricks.keys():
            if tile in brick_data:
                brick = bricks[tile]
                break

        # print(brick_data)
        move = brick.get_move(brick_data)
        # print(data)
        if not move:
            return old
        sock.send(move.encode())
        # sleep(1)


def main():
    highscore = 0
    while(1):
        data = play()
        score = data.index("/")
        score = data[score-3:score]
        try:
            score = int(score)
        except:
            continue
        if score > highscore:
            highscore = score
            print(data)
            print(f"Yay! New High Score: {highscore}")
            input("Enter to coninue")


if __name__ == "__main__":
    main()
