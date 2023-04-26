from flask import Flask, render_template, request, json
from azul import Azul
from player import HumanPlayer

app = Flask(__name__)

def initialize_game():
    player1 = HumanPlayer(1)
    player2 = HumanPlayer(2)
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

@app.route('/available_colors', methods=['POST'])
def available_colors():
    source_str = request.form['source']
    source = game.factories_dict[source_str]
    print("the source is ", source)
    available_colors = game.get_available_colors(source)
    print("available_colors ",available_colors)
    return json.dumps(available_colors)

@app.route('/available_pattern_lines', methods=['POST'])
def available_pattern_lines():
    print('request is:' ,request.form)
    color = request.form['color']
    player_id = request.form['player_id']
    player = game.player_dict['Player %s' % player_id]
    # print('player is:', player)
    available_pattern_lines = game.get_available_pattern_lines(player,color)
    return json.dumps(available_pattern_lines)

if __name__ == '__main__':
    app.run(debug=True)
