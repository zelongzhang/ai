import random
# Simple game of nuts which allows a user to select 3 diiferent modes of play: human vs human, human vs ai and human vs trained ai.

# get an integer between min and max inclusive. Catches out of range and invalid types.
def get_int(min,max,prompt):
	while True:
		try:
			i=int(input(prompt))
			if not min<=i<=max:
				print('Please enter an integet between ',min,' and ',max)
			else:
				return i
		except ValueError:
			print('Please enter an integer')


# participants of the game takes a turn based on their type. Hat is only required by smart ai.
def take_turn(min,max,type,hat):
		choice = 0
		if type=='random_ai': 					# random ai for human vs ai
			choice = random.randrange(min,max,1)
		elif type=='smart_ai':						# weighted selection using the ai hat at the specific nut for smart ais
			choice = random.choices([i for i in range(min,max+1,1)],weights=[hat[0],hat[1],hat[2]],k=1)[0]
		else: 									# selection for human players
			prompt = str(type)+': How many nuts do you take?  '+'('+ str(min) +'-'+ str(max) +')'
			choice = get_int(min,max,prompt)
		return choice


# function to call different game modes.
def play(mode,turn_min,turn_max,nuts):
	if mode ==1:
		human_vs_human(turn_min,turn_max,nuts)
	elif mode==2:
		human_vs_ai(turn_min,turn_max,nuts)
	elif mode==3:
		human_vs_trained_ai(turn_min,turn_max,nuts)


# human vs human play mode. Each player takes a turn and then a check to see if they've lost. If they haven't the other players takes a turn.
# continues until nuts reaches 0 or below so taking 3 nuts at nuts=1 will still result in a loss
def human_vs_human(turn_min,turn_max,nuts):
		while nuts>0:
			nuts-=take_turn(turn_min,turn_max,'Player 1',[])
			if nuts <=0:
					print('Player 1 loses')
					break
			else:
				print('\nThere are ',nuts,' nuts on the table')
				nuts -= take_turn(turn_min,turn_max,'Player 2',[])
				
			if nuts <=0:
				print('Player 2 loses')
				break
			else:
				print('\nThere are ',nuts,' nuts on the table')


# human vs random/dumb ai. human player same as human vs human. Ai chooses randomly and game continues until nuts <0
def human_vs_ai(turn_min,turn_max,nuts):
	while nuts>0:

			nuts-=take_turn(turn_min,turn_max,'Player 1',[])
			if nuts <=0:
					print('Player 1 loses')
					break
			else:
				print('\nThere are ',nuts,' nuts on the table')
				ai_choice= take_turn(turn_min,turn_max,'random_ai',[])
				print('ai takes ',ai_choice,' nuts')
				nuts-=ai_choice
			if nuts <=0:
				print('ai loses')
				break
			else:
				print('\nThere are ',nuts,' nuts on the table')


# human vs a trained/smart ai. Ai is trained in function train_ai().
# the game is similar to human vs ai with the ai also passing its ai[nuts]/hat into take_turn() to make a decision.
# Player may choose to play against ai again with the same numbe of initial nuts since it takes a while to re-train an ai.
def human_vs_trained_ai(turn_min,turn_max,nuts):
	times_to_train=100000 #@grader: please set lower if using test code in train_ai()
	ai_trained = train_ai(turn_min,turn_max,nuts,times_to_train)
	play_again=1
	while play_again==1:
		nuts_this_round=int(nuts)
		while nuts_this_round>0:
			nuts_this_round-=take_turn(1,3,'Player 1',[])
			if nuts_this_round <=0:
				print('Player 1 loses')
				play_again=get_int(0,1,'Play trained ai again? (1:yes,0:no)')
				break
			else:
				print('\nThere are ',nuts_this_round,' nuts on the table')
				ai_choice= take_turn(1,3,'smart_ai',ai_trained[nuts_this_round])
				print('ai takes ',ai_choice,' nuts')
				nuts_this_round-=ai_choice
			if nuts_this_round <=0:
				print('ai loses')
				play_again=get_int(0,1,'Play trained ai again? (1:yes,0:no)')
				break
			else:
				print('\nThere are ',nuts_this_round,' nuts on the table')


