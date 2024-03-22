# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com
import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    # Check if moving up will be within bounds
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # Check if moving down will be within bounds
    if my_head["y"] == 0:
        is_move_safe["down"] = False

    # Check if moving left will be within bounds
    if my_head["x"] == 0:
        is_move_safe["left"] = False

    # Check if moving right will be within bounds
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    # Iterates through each segment of the snake body
    for body_segment in my_body[1:]:

        # Check if moving up would cause collision
        if my_head["x"] == body_segment["x"] and my_head["y"] + 1 == body_segment["y"]:
            is_move_safe["up"] = False

        # Check if moving down would cause collision
        if my_head["x"] == body_segment["x"] and my_head["y"] - 1 == body_segment["y"]:
            is_move_safe["down"] = False

        # Check if moving left would cause collision
        if my_head["x"] - 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
            is_move_safe["left"] = False

        # Check if moving right would cause collision
        if my_head["x"] + 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
            is_move_safe["right"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']
    opponents = game_state['board']['snakes']
    for snake in opponents:
        for body_segment in snake['body']:
            #collision moving up
            if my_head["x"] == body_segment["x"] and my_head["y"] + 1 == body_segment["y"]:
                is_move_safe["up"] = False
            #collision moving down
            if my_head["x"] == body_segment["x"] and my_head["y"] - 1  == body_segment["y"]:
                is_move_safe["down"] = False
            #collision moving left
            if my_head["x"] - 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
                is_move_safe["left"] = False
            #collision moving right
            if my_head["x"] + 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
                is_move_safe["right"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    # Calculate the distance between two points
    def distance(point1, point2):
        return abs(point1['x'] - point2['x']) + abs(point1['y'] - point2['y'])
    
    # Calculate the distance from the head to the closest food
    closest_food = food[0] # Set the closest food to the first food item
    closest_food_distance = distance(my_head, closest_food) # Set the closest food distance to the distance from the head to the first food item

    for food_item in food:
        food_distance = distance(my_head, food_item) # Calculate the distance from the head to the food
        if food_distance < closest_food_distance: # If the distance is less than the current closest food
            closest_food = food_item # Set the closest food to the current food
            closest_food_distance = food_distance # Set the closest food distance to the current food distance

    # Move towards the closest food
    if closest_food['x'] > my_head['x'] and 'right' in safe_moves: # If the closest food is to the right and moving right is safe
        next_move = 'right' # Move right
    elif closest_food['x'] < my_head['x'] and 'left' in safe_moves: # If the closest food is to the left and moving left is safe
        next_move = 'left' # Move left
    elif closest_food['y'] > my_head['y'] and 'up' in safe_moves: # If the closest food is above and moving up is safe
        next_move = 'up' # Move up
    elif closest_food['y'] < my_head['y'] and 'down' in safe_moves: # If the closest food is below and moving down is safe
        next_move = 'down' # Move down
    

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
