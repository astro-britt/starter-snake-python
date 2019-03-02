from utils import *

# done
def hit_wall(head_x, head_y, board_height, board_width, direction):
    # true if this move will cause you to hit a wall
    dir_vect = direction_to_vector(direction)
    if (head_x + dir_vect[0] == 0) or (head_x + dir_vect[0] == board_width-1):
        return(True)
    elif (head_y + dir_vect[1] == 0) or (head_x + dir_vect[1] == board_height-1):
        print('would hit a wall if we go {}'.format(direction))
        return(True)
    else:
        return(False)


# done
def head_hit_neck(head_x, head_y, neck_x, neck_y, direction):
    # true if this move will cause you to hit your head on your neck
    dir_vect = direction_to_vector(direction)
    new_head_x = head_x + dir_vect[0]
    new_head_y = head_y + dir_vect[1]
    if (new_head_x == neck_x) & (new_head_y == neck_y):
        return(True)
        print('would run over our own neck if we go {}'.format(direction))
    else:
        return(False)


# done
def hit_other_snek(head_x, head_y, data, direction):
    # True if this move will cause you to collide with another snake
    # according to their current position, not where they could move next
    # also in future, take into account that their tail will shorten if they don't eat
    dir_vect = direction_to_vector(direction)
    new_head_coord = (head_x + dir_vect[0], head_y + dir_vect[1])

    # get coordinates occupied by all other snakes
    other_snek_body_coords = []
    other_snek_possible_heads = []

    for snek in data['board']['snakes']:
        for coord in snek['body']:
            other_snek_body_coords.append((coord['x'], coord['y']))
            # also avoid all possible pixels the other snek could go to
        other_snek_possible_heads.append(get_surrounding_coords(snek['body'][0]['x'], snek['body'][0]['y']))
        # for later if time, check if the other snake can access food,
        # if not then take tail coord out of avoid list
    avoid_coords = other_snek_body_coords + other_snek_possible_heads
    if new_head_coord in avoid_coords:
        return True
        print('would hit other snake if we go {}'.format(direction))
    else:
        return False


def head_hit_tail(head_x, head_y, data, direction):
    # if moving in this direction will cause the head to hit the tail,
    # reurn true
    dir_vect = direction_to_vector(direction)
    new_head_coord = (head_x + dir_vect[0], head_y + dir_vect[1])

    tail_coords = []
    for tail_coord in data['you']['body']:
        tail_coords.append((tail_coord['x'], tail_coord['y']))
        print('my body coords: {}'.format(tail_coords))
    if new_head_coord in tail_coords:
        print('would hit our own tail if we go {}'.format(direction))
    print('my current head position is {} and if we turn {} it will be {}'.format((head_x, head_y), direction, new_head_coord))
        return(True)
    else:
        return(False)


# done
def assign_food_reward(head_x, head_y, data, direction):
    new_head_coord = (head_x + direction_to_vector(direction)[0], head_y + direction_to_vector(direction)[1])
    # make an array of board shape
    # 0s where no food
    # 1s where yes food
    # food_array = np.zeros(data['board']['height'], data['board']['height'])
    food_reward = 0
    for food_spot in data['board']['food']:
        # food_array[food_spot['x'], food_spot['y']] = 1
        # if we turn this direction, how many more turns
        # would it take use to get to this food?
        n_turns_to_food = abs(new_head_coord[0] - food_spot['x']) + abs(new_head_coord[1] - food_spot['y'])
        # assign reward based on maximum possible number of turns
        max_turns = data['board']['height'] + data['board']['height']
        food_reward += max_turns - n_turns_to_food
    return(food_reward)
