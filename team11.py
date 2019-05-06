from __future__ import division
import numpy as np
import time
import copy

class Team11():

    def __init__(self, depth):

        self.MAX_DEPTH = depth
        self.hash_small_board_heuristic = np.zeros((3,3,3,3,3,3,3,3,3))
        self.hash_small_board_heuristic[:] = -1e6
        self.numOfMoves = 0
        self.bonus_move = 0

    def move(self, board, old_move, flag):

        self.startTime = time.time()

        self.numOfMoves += 1
        # if self.numOfMoves == 20:
        #     self.MAX_DEPTH = 3
        # if self.numOfMoves == 30:
        #     self.MAX_DEPTH = 4
        # if self.numOfMoves == 37:
        #     self.MAX_DEPTH = 5
        # if self.numOfMoves == 41:
        #     self.MAX_DEPTH = 6
        # if self.numOfMoves == 43:
        #     self.MAX_DEPTH = 7
        # if self.numOfMoves == 44:
        #     self.MAX_DEPTH = 8

        if self.numOfMoves == 1:
            self.maximizer = flag
            if flag == 'x':
                self.minimizer = 'o'
            else:
                self.minimizer = 'x'

            self.mp = {self.maximizer: 0 , self.minimizer: 1, '-': 2}
            if flag == 'x':
                return (0, 4, 4)
            
        movearr = board.find_valid_move_cells(old_move)

        ordered_movearr = []
        for i in range(len(movearr)):
            deep_cop = copy.deepcopy(board)
            deep_cop.update(old_move, movearr[i], self.maximizer)
            ordered_movearr.append((self.heuristic(deep_cop), movearr[i]))

        ordered_movearr = sorted(ordered_movearr, key = lambda x: x[0], reverse = True)

        curBest = -1e4
        for i in range(len(ordered_movearr)):
            deep_cop = copy.deepcopy(board)
            deep_cop.update(old_move, ordered_movearr[i][1], self.maximizer)
            
            if self.bonus_move == 0 and board.small_boards_status[ordered_movearr[i][1][0]][ordered_movearr[i][1][1]//3][ordered_movearr[i][1][2]//3] == '-'\
            and deep_cop.small_boards_status[ordered_movearr[i][1][0]][ordered_movearr[i][1][1]//3][ordered_movearr[i][1][2]//3] == self.maximizer:
                value = self.minimax(deep_cop, self.maximizer, curBest, 1000, ordered_movearr[i][1], 0, 1)
            else:
                value = self.minimax(deep_cop, self.minimizer, curBest, 1000, ordered_movearr[i][1], 0, 0)

            if value > curBest:
                curBest = value
                bestMove = ordered_movearr[i][1]

        deep_cop = copy.deepcopy(board)
        deep_cop.update(old_move, bestMove, self.maximizer)

        if self.bonus_move == 1:
        	self.bonus_move = 0
        elif self.bonus_move == 0 and board.small_boards_status[bestMove[0]][bestMove[1]//3][bestMove[2]//3] == '-' \
        and deep_cop.small_boards_status[bestMove[0]][bestMove[1]//3][bestMove[2]//3] == self.maximizer:
        	self.bonus_move = 1

        return bestMove

    def drawvalue(self, board):
        sb = board.small_boards_status
        p1 = self.maximizer
        p2 = self.minimizer
        score = 0
        for u in range(2):
            #corners
            if sb[u][0][0] == p1:
                score += 4
            elif sb[u][0][0] == p2:
                score -= 4

            if sb[u][0][2] == p1:
                score += 4
            elif sb[u][0][2] == p2:
                score -= 4

            if sb[u][2][0] == p1:
                score += 4
            elif sb[u][2][0] == p2:
                score -= 4

            if sb[u][2][2] == p1:
                score += 4
            elif sb[u][2][2] == p2:
                score -= 4

            if sb[u][0][1] == p1:
                score += 6
            elif sb[u][0][1] == p2:
                score -= 6

            if sb[u][1][0] == p1:
                score += 6
            elif sb[u][1][0] == p2:
                score -= 6

            if sb[u][1][2] == p1:
                score += 6
            elif sb[u][1][2] == p2:
                score -= 6

            if sb[u][2][1] == p1:
                score += 6
            elif sb[u][2][1] == p2:
                score -= 6

            if sb[u][1][1] == p1:
                score += 3
            elif sb[u][1][1] == p2:
                score -= 3

        return score

    def minimax(self, board, player, alpha, beta, old_move, depth, bonus):

        status = board.find_terminal_state()
        if status[1] == "WON":
            if status[0] == self.maximizer:
                return 1000
            else:
                return -1000
        if status[1] == "DRAW":
            return self.drawvalue(board)

        movearr = board.find_valid_move_cells(old_move)
        
        if depth > self.MAX_DEPTH:
            return self.heuristic(board)

        if time.time()-self.startTime > 22:
            # print "Not good"
            return self.heuristic(board)

        ordered_movearr = []

        if player == self.maximizer:
            for i in range(len(movearr)):
                deep_cop = copy.deepcopy(board)
                deep_cop.update(old_move, movearr[i], self.maximizer)
                ordered_movearr.append((self.heuristic(deep_cop),movearr[i]))

            ordered_movearr = sorted(ordered_movearr, key = lambda x: x[0], reverse = True)

            curBest = -1e3
            for i in range(len(ordered_movearr)):
                deep_cop = copy.deepcopy(board)
                deep_cop.update(old_move, ordered_movearr[i][1], self.maximizer)

                if bonus == 0 and board.small_boards_status[ordered_movearr[i][1][0]][ordered_movearr[i][1][1]//3][ordered_movearr[i][1][2]//3] == '-'\
                and deep_cop.small_boards_status[ordered_movearr[i][1][0]][ordered_movearr[i][1][1]//3][ordered_movearr[i][1][2]//3] == self.maximizer:
                    curBest = max(curBest, self.minimax(deep_cop, self.maximizer, alpha, beta, ordered_movearr[i][1], depth+1, 1))
                else:
                    curBest = max(curBest, self.minimax(deep_cop, self.minimizer, alpha, beta, ordered_movearr[i][1], depth+1, 0))            

                alpha = max(alpha, curBest)
                if alpha >= beta:
                    break

            return curBest
        else:
            for i in range(len(movearr)):
                deep_cop = copy.deepcopy(board)
                deep_cop.update(old_move, movearr[i], self.minimizer)
                ordered_movearr.append((self.heuristic(deep_cop), movearr[i]))

            ordered_movearr = sorted(ordered_movearr, key = lambda x: x[0])

            curBest = 1e3
            for i in range(len(ordered_movearr)):
                deep_cop = copy.deepcopy(board)
                deep_cop.update(old_move, ordered_movearr[i][1], self.minimizer)

                if bonus == 0 and board.small_boards_status[ordered_movearr[i][1][0]][ordered_movearr[i][1][1]//3][ordered_movearr[i][1][2]//3] == '-'\
                and deep_cop.small_boards_status[ordered_movearr[i][1][0]][ordered_movearr[i][1][1]//3][ordered_movearr[i][1][2]//3] == self.minimizer:                
                    curBest = min(curBest, self.minimax(deep_cop, self.minimizer, alpha, beta, ordered_movearr[i][1], depth+1, 1))
                else:
                    curBest = min(curBest, self.minimax(deep_cop, self.maximizer, alpha, beta, ordered_movearr[i][1], depth+1, 0))

                beta = min(beta, curBest)
                if alpha >= beta:
                    break

            return curBest
    
    def smallWins(self,board,board_no,row,col, player):

        s_b = board.small_boards_status[board_no][row][col]
        if s_b == self.maximizer:
            return self.maximizer
        
        if s_b == self.minimizer:
            return self.minimizer

        if s_b == 'd':
            return 'DRAW'

    	s_b = board.big_boards_status[board_no]
    	otherPlayer = 'x'
        if player == 'x':
            otherPlayer = 'o'
    	# Horizontal
        for i in range(3):
            flagOppPlayer = 0
            for j in range(3):
                if s_b[3*row+i][3*col+j] == otherPlayer:
                    flagOppPlayer = 1

    		if flagOppPlayer == 0:
    			return 'POSSIBLE'

    	# Vertical
    	for i in range(3):
    		flagOppPlayer = 0
    		for j in range(3):
    			if s_b[3*row+j][3*col+i] == otherPlayer:
    				flagOppPlayer = 1

    		if flagOppPlayer == 0:
    			return 'POSSIBLE'

    	# Diagonal
    	for i in range(3):
    		flagOppPlayer = 0
    		if s_b[3*row+i][3*col+i] == otherPlayer:
    			flagOppPlayer = 1
    	
    	if flagOppPlayer == 0:
    		return 'POSSIBLE'

		for i in range(3):
			flagOppPlayer = 0
    		if s_b[3*row+i][3*col+2-i] == otherPlayer:
    			flagOppPlayer = 1
    	
    	if flagOppPlayer == 0:
    		return 'POSSIBLE'        	

    	return 'DRAW'

    def smallBoardHeuristic(self,board,index):

    	sb = board[index[0]]
    	r = 3*index[1]
    	c = 3*index[2]
    	mp = self.mp
    	if self.hash_small_board_heuristic[ mp[sb[r][c]] ][ mp[sb[r][c+1]] ][ mp[sb[r][c+2]] ][ mp[sb[r+1][c]] ][ mp[sb[r+1][c+1]] ]\
    							[ mp[sb[r+1][c+2]] ][ mp[sb[r+2][c]] ][ mp[sb[r+2][c+1]] ][ mp[sb[r+2][c+2]] ] == -1e6:

	    	max_num = [0,0,0,0]
	    	min_num = [0,0,0,0]
	    	#horizontal
	    	for i in range(3):
	    		pcmax = 0
	    		pcmin = 0
	    		flagmax = 1
	    		flagmin = 1
	    		for j in range(3):
	    			s_b = board[index[0]][3*index[1]+i][3*index[2]+j]
	    			if s_b == self.maximizer:
	    				flagmin = 0
	    				pcmax += 1

	    			if s_b == self.minimizer:
	    				flagmax = 0
	    				pcmin += 1

	    		if flagmax == 1:
	    			max_num[pcmax] += 1
	    		if flagmin == 1:
	    			min_num[pcmin] += 1

	    	#vertical
	    	for i in range(3):
	    		pcmax = 0
	    		pcmin = 0
	    		flagmax = 1
	    		flagmin = 1
	    		for j in range(3):
	    			s_b = board[index[0]][3*index[1]+j][3*index[2]+i]
	    			if s_b == self.maximizer:
	    				flagmin = 0
	    				pcmax += 1
	    			if s_b == self.minimizer:
	    				flagmax = 0
	    				pcmin += 1

	    		if flagmax == 1:
	    			max_num[pcmax] += 1
	    		if flagmin == 1:
	    			min_num[pcmin] += 1

	    	#diagonal
	    	pcmax = 0
	    	pcmin = 0
	    	flagmax = 1
	    	flagmin = 1
	    	for i in range(3):
	    		s_b = board[index[0]][3*index[1]+i][3*index[2]+i]

	    		if s_b == self.maximizer:
	    			flagmin = 0
	    			pcmax += 1
	    		if s_b == self.minimizer:
	    			flagmax = 0
	    			pcmin += 1

	    	if flagmax == 1:
	    		max_num[pcmax] += 1
	    	if flagmin == 1:
	    		min_num[pcmin] += 1

	    	pcmax = 0
	    	pcmin = 0
	    	flagmax = 1
	    	flagmin = 1
	    	for i in range(3):
	    		s_b = board[index[0]][3*index[1]+i][3*index[2]+2-i]

	    		if s_b == self.maximizer:
	    			flagmin = 0
	    			pcmax += 1
	    		if s_b == self.minimizer:
	    			flagmax = 0
	    			pcmin += 1

	    	if flagmax == 1:
	    		max_num[pcmax] += 1
	    	if flagmin == 1:
	    		min_num[pcmin] += 1

	    	partial = 1*(max_num[1] - min_num[1]) + (25/9)*(max_num[2] - min_num[2])

	    	if max_num[3] == 1:
	    		partial = 50/3
	    	if min_num[3] == 1:
	    		partial = -50/3
	    	
	    	self.hash_small_board_heuristic[ mp[sb[r][c]] ][ mp[sb[r][c+1]] ][ mp[sb[r][c+2]] ][ mp[sb[r+1][c]] ][ mp[sb[r+1][c+1]] ]\
                                    [ mp[sb[r+1][c+2]] ][ mp[sb[r+2][c]] ][ mp[sb[r+2][c+1]] ][ mp[sb[r+2][c+2]] ] = partial

    	return self.hash_small_board_heuristic[ mp[sb[r][c]] ][ mp[sb[r][c+1]] ][ mp[sb[r][c+2]] ][ mp[sb[r+1][c]] ][ mp[sb[r+1][c+1]] ]\
    								[ mp[sb[r+1][c+2]] ][ mp[sb[r+2][c]] ][ mp[sb[r+2][c+1]] ][ mp[sb[r+2][c+2]] ]

    def heuristic(self,board):

        partial = 0

        maximizer_count = [0,0,0,0]
        minimizer_count = [0,0,0,0]

        for u in range (2):

            #horizontal
            for i in range(3):
                player_count_maximizer = 0
                player_count_minimizer = 0
                flag_maximizer_possible = 1
                flag_minimizer_possible = 1
                temp = []
                for j in range(3):
                    if self.smallWins(board,u,i,j, self.maximizer) == self.maximizer:
                        player_count_maximizer += 1
                        flag_minimizer_possible = 0
                    
                    if self.smallWins(board,u,i,j, self.minimizer) == self.minimizer:
                        player_count_minimizer += 1
                        flag_maximizer_possible = 0

                    if self.smallWins(board,u,i,j, self.maximizer) == 'DRAW':
                        flag_maximizer_possible = 0

                    if self.smallWins(board,u,i,j, self.minimizer) == 'DRAW':
                        flag_minimizer_possible = 0

                    if self.smallWins(board,u,i,j, self.maximizer) == 'POSSIBLE' and self.smallWins(board, u, i, j, self.minimizer) == 'POSSIBLE':
                    	temp.append((u,i,j))
            
                if flag_minimizer_possible == 1 or flag_maximizer_possible == 1:
	                for k in range(len(temp)):
	                	partial += self.smallBoardHeuristic(board.big_boards_status,temp[k]);
                if flag_maximizer_possible == 1:
                    maximizer_count[player_count_maximizer] += 1
                if flag_minimizer_possible == 1:
                    minimizer_count[player_count_minimizer] += 1


            #vertical
            for i in range(3):
                player_count_maximizer = 0
                player_count_minimizer = 0
                flag_maximizer_possible = 1
                flag_minimizer_possible = 1
                temp = []
                for j in range(3):
                    if self.smallWins(board,u,j,i,self.maximizer) == self.maximizer:
                        player_count_maximizer += 1
                        flag_minimizer_possible = 0
                    
                    if self.smallWins(board,u,j,i,self.minimizer) == self.minimizer:
                        player_count_minimizer += 1
                        flag_maximizer_possible = 0

                    if self.smallWins(board,u,j,i,self.maximizer) == 'DRAW':
                        flag_maximizer_possible = 0
                    if self.smallWins(board,u,j,i,self.minimizer) == 'DRAW':
                        flag_minimizer_possible = 0
                    if self.smallWins(board,u,j,i,self.maximizer) == 'POSSIBLE' and self.smallWins(board, u, i, j, self.minimizer) == 'POSSIBLE':
                    	temp.append((u,j,i))

                if flag_maximizer_possible == 1:
                    maximizer_count[player_count_maximizer] += 1
                if flag_minimizer_possible == 1:
                    minimizer_count[player_count_minimizer] += 1
                if flag_minimizer_possible == 1 or flag_maximizer_possible == 1:
                	for k in range(len(temp)):
                		partial += self.smallBoardHeuristic(board.big_boards_status,temp[k])

            #diagonal
            player_count_maximizer = 0
            player_count_minimizer = 0
            flag_maximizer_possible = 1
            flag_minimizer_possible = 1
            temp = []
            for i in range(3):
                if self.smallWins(board,u,i,i,self.maximizer) == self.maximizer:
                    player_count_maximizer += 1
                    flag_minimizer_possible = 0
                if self.smallWins(board,u,i,i,self.minimizer) == self.minimizer:
                    player_count_minimizer += 1
                    flag_maximizer_possible = 0
                if self.smallWins(board,u,i,i,self.maximizer) == 'DRAW':
                    flag_maximizer_possible = 0
                if self.smallWins(board,u,i,i,self.minimizer) == 'DRAW':
                    flag_minimizer_possible = 0
                if self.smallWins(board,u,i,i,self.maximizer) == 'POSSIBLE' and self.smallWins(board, u, i, j, self.minimizer) == 'POSSIBLE':
                	temp.append((u,i,i))

            if flag_maximizer_possible == 1:
                maximizer_count[player_count_maximizer] += 1
            if flag_minimizer_possible == 1:
                minimizer_count[player_count_minimizer] += 1
            if flag_minimizer_possible == 1 or flag_maximizer_possible == 1:
            	for k in range(len(temp)):
            		partial += self.smallBoardHeuristic(board.big_boards_status,temp[k])

            player_count_maximizer = 0
            player_count_minimizer = 0
            flag_maximizer_possible = 1
            flag_minimizer_possible = 1
            temp = []
            for i in range(3):
                
                if self.smallWins(board,u,i,2-i,self.maximizer) == self.maximizer:
                    player_count_maximizer += 1
                    flag_minimizer_possible = 0

                if self.smallWins(board,u,i,2-i,self.minimizer) == self.minimizer:
                    player_count_minimizer += 1
                    flag_maximizer_possible = 0

                if self.smallWins(board,u,i,2-i,self.maximizer) == 'DRAW':
                    flag_maximizer_possible = 0
                if self.smallWins(board,u,i,2-i,self.minimizer) == 'DRAW':
                    flag_minimizer_possible = 0
                if self.smallWins(board,u,i,2-i,self.maximizer) == 'POSSIBLE' and self.smallWins(board, u, i, j, self.minimizer) == 'POSSIBLE':
                	temp.append((u, i, 2-i))

            if flag_maximizer_possible == 1:
                maximizer_count[player_count_maximizer] += 1
            if flag_minimizer_possible == 1:
                minimizer_count[player_count_minimizer] += 1
            if flag_minimizer_possible == 1 or flag_maximizer_possible == 1:
            	for k in range(len(temp)):
            		partial += self.smallBoardHeuristic(board.big_boards_status,temp[k])

        partial += 50/3 * (maximizer_count[1] - minimizer_count[1]) + 400/3 * (maximizer_count[2] - minimizer_count[2])
        if maximizer_count[3] == 1:
        	partial = 1000
        if minimizer_count[3] == 1:
        	partial = -1000

        return partial

