import json
import os
import random
import bottle
import numpy as np

from api import ping_response, start_response, move_response, end_response
from utils import *
from logic import *


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

    turn = data['turn']
    board_height = data['board']['height']
    board_width = data['board']['width']

    head_x = data['you']['body'][0]['x']
    head_y = data['you']['body'][0]['y']
    if turn != 1:
        neck_x = data['you']['body'][1]['x']
        neck_y = data['you']['body'][1]['y']
    # other_sneks = data['board']['snakes']

    for direction in ['up', 'down', 'left', 'right']:
        reward = 0
        # check if any of the moves will run you into a wall
        if hit_wall(head_x, head_y, board_height, board_width, direction):
            reward += -np.inf

        # check which of the moves will run your head into your neck
        if turn != 1:
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

        # for the log
        print(directions)

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
