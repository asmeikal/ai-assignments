import random
import sys

player = 'P'
wumpus = 'W'
pit    = '_'
gold   = 'G'

def get_input(s):
    if sys.version_info >= (3, 0):
        return input(s)
    else:
        return raw_input(s)

def inside_board(x, y, size):
    return x >= 0 and y >= 0 and x < size and y < size

def generate_board(size):
    res = []
    for i in range(size):
        res += [[None] * size]
    return res

def random_square(size):
    return (random.randint(0, size-1), random.randint(0, size-1))

def random_empty_square(board):
    i, j = random_square(len(board))
    while board[i][j] != None:
        i, j = random_square(len(board))
    return (i, j)

def place_character(board, char):
    i, j = random_empty_square(board)
    board[i][j] = char

def print_percepts(percepts):
    res = ""
    if percepts['exit']:
        res += "You see the exit of the cave. "
    if percepts['bump']:
        res += "You bump in the wall. "
    if percepts['stench']:
        res += "You smell a terrible stench. "
    if percepts['glitter']:
        res += "You see something glittering. "
    if percepts['breeze']:
        res += "You feel a breeze on your face. "
    if percepts['scream']:
        res += "You hear a terrible scream. "
    if res == "":
        res = "You feel nothing. "
    return res

def print_orientation(o):
    x, y = o
    if x == 1:
        res = "south"
    elif x == -1:
        res = "north"
    elif y == 1:
        res = "east"
    else:
        res = "west"
    return res

def turn_right(o):
    x, y = o
    if abs(x) > 0:
        return (y, -x)
    else:
        return (y, x)

def turn_left(o):
    x, y = o
    if abs(x) > 0:
        return (y, x)
    else:
        return (-y, x)


class WumpusWorld(object):
    def __init__(self):
        self.percepts = {
            'exit': False,
            'bump': False,
            'stench': False,
            'glitter': False,
            'breeze': False,
            'scream': False,
        }
        self.size = 4
        self.board = generate_board(self.size)
        self.board[0][0] = player
        self.points = 0
        self.finished = False
        self.fired_arrow = False
        self.player_pos = (0,0)
        self.player_orientation = (0,1)
        place_character(self.board, wumpus)
        for _ in range(self.size):
            place_character(self.board, pit)
        self.gold_position = random_empty_square(self.board)

    def __str__(self):
        res = "Points: {}\n".format(self.points)
        if self.fired_arrow:
            res += "You have fired your arrow.\n"
        else:
            res += "You have an arrow.\n"
        if self.gold_position == None:
            res += "You have found the gold.\n"
        res += "You're facing {}.\n".format(print_orientation(self.player_orientation))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != None:
                    res += self.board[i][j] + " "
                elif (i, j) == self.gold_position:
                    res += "G "
                else:
                    res += ". "
            res += "\n"
        return res

    def Move(self):
        self.percepts['scream'] = False
        self.points -= 1
        x, y = self.player_pos
        dx, dy = self.player_orientation
        new_x, new_y = (x + dx, y + dy)
        if not inside_board(new_x, new_y, self.size):
            self.percepts['bump'] = True
        else:
            self.percepts['bump'] = False
            if self.board[new_x][new_y] == wumpus or self.board[new_x][new_y] == pit:
                self.Die(self.board[new_x][new_y])
            else:
                print("You move forward.")
                self.board[x][y] = None
                self.board[new_x][new_y] = player
                self.player_pos = (new_x, new_y)

    def Die(self, cell):
        if cell == wumpus:
            print("The Wumpus eats you!")
        elif cell == pit:
            print("You fall into a bottomless pit!")
        print("You died.")
        self.points -= 1000
        self.finished = True

    def update_percepts(self):
        x, y = self.player_pos
        self.percepts['exit'] = self.player_pos == (0,0)
        self.percepts['glitter'] = self.player_pos == self.gold_position
        self.percepts['stench'] = False
        self.percepts['breeze'] = False
        adj = [(-1,0), (0,1), (1,0), (0,-1)]
        for d in adj:
            dx, dy = d
            n_x, n_y = (x + dx, y + dy)
            if inside_board(n_x, n_y, self.size):
                self.percepts['stench'] |= self.board[n_x][n_y] == wumpus
                self.percepts['breeze'] |= self.board[n_x][n_y] == pit

    def Finished(self):
        return self.finished

    def TurnLeft(self):
        self.percepts['scream'] = False
        self.percepts['bump'] = False
        print("You turn left.")
        self.player_orientation = turn_left(self.player_orientation)

    def TurnRight(self):
        self.percepts['scream'] = False
        self.percepts['bump'] = False
        print("You turn right.")
        self.player_orientation = turn_right(self.player_orientation)

    def Percepts(self):
        self.update_percepts()
        return self.percepts

    def FireArrow(self):
        self.percepts['bump'] = False
        self.percepts['scream'] = False
        if self.fired_arrow:
            print("You have no more arrows to fire.")
            return
        print("You fire your arrow.")
        self.fired_arrow = True
        self.points -= 10
        x, y = self.player_pos
        dx, dy = self.player_orientation
        n_x, n_y = (x + dx, y + dy)
        while inside_board(n_x, n_y, self.size):
            if self.board[n_x][n_y] == wumpus:
                self.percepts['scream'] = True
                self.board[n_x][n_y] = None
                return
            n_x, n_y = (n_x + dx, n_y + dy)
        print("The arrow hits nothing.")

    def Exit(self):
        self.percepts['scream'] = False
        self.percepts['bump'] = False
        if (0,0) != self.player_pos:
            print("You can't exit from here.")
        else:
            print("You exit the world of Wumpus.")
            self.finished = True

    def PickUp(self):
        self.percepts['scream'] = False
        self.percepts['bump'] = False
        x, y = self.player_pos
        if (x, y) == self.gold_position:
            self.points += 1000
            self.gold_position = None
            print("You found the gold!")
        else:
            print("There is nothing here to pickup.")