# Trains an ai to go second in the game of nuts. Not always trained well. 
# Resulting trained ais takes nuts such that 4x+1,where x>=0 (i.e 13,17,21...) nuts remain after their turn
# On any initial nuts = 4x+1, the ai which goes second is heavily favored(95%+ win rate)
# On all other initial nuts, the first ai is heavily favored(~99%) and the second ai which is what we need is not well trained
# Higher initial nuts input does not ensure more effective training. The heavily losing ai's smaller hats are better trained than higher hats
# Higher iteration times produces better hats.
def train_ai(turn_min,turn_max,nuts,iteration):
	ai=[[0]] #hats for each ai, @grader: [0] denotes 0 nuts on table. Thus, ai[nuts]=hat at nuts
	ai_trained=[[0]]
	ai_this_round=[]# lists for the path of each ai in a round
	ai_trained_this_round=[]
	total_nuts=int(nuts)
	print('Training ai...')
	for i in range(nuts):
		ai.append([1 for i in range(turn_max-turn_min+1)])
		ai_trained.append([1 for i in range(turn_max-turn_min+1)])
	#ai_win=0 	#counter for ai wins
	#ai_trained_win=0

	for i in range(iteration):
		nuts=int(total_nuts)
		while nuts>0:  #@grader: test code on how ai[] and ai_trained[] are changed are commented out in this while loop. 
			ai_choice=take_turn(turn_min,turn_max,'smart_ai',ai[nuts])
			#print('\nai at nut ',nuts,' has hat ',ai[nuts]) 
			#print('ai takes ',ai_choice)
			ai_this_round.append([nuts,ai_choice])
			nuts-=ai_choice
			if nuts <=0:
				#print('ai_trained wins\n')
				#print('ai this round:',ai_this_round)
				#print('ai_trained this round:',ai_trained_this_round)
				for i in range(len(ai_this_round)):
					if ai[ai_this_round[i][0]][ai_this_round[i][1]-1]>1:
						ai[ai_this_round[i][0]][ai_this_round[i][1]-1]-=1
				for i in range(len(ai_trained_this_round)):
					ai_trained[ai_trained_this_round[i][0]][ai_trained_this_round[i][1]-1]+=1
				#print('ai after this round:',ai)
				#print('ai_trained after this round:',ai_trained)
				#ai_trained_win+=1
				continue
			else:
				ai_trained_choice = take_turn(turn_min,turn_max,'smart_ai',ai_trained[nuts])
				#print('\nai_trained at nut ',nuts,' has hat ',ai[nuts])
				#print('ai_trained takes ',ai_trained_choice)
				ai_trained_this_round.append([nuts,ai_trained_choice])
				nuts-=ai_trained_choice
			if nuts <=0:
				#print('ai wins\n')
				#print('ai this round:',ai_this_round)
				#print('ai_trained this round:',ai_trained_this_round)
				for i in range(len(ai_trained_this_round)):
					if ai_trained[ai_trained_this_round[i][0]][ai_trained_this_round[i][1]-1]>1:
						ai_trained[ai_trained_this_round[i][0]][ai_trained_this_round[i][1]-1]-=1
				for i in range(len(ai_this_round)):
					ai[ai_this_round[i][0]][ai_this_round[i][1]-1]+=1
				#print('ai after this round:',ai)
				#print('ai_trained after this round:',ai_trained)
				#ai_win+=1
				continue
		ai_this_round.clear()
		ai_trained_this_round.clear()
	#print('ai won ',ai_win,' times')
	#print('ai_trained won ',ai_trained_win,' times')
	#print('ai final hats: ',ai) 
	#print('ai_trained final hats: ',ai_trained) #@grader: uncomment this to see the final trained ai hats
	print('Training complete')
	return ai_trained


# game of nuts settings and menu. 
# nuts_min and nuts_max limit the initial nut #. 
# turn_min and turn_max limit the # of nuts each participant can take each turn.
# player can choose to replay game of nuts.
def main():
	print('Welcome to the game of nuts')
	replay=1
	nuts_min=10
	nuts_max=100
	turn_min=1
	turn_max=3
	while replay==1:
		nuts = get_int(nuts_min,nuts_max,('How many nuts are on the table initially?'+'('+str(nuts_min)+' - '+str(nuts_max)+')'))
		mode=get_int(1,3,'Which mode to play? \n1:human vs human \n2:human vs ai \n3:human vs trained ai\nEnter mode:')
		play(mode,turn_min,turn_max,nuts)
		replay=get_int(0,1,'Play game of nuts again? (1:yes,0:no)')

main()