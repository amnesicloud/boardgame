from flask import Flask, render_template, request, json, jsonify
from azul import Azul
from player import HumanPlayer

app = Flask(__name__)

def initialize_game():
    player1 = HumanPlayer(0)
    player2 = HumanPlayer(1)
    game = Azul(num_players=2, player_list=[player1, player2])
    return game

game = initialize_game()

@app.route('/')
def index():
    game_state = json.dumps(game.to_dict())
    print("=" * 50)
    print(game_state)  # Add this line to print the game state JSON
    return render_template('index.html', game_state=game_state)

# @app.route('/play', methods=['POST'])
# def play():
#     # Retrieve the action from the form data
#     action = request.form.get('action')
#
#     # Process the action and update the game state
#     # ...
#
#     # Convert the game state to JSON
#     game_state = game.to_dict()
#
#     # Render the template and pass the game state
#     return render_template('index.html', game_state=json.dumps(game_state))

# @app.route('/available_colors', methods=['POST'])
# def available_colors():
#     source_str = request.form['source']
#     source = game.factories_dict[source_str]
#     print("the source is ", source)
#     available_colors = game.get_available_colors(source)
#     print("available_colors ",available_colors)
#     return json.dumps(available_colors)

@app.route('/available_colors', methods=['POST'])
def available_colors():
    data = request.json  # Access the JSON data sent in the request
    source_str = data['source']  # Get the 'source' from the JSON data
    source = game.factories_dict[source_str]
    print("the source is ", source)
    available_colors = game.get_available_colors(source)
    print("available_colors ", available_colors)
    return jsonify(available_colors)  # Use Flask's jsonify to return JSON response


@app.route('/available_pattern_lines', methods=['POST'])
def available_pattern_lines():
    print('request is:' ,request.form)
    data = request.json
    color = data['color']
    player_id = request.form['player_id']
    player = game.player_dict[int(player_id)]
    # print('player is:', player)
    available_pattern_lines = game.get_available_pattern_lines(player,color)
    print("available_pattern_lines :", available_pattern_lines)
    return json.dumps(available_pattern_lines)




@app.route('/get_game_state')
def get_game_state():
    # Fetch or generate the current game state
    game_state = game.to_dict()
    # Return the game state as JSON
    # print("game_state", game_state)
    print("get_game_state", jsonify(game_state))
    return jsonify(game_state)

@app.route('/send_action', methods=['POST'])
def handle_action():
    # Get the action data from the request
    action = request.json
    print("=" * 100)
    print("handle_action")
    data = request.json
    print("data is:", data)
    currentPlayer_id = data['currentPlayerId']
    currentPlayer = game.player_dict[int(currentPlayer_id)]

    source_id = data['factoryId']

    if source_id == "Factory_center":
        source_id = "Center"
    source = game.factories_dict[source_id]

    color = data['tileColor']

    if data['destination'] != "floorLine":
        patternLine = int(data['destination'].split("-")[1])
    else:
        patternLine = -1

    # Update game state with the selected source, color, and pattern line
    # game_state.update_game_state(currentPlayer, source, color, patternLine)

    print("before perform")
    print(game.to_dict())
    game.perform_action(currentPlayer, source, color, patternLine)
    print("-" * 100)
    print("after perform")
    print(game.to_dict())

    if game.is_round_over():
        game.end_round()
    if game.is_game_over():
        game.get_winner()

    game_state = game.to_dict()
    # Return the updated game state as JSON
    return jsonify(game_state)

# Assume you have a function to process the action and update the game state
def process_action(action, game_state):
    # Update game_state based on the action
    # Return the updated game state
    return updated_game_state

if __name__ == '__main__':
    app.run(debug=True)
