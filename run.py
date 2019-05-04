from simulator import *
from team11 import Team11
from flask import Flask, render_template, request, redirect

t11 = Team11()
mine = 'x'
his = 'o'
old_move = (-1,-1,-1)
game_board = BigBoard()
curturn = 0

# Initialization of flask App
app = Flask(__name__)

@app.route('/')
def game():
	global curturn, old_move, t11, mine, his, game_board

	if curturn == 1:
		my_move = t11.move(game_board, old_move, mine)
		update_status, small_board_won = game_board.update(old_move, my_move, mine)
		old_move = my_move

		if small_board_won:
			my_move = t11.move(game_board, old_move, mine)
			update_status, small_board_won = game_board.update(old_move, my_move, mine)
			old_move = my_move
		curturn = 0

	valid_moves = [list(elem) for elem in game_board.find_valid_move_cells(old_move)]
	return render_template('game.html', big = game_board.big_boards_status, small = game_board.small_boards_status, mine = his, valid_moves = valid_moves)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/recievemove', methods=['POST', 'GET'])
def recievemove():

	global curturn, old_move, t11, mine, his, game_board

	if curturn == 0:
		data = request.get_json(force=True)
		his_turn = (data['b'], data['r'], data['c'])
		
		update_status, small_board_won = game_board.update(old_move, his_turn, his)
		old_move = his_turn

		if small_board_won:
			curturn = 0
		else:
			curturn = 1
		
		return redirect('/')

	return "Great"

@app.route('/recievemode', methods=['POST', 'GET'])
def recievemode():

	global curturn, old_move, t11, mine, his, game_board

	data = request.get_json(force=True)
	
	if data['mode'] == 1:
		mine = 'o'
		his = 'x'
		curturn = 0
	else:
		mine = 'x'
		his = 'o'
		curturn = 1

	old_move = (-1, -1, -1)
	game_board = BigBoard()

	return redirect('/')

app.run(debug = True)