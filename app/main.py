import json
import os
import random
import bottle
import numpy as np

from api import ping_response, start_response, move_response, end_response
from utils import *


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    # dictionary with reward to choose each
    directions = {'up': 1,
                  'down': 1,
                  'left': 1,
                  'right': 1}

    board_height = data['board']['height']
    board_width = data['board']['width']

    head_x = data['you']['body'][0]['x']
    head_y = data['you']['body'][0]['y']
    neck_x = data['you']['body'][1]['x']
    neck_y = data['you']['body'][1]['y']
    # other_sneks = data['board']['snakes']

    for direction in ['up', 'down', 'left', 'right']:
        reward = 0
        # check if any of the moves will run you into a wall
        if hit_wall(head_x, head_y, board_height, board_width, direction):
            reward += -np.inf

        # check which of the moves will run your head into your neck
        if head_hit_neck(head_x, head_y, neck_x, neck_y, direction):
            reward += -np.inf

        # check if it's going to hit its own tail
        if head_hit_tail(head_x, head_y, data, direction):
            reward += -np.inf

        # check if any of the moves will run you into another snake
        if hit_other_snek(head_x, head_y, data, direction):
            reward += -np.inf

        # check which move will bring you closest to food
        # assign rewards based on how much closer the food is
        reward += assign_food_reward(head_x, head_y, data, direction)

        # update directions dict with new reward
        directions[direction] += reward

    # choose direction with greatest reward
    direction = keywithmaxval(directions)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )

# done
def hit_wall(head_x, head_y, board_height, board_width, direction):
    # true if this move will cause you to hit a wall
    dir_vect = direction_to_vector(direction)
    if (head_x + dir_vect[0] == 0) or (head_x + dir_vect[0] == board_width):
        return(True)
    elif (head_y + dir_vect[1] == 0) or (head_x + dir_vect[1] == board_height):
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
    if new_head_coord in tail_coords:
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
