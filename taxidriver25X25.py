#import libraries
import numpy as np
import time
#define the shape of the environment (i.e., its states)
environment_rows = 26
environment_columns = 26
#Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a) 
#The array contains 11 rows and 11 columns (to match the shape of the environment), as well as a third "action" dimension.
#The "action" dimension consists of 4 layers that will allow us to keep track of the Q-values for each possible action in
#each state (see next cell for a description of possible actions). 
#The value of each (state, action) pair is initialized to 0.

q_values = np.zeros((environment_rows, environment_columns, 4))
q_values2 = np.zeros((environment_rows, environment_columns, 4))
#define actions
#numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']
#Create a 2D numpy array to hold the rewards for each state. 
#The array contains 11 rows and 11 columns (to match the shape of the environment), and each value is initialized to -100.
rewards = np.full((environment_rows, environment_columns), -1.)
#rewards[0, 5] = 100. #set the reward for the packaging area (i.e., the goal) to 100
rewards[25][15]=1000.
aisles = {} #store locations in a dictionary
aisles[0] = [i for i in range(0, 26)]
aisles[1] = [1,2,3,4,14]
aisles[2] = [1, 7, 9 ,15,16,17,18,19,20]
aisles[3] =[21,22,20,19,18]
aisles[4] = [3, 7, 15]
aisles[5] = [1,5,8,15]
aisles[6] = [3,6,9,12,15,18,21,24]
aisles[7] = [1,3,5,7,9,11,13,15,17,19,21,23,25]
aisles[8] = [3, 7]
aisles[9] = [4,5,6,7,8,9,15]
aisles[10] = [7,8,9,10,20,21,22,19]
aisles[11] = [0,1,3,5,6,24,12,17]
aisles[12] = [24,23,22,21,20]
aisles[13] = [3,6,9,12,15,18,21,24]
aisles[14] = [0,15,13,12,11,10,2,3,21,4]
aisles[15] = [15,13,12,11,10,2,23,3,4,21]
aisles[16] = [1,6,7,9,15,17,20]
aisles[17] = [15,13,12,11,10,2,23,3,4,21,22,23,24,25]
aisles[18] = [0,15,13,12,11,10,2,3,4,21]
aisles[19] = [15,13,12,11,10,2,3,4,21]
aisles[20] = [15,13,12,11,10,21]
aisles[21] = [0,2,23,3,4,21]
aisles[22] = [1,3,5,7,9,11,13,15,17,19,21,23,25]
aisles[23] = [0,15,13,12,11,10,23,2,3,4,21]
aisles[24] = [0,15,13,12,11,10,2,3,4]
aisles[25] = [0,14]



#set the rewards for all aisle locations (i.e., white squares)
for row_index in range(0, 26):
  for column_index in aisles[row_index]:
    rewards[row_index, column_index] = -100.
rewards[0][5] = 100.
rewards[25][15]=100.
rewards[5][0]=-100
#print rewards matrix
for row in rewards:
  print(row)
rewards[0][5] = -1.

#define a function that determines if the specified location is a terminal state
def is_terminal_state(current_row_index, current_column_index):
  #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True
def passenger(current_row_index, current_column_index):
  if rewards[current_row_index, current_column_index] == -1. or rewards[current_row_index, current_column_index] == 100.:
    return False
  else:
    return True

#define a function that will choose a random, non-terminal starting location
def get_starting_location():
  #get a random row and column index
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  #continue choosing random row and column indexes until a non-terminal state is identified
  #(i.e., until the chosen state is a 'white square').
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index
def get_ending_location():
  #get a random row and column index
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  #continue choosing random row and column indexes until a non-terminal state is identified
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index
#define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
def get_next_action(current_row_index, current_column_index, epsilon):
  #if a randomly chosen value between 0 and 1 is less than epsilon, 
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(4)

#define a function that will get the next location based on the chosen action
def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

#Define a function that will get the shortest path between the destination and passenger
def get_shortest_path(start_row_index, start_column_index):
  rewards[0][5]=-1.
  rewards[25][15]=100.
  
  #return immediately if this is an invalid starting location
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else: #if this is a 'legal' starting location
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    #shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(current_row_index, current_column_index):
      shortest_path.append([current_row_index, current_column_index])
      #get the best action to take
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
     
      #print(current_row_index, current_column_index) 
     # time.sleep(.5)
    #print("finished")
    rewards[25][15]=-1.
    rewards[0][5]=100.

    return get_shortest_path2(current_row_index, current_column_index, shortest_path)
