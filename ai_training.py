import random


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


def take_turn(min,max,type,hat):
		choice = 0
		if type=='random_ai':
			choice = random.randrange(min,max,1)
		elif type=='ai':
			choice = random.choices([i for i in range(int(min),int(max)+1,1)],weights=[hat[0],hat[1],hat[2]],k=1)[0]
		else:
			prompt = str(type)+': How many nuts do you take?  '+'('+ str(min) +'-'+ str(max) +')'
			choice = get_int(min,max,prompt)
		return choice

	
def play(mode,turn_min,turn_max,nuts):
	if mode ==1:
		human_vs_human(turn_min,turn_max,nuts)
	elif mode==2:
		human_vs_ai(turn_min,turn_max,nuts)
	elif mode==3:
		ai_vs_ai(turn_min,turn_max,nuts)
	elif mode==4:
		bot_vs_ai(turn_min,turn_max,nuts)


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


def human_vs_ai(turn_min,turn_max,nuts):
	while nuts>0:

			nuts-=take_turn(turn_min,turn_max,'Player 1','')
			if nuts <=0:
					print('Player 1 loses')
					break
			else:
				print('\nThere are ',nuts,' nuts on the table')
				ai_choice= take_turn(turn_min,turn_max,'random_ai','')
				print('ai takes ',ai_choice,' nuts')
				nuts-=ai_choice
			if nuts <=0:
				print('ai loses')
				break
			else:
				print('\nThere are ',nuts,' nuts on the table')

def train_ai(turn_min,turn_max,nuts,iteration):

	ai=[0]
	ai_trained=[0]
	ai_this_round=[]
	ai_trained_this_round=[]
	total_nuts=int(nuts)
	
	for i in range(nuts):
		ai.append([1 for i in range(turn_max-turn_min+1)])
		ai_trained.append([1 for i in range(turn_max-turn_min+1)])
	ai_win=0
	ai_trained_win=0

	for i in range(iteration):
		nuts=int(total_nuts)
		while nuts>0:
			ai_choice=take_turn(turn_min,turn_max,'ai',ai[nuts])
			print('\nai at nut ',nuts,' has weights ',ai[nuts])
			print('ai takes ',ai_choice)
			ai_this_round.append([nuts,ai_choice])
			nuts-=ai_choice
			if nuts <=0:
				print('ai_trained wins\n')
				print('ai this round:',ai_this_round)
				print('ai_trained this round:',ai_trained_this_round)
				for i in range(len(ai_this_round)):
					if ai[ai_this_round[i][0]][ai_this_round[i][1]-1]>1:
						ai[ai_this_round[i][0]][ai_this_round[i][1]-1]-=1
				for i in range(len(ai_trained_this_round)):
					ai_trained[ai_trained_this_round[i][0]][ai_trained_this_round[i][1]-1]+=1
				print('ai after this round:',ai)
				print('ai_trained after this round:',ai_trained)
				ai_trained_win+=1
				continue
			else:
				ai_trained_choice = take_turn(turn_min,turn_max,'ai',ai_trained[nuts])
				print('\nai_trained at nut ',nuts,' has weights ',ai[nuts])
				print('ai_trained takes ',ai_trained_choice)
				ai_trained_this_round.append([nuts,ai_trained_choice])
				nuts-=ai_trained_choice

			if nuts <=0:
				print('ai wins\n')
				print('ai this round:',ai_this_round)
				print('ai_trained this round:',ai_trained_this_round)
				for i in range(len(ai_trained_this_round)):
					if ai_trained[ai_trained_this_round[i][0]][ai_trained_this_round[i][1]-1]>1:
						ai_trained[ai_trained_this_round[i][0]][ai_trained_this_round[i][1]-1]-=1
				for i in range(len(ai_this_round)):
					ai[ai_this_round[i][0]][ai_this_round[i][1]-1]+=1
				print('ai after this round:',ai)
				print('ai_trained after this round:',ai_trained)
				ai_win+=1
				continue

		ai_this_round.clear()
		ai_trained_this_round.clear()
	#print(ai_win)
	#print(ai_trained_win)
	return ai_trained


def ai_vs_ai(turn_min,turn_max,nuts):
	times_to_train=2
	ai_trained = train_ai(turn_min,turn_max,nuts,times_to_train)
	total_nuts=int(nuts)
	play_again=1
	while play_again==1:
		nuts = int(total_nuts)
		while nuts>0:
			nuts-=take_turn(1,3,'Player 1','')
			if nuts <=0:
				print('Player 1 loses')
				play_again=get_int(0,1,'Play trained ai again? (1:yes,0:no)')
				break
			else:
				print('\nThere are ',nuts,' nuts on the table')
				ai_choice= take_turn(1,3,'ai',ai_trained[nuts-1])
				print('ai takes ',ai_choice,' nuts')
				nuts-=ai_choice
			if nuts <=0:
				print('ai loses')
				play_again=get_int(0,1,'Play trained ai again? (1:yes,0:no)')
				break
			else:
				print('\nThere are ',nuts,' nuts on the table')		


def main():
	print('Welcome to the game of nuts')
	replay=1
	nuts_min=10
	nuts_max=100
	turn_min=1
	turn_max=3
	while replay==1:
		nuts = get_int(nuts_min,nuts_max,('How many nuts are on the table initially?'+'('+str(nuts_min)+' - '+str(nuts_max)+')'))
		mode=get_int(1,3,'enter mode \n1:human vs human \n2:human vs ai \n3:human vs trained ai\n')
		play(mode,turn_min,turn_max,nuts)
		replay=get_int(0,1,'Play game of nuts again? (1:yes,0:no)')
main()
