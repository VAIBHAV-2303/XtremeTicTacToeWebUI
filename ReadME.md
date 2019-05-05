# Authors

* [Vaibhav Garg](https://github.com/VAIBHAV-2303)
* [Anchit Gupta](https://github.com/Anchit1999)

# Algorithm

* Mini-Max algorithm
* Move Ordering
* Transposition Table
* Comprehensive heuristic

# Heuristic Psuedocode
	
	if WON by maximizer:
		return 1000
	if WON by minimizer:
		return 1000

	if DRAW:
		return 0

	value = 0

	<!-- Big Board hueristic -->
	for both the big boards:
		value += (50/3) * (maximizer_count[1] - minimizer_count[1]) + (400/3) * (maximizer_count[2] - minimizer_count[2])

	Here, maximizer_count[x] refers to small boards won by maximizer consecutively x in a row or column or diagonally such that it is still possible for the the maximizer to win in that respective row or column or diagonal.

	<!-- Small Board huersistic -->
	for every small board that is yet to be conquered and is part of the above mentioned row or column or diagonal: 
		value += 1*(max_num[1] - min_num[1]) + (25/9)*(max_num[2] - min_num[2])

	Here, max_num[x] refers to individual cells marked by maximizer consecutively x in a row or column or diagonally such that the remaining cells are yet to be marked.

	return value