#define a function that determines if the specified location is a terminal state
def is_terminal_state2(current_row_index, current_column_index):
  #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True

#define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
def get_next_action2(current_row_index, current_column_index, epsilon):
  #if a randomly chosen value between 0 and 1 is less than epsilon, 
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() < epsilon:
    return np.argmax(q_values2[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(4)

#define a function that will get the next location based on the chosen action
def get_next_location2(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

#Define a function that will get the shortest path between the passenger and destination
def get_shortest_path2(start_row_index, start_column_index,shortest_path):

  current_row_index, current_column_index = start_row_index, start_column_index
 # shortest_path = []
  shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
  while not is_terminal_state(current_row_index, current_column_index):
      #get the best action to take
    action_index = get_next_action2(current_row_index, current_column_index, 1.)
      #move to the next location on the path, and add the new location to the list
    current_row_index, current_column_index = get_next_location2(current_row_index, current_column_index, action_index)
    shortest_path.append([current_row_index, current_column_index])
    #print(current_row_index, current_column_index) 
   # time.sleep(.5)
  #print("finished")
  
  return shortest_path
#define training parameters
epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9 #discount factor for future rewards
learning_rate = 0.9 #the rate at which the AI agent should learn

#run through training episodes
for episode in range(1000000):
  print(episode)
  rewards[25][15]=100.
  rewards[0][5]=-1.
  #get the starting location for this episode
  row_index, column_index = get_starting_location()

  #continue taking actions (i.e., moving) until we reach a terminal state

  while not is_terminal_state(row_index, column_index):
    #choose which action to take (i.e., where to move next)
    action_index = get_next_action(row_index, column_index, epsilon)

    #perform the chosen action, and transition to the next state (i.e., move to the next location)
    old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
    row_index, column_index = get_next_location(row_index, column_index, action_index)
    
    #receive the reward for moving to the new state, and calculate the temporal difference
    reward = rewards[row_index, column_index]
    old_q_value = q_values[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_row_index, old_column_index, action_index] = new_q_value

  rewards[25][15]=-1.
  rewards[0][5]=100.
  while not is_terminal_state(row_index, column_index):
    #choose which action to take (i.e., where to move next)
    action_index = get_next_action2(row_index, column_index, epsilon)

    #perform the chosen action, and transition to the next state (i.e., move to the next location)
    old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
    row_index, column_index = get_next_location2(row_index, column_index, action_index)
    
    #receive the reward for moving to the new state, and calculate the temporal difference
    reward = rewards[row_index, column_index]
    old_q_value = q_values2[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values2[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values2[old_row_index, old_column_index, action_index] = new_q_value
print('Training complete!')
#display a few shortest paths
rewards[0][5]=5.
rewards[25][15]=6.
count=0
for row in rewards:
  for item in row:
    if item == -1.:
      print("-",end=" ")
    elif item == 5.:
      print("D",end=" ")
    elif item == 6.:
      print("P",end=" ")
    else:
      print("*",end=" ")
  print(count)
  count=count+1
  print("\n")
print("\n")
rewards[0][5]=-1.
rewards[25][15]=100.
print("Path starting at [25,25]")

print(get_shortest_path(25, 25)) #starting at row 3, column 9
print("\n")

print("Path starting at [3,9]")
print(get_shortest_path(3, 9)) #starting at row 3, column 9
print("\n")
print("Path starting at [1,5]")
print(get_shortest_path(1, 5)) #starting at row 5, column 0
print("\n")

temprow, tempcol=get_starting_location()
print("Path starting at the random values", temprow,tempcol)
print(get_shortest_path(temprow, tempcol)) 
#Get user inputs for starting points
while True:
    try:
        x, y = map(int, input("Enter a x,y value to start at separate by a space: ").split())
        break
    except ValueError:
        print("Invalid input. Please enter two integers separated by a space.")
print(get_shortest_path(x, y))