move = "M"
fire = "F"
left = "L"
right = "R"
pickup = "P"
help_d = "H"
quit = "Q"
cheat = "C"
exit = "X"

def print_help():
    print("The available actions are:")
    print("'{}' for help.".format(help_d))
    print("'{}' to turn left.".format(left))
    print("'{}' to turn right.".format(right))
    print("'{}' to move forward.".format(move))
    print("'{}' to pickup something from the ground.".format(pickup))
    print("'{}' to fire an arrow.".format(fire))
    print("'{}' to exit the cave.".format(exit))
    print("'{}' to cheat.".format(cheat))
    print("'{}' to quit.".format(quit))

def exec_action(world, action):
    a = action.upper()
    if a == help_d:
        print_help()
    elif a == move:
        world.Move()
    elif a == fire:
        world.FireArrow()
    elif a == left:
        world.TurnLeft()
    elif a == right:
        world.TurnRight()
    elif a == pickup:
        world.PickUp()
    elif a == quit:
        print("Bye!")
        sys.exit(0)
    elif a == exit:
        world.Exit()
    elif a == cheat:
        print(world)
    else:
        print("Sorry, I don't understand action '{}'.".format(action))
        print_help()

if __name__ == '__main__':
    print()
    print("Welcome to the world of Wumpus!")
    print()
    print("You enter a dark cave looking for gold. The Wumpus, a terrible creature, waits inside.")
    print("You can move in the four directions (N/W/E/S) through the rooms of this dark cave.")
    print("Some rooms have a bottomless pit inside: you can feel a breeze coming from them,")
    print("when you're next to one of them. Don't enter these rooms, or you'll fall into the pit!")
    print("And stay away from the Wumpus! You can tell where it is from its terrible stench.")
    print("You have a single arrow you can shoot to kill the Wumpus. Look for the glittering gold.")
    print()
    print_help()
    print()
    print("You are facing east. Don't get lost.")
    print()
    world = WumpusWorld()
    while not world.Finished():
        print(print_percepts(world.Percepts()))
        action = get_input("What do you do? ")
        exec_action(world, action)
    print("You made {} points.".format(world.points))
