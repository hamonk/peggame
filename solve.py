import sys


if sys.argv[1] == 'standard':
    # standard
    pos = ({                 (5,1):1,
                        (4,1):1, (4,2):1,
                    (3,1):1, (3,2):0, (3,3):1,
                (2,1):1, (2,2):1, (2,3):1, (2,4):1,
            (1,1):1, (1,2):1, (1,3):1, (1,4):1, (1,5):1}, [])

elif sys.argv[1] == 'corner':
    # corner
    pos = ({                 (5,1):1,
                        (4,1):1, (4,2):1,
                    (3,1):1, (3,2):1, (3,3):1,
                (2,1):1, (2,2):1, (2,3):1, (2,4):1,
            (1,1):0, (1,2):1, (1,3):1, (1,4):1, (1,5):1}, [])

elif sys.argv[1] == 'b21':
    # side
    pos = ({                 (5,1):1,
                        (4,1):1, (4,2):1,
                    (3,1):1, (3,2):1, (3,3):1,
                (2,1):0, (2,2):1, (2,3):1, (2,4):1,
            (1,1):1, (1,2):1, (1,3):1, (1,4):1, (1,5):1}, [])

elif sys.argv[1] == 'b31':
    # side
    pos = ({                 (5,1):1,
                        (4,1):1, (4,2):1,
                    (3,1):0, (3,2):1, (3,3):1,
                (2,1):1, (2,2):1, (2,3):1, (2,4):1,
            (1,1):1, (1,2):1, (1,3):1, (1,4):1, (1,5):1}, [])

else:
    # easy test
    pos = ({                 (5,1):1,
                        (4,1):0, (4,2):0,
                      (3,1):0, (3,2):1, (3,3):0,
                   (2,1):0, (2,2):1, (2,3):0, (2,4):0,
            (1,1):0, (1,2):0, (1,3):0, (1,4):0, (1,5):0}, [])


ref = {5: [1], 4: [1,2], 3: [1,2,3], 2: [1,2,3,4], 1: [1,2,3,4,5]}

def valid(x):
    if (x[0] >= 1) & (x[0] <= 5) & (x[1] >= 1) & (x[1] <= 5):
        return x[1] in ref[x[0]]
    else:
        False

def find_moves(pos):
    # print(f"find next moves for: {pos}")
    moves = {x: [] for x in pos[0].keys()}
    found_move = False
    for x in pos[0].keys():
        if pos[0][x] == 1:
            for move in [(2,-2), (0,-2),
                        (2,0), (-2,0),
                        (0,2), (-2, 2)]:
                new_pos = (x[0] + move[0], x[1] + move[1])
                
                # inside the triangle and middle is a 1
                if valid(new_pos):
                    if (pos[0][(x[0]+new_pos[0]) / 2, (x[1]+new_pos[1]) / 2] == 1):
                        moves[x].append(new_pos)
                        found_move = True
                        # print_pos(pos)
                        # print(f"here: {(x[0]+new_pos[0]) / 2, (x[1]+new_pos[1]) / 2} / {x} -> {new_pos}")
    return moves, found_move

def get_new_pos(pos, orig, dest):
    new_pos = pos[0].copy()
    new_pos[orig] = 0
    new_pos[dest] = 1
    new_pos[(orig[0]+dest[0]) / 2, (orig[1]+dest[1]) / 2] = 0
    return new_pos

def print_pos(pos):
    print(f"    {pos[0][(5,1)]}")
    print(f"   {pos[0][(4,1)]} {pos[0][(4,2)]}")
    print(f"  {pos[0][(3,1)]} {pos[0][(3,2)]} {pos[0][(3,3)]}")
    print(f" {pos[0][(2,1)]} {pos[0][(2,2)]} {pos[0][(2,3)]} {pos[0][(2,4)]}")
    print(f"{pos[0][(1,1)]} {pos[0][(1,2)]} {pos[0][(1,3)]} {pos[0][(1,4)]} {pos[0][(1,5)]}\n")

print_pos(pos)

# position = position + list of moves

def find_next_pos(pos):
    res = []
    moves, found_move = find_moves(pos)
    for x in pos[0]:
        if pos[0][x] == 1:
            for y in moves[x]:
                if pos[0][y] == 0:
                    new_pos = get_new_pos(pos, x, y)
                    res.append((new_pos, pos[1] + [f"{x[0]}{x[1]}->{y[0]}{y[1]}"]))
    return res, found_move

def find_next(positions):
    res = []
    dead = []
    for position in positions:
        
        next_positions, found_move = find_next_pos(position)
        # print_pos(position)
        # print(found_move)
        
        if found_move:
            res += next_positions
        else:
            dead.append(position)
    return res, dead

summary = []

# init
positions, found_move = find_next_pos(pos)
summary.append(len(positions))
deads = {}

# 13 to finish
for x in range(1, int(sys.argv[2])):
    print(f"i:{x} ##########")
    positions, deads[x] = find_next(positions)
    summary.append(len(positions))

# dead ends
print("### dead ends ###")
for x in deads.keys():
    print(f"{x}: {len(deads[x])}")

for i, pos in enumerate(positions):
    print(f" {i} ######### {sum(pos[0].values())} / {' '.join(pos[1])}")
    print_pos(pos)

print(f"{len(positions)} different solutions")

final_positions = ["".join([str(y) for y in list(x[0].values())]) for x in positions]
combined = list(zip(final_positions, positions))

unique_sol = set(final_positions)
examples = []
for x in unique_sol:
    found = False
    print(f"######## final position {x}")
    for y in combined:
        if (not found) and (x == y[0]):
            print_pos(y[1])
            found = True

print("######## number of solutions at each step")
print(summary)

print("######## dead ends")
for x in deads.keys():
    print(f"{x}: {len(deads[x])}")

# for x in deads[12][:5]:
#     print_pos(x)