# -*- coding: utf-8 -*-
"""coursework_1_jhc21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UuGAkjugJCUY5xG7xfse_Z9tn6kry-Qe
"""

import numpy as np 
import random
import matplotlib.pyplot as plt # Graphical library
#from sklearn.metrics import mean_squared_error # Mean-squared error function

"""# Coursework 1 :
See pdf for instructions. 
"""

# WARNING: fill in these two functions that will be used by the auto-marking script
# [Action required]

def get_CID():
  return "02005997" # Return your CID (add 0 at the beginning to ensure it is 8 digits long)

def get_login():
  return "jhc21" # Return your short imperial login

"""## Helper class"""

# This class is used ONLY for graphics
# YOU DO NOT NEED to understand it to work on this coursework

class GraphicsMaze(object):

  def __init__(self, shape, locations, default_reward, obstacle_locs, absorbing_locs, absorbing_rewards, absorbing):

    self.shape = shape
    self.locations = locations
    self.absorbing = absorbing

    # Walls
    self.walls = np.zeros(self.shape)
    for ob in obstacle_locs:
      self.walls[ob] = 20

    # Rewards
    self.rewarders = np.ones(self.shape) * default_reward
    for i, rew in enumerate(absorbing_locs):
      self.rewarders[rew] = 10 if absorbing_rewards[i] > 0 else -10

    # Print the map to show it
    self.paint_maps()

  def paint_maps(self):
    """
    Print the Maze topology (obstacles, absorbing states and rewards)
    input: /
    output: /
    """
    plt.figure(figsize=(15,10))
    plt.imshow(self.walls + self.rewarders)
    plt.show()

  def paint_state(self, state):
    """
    Print one state on the Maze topology (obstacles, absorbing states and rewards)
    input: /
    output: /
    """
    states = np.zeros(self.shape)
    states[state] = 30
    plt.figure(figsize=(15,10))
    plt.imshow(self.walls + self.rewarders + states)
    plt.show()

  def draw_deterministic_policy(self, Policy):
    """
    Draw a deterministic policy
    input: Policy {np.array} -- policy to draw (should be an array of values between 0 and 3 (actions))
    output: /
    """
    plt.figure(figsize=(15,10))
    plt.imshow(self.walls + self.rewarders) # Create the graph of the Maze
    for state, action in enumerate(Policy):
      if(self.absorbing[0,state]): # If it is an absorbing state, don't plot any action
        continue
      arrows = [r"$\uparrow$",r"$\rightarrow$", r"$\downarrow$", r"$\leftarrow$"] # List of arrows corresponding to each possible action
      action_arrow = arrows[action] # Take the corresponding action
      location = self.locations[state] # Compute its location on graph
      plt.text(location[1], location[0], action_arrow, ha='center', va='center') # Place it on graph
    plt.show()

  def draw_policy(self, Policy):
    """
    Draw a policy (draw an arrow in the most probable direction)
    input: Policy {np.array} -- policy to draw as probability
    output: /
    """
    deterministic_policy = np.array([np.argmax(Policy[row,:]) for row in range(Policy.shape[0])])
    self.draw_deterministic_policy(deterministic_policy)

  def draw_value(self, Value):
    """
    Draw a policy value
    input: Value {np.array} -- policy values to draw
    output: /
    """
    plt.figure(figsize=(15,10))
    plt.imshow(self.walls + self.rewarders) # Create the graph of the Maze
    for state, value in enumerate(Value):
      if(self.absorbing[0, state]): # If it is an absorbing state, don't plot any value
        continue
      location = self.locations[state] # Compute the value location on graph
      plt.text(location[1], location[0], round(value,2), ha='center', va='center') # Place it on graph
    plt.show()

  def draw_deterministic_policy_grid(self, Policies, title, n_columns, n_lines):
    """
    Draw a grid representing multiple deterministic policies
    input: Policies {np.array of np.array} -- array of policies to draw (each should be an array of values between 0 and 3 (actions))
    output: /
    """
    plt.figure(figsize=(20,8))
    for subplot in range (len(Policies)): # Go through all policies
      ax = plt.subplot(n_columns, n_lines, subplot+1) # Create a subplot for each policy
      ax.imshow(self.walls+self.rewarders) # Create the graph of the Maze
      for state, action in enumerate(Policies[subplot]):
        if(self.absorbing[0,state]): # If it is an absorbing state, don't plot any action
          continue
        arrows = [r"$\uparrow$",r"$\rightarrow$", r"$\downarrow$", r"$\leftarrow$"] # List of arrows corresponding to each possible action
        action_arrow = arrows[action] # Take the corresponding action
        location = self.locations[state] # Compute its location on graph
        plt.text(location[1], location[0], action_arrow, ha='center', va='center') # Place it on graph
      ax.title.set_text(title[subplot]) # Set the title for the graph given as argument
    plt.show()

  def draw_policy_grid(self, Policies, title, n_columns, n_lines):
    """
    Draw a grid representing multiple policies (draw an arrow in the most probable direction)
    input: Policy {np.array} -- array of policies to draw as probability
    output: /
    """
    deterministic_policies = np.array([[np.argmax(Policy[row,:]) for row in range(Policy.shape[0])] for Policy in Policies])
    self.draw_deterministic_policy_grid(deterministic_policies, title, n_columns, n_lines)

  def draw_value_grid(self, Values, title, n_columns, n_lines):
    """
    Draw a grid representing multiple policy values
    input: Values {np.array of np.array} -- array of policy values to draw
    output: /
    """
    plt.figure(figsize=(20,8))
    for subplot in range (len(Values)): # Go through all values
      ax = plt.subplot(n_columns, n_lines, subplot+1) # Create a subplot for each value
      ax.imshow(self.walls+self.rewarders) # Create the graph of the Maze
      for state, value in enumerate(Values[subplot]):
        if(self.absorbing[0,state]): # If it is an absorbing state, don't plot any value
          continue
        location = self.locations[state] # Compute the value location on graph
        plt.text(location[1], location[0], round(value,1), ha='center', va='center') # Place it on graph
      ax.title.set_text(title[subplot]) # Set the title for the graoh given as argument
    plt.show()

"""## Maze class"""

# This class define the Maze environment

class Maze(object):

  # [Action required]
  def __init__(self):
    """
    Maze initialisation.
    input: /
    output: /
    """
    
    # [Action required]
    # Properties set from the CID
    CID = get_CID()
    y, z = int(CID[-2]), int(CID[-1])
    self._prob_success = 0.8 + 0.02*(9-y) # float
    self._gamma = 0.8 + 0.02*y # float
    self._goal = z%4 # integer (0 for R0, 1 for R1, 2 for R2, 3 for R3)

    # Build the maze
    self._build_maze()
                              

  # Functions used to build the Maze environment 
  # You DO NOT NEED to modify them
  def _build_maze(self):
    """
    Maze initialisation.
    input: /
    output: /
    """

    # Properties of the maze
    self._shape = (13, 10)
    self._obstacle_locs = [
                          (1,0), (1,1), (1,2), (1,3), (1,4), (1,7), (1,8), (1,9), \
                          (2,1), (2,2), (2,3), (2,7), \
                          (3,1), (3,2), (3,3), (3,7), \
                          (4,1), (4,7), \
                          (5,1), (5,7), \
                          (6,5), (6,6), (6,7), \
                          (8,0), \
                          (9,0), (9,1), (9,2), (9,6), (9,7), (9,8), (9,9), \
                          (10,0)
                         ] # Location of obstacles
    self._absorbing_locs = [(2,0), (2,9), (10,1), (12,9)] # Location of absorbing states
    self._absorbing_rewards = [ (500 if (i == self._goal) else -50) for i in range (4) ]
    self._starting_locs = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9)] #Reward of absorbing states
    self._default_reward = -1 # Reward for each action performs in the environment
    self._max_t = 500 # Max number of steps in the environment

    # Actions
    self._action_size = 4
    self._direction_names = ['N','E','S','W'] # Direction 0 is 'N', 1 is 'E' and so on
        
    # States
    self._locations = []
    for i in range (self._shape[0]):
      for j in range (self._shape[1]):
        loc = (i,j) 
        # Adding the state to locations if it is no obstacle
        if self._is_location(loc):
          self._locations.append(loc)
    self._state_size = len(self._locations)

    # Neighbours - each line is a state, ranked by state-number, each column is a direction (N, E, S, W)
    self._neighbours = np.zeros((self._state_size, 4)) 
    
    for state in range(self._state_size):
      loc = self._get_loc_from_state(state)

      # North
      neighbour = (loc[0]-1, loc[1]) # North neighbours location
      if self._is_location(neighbour):
        self._neighbours[state][self._direction_names.index('N')] = self._get_state_from_loc(neighbour)
      else: # If there is no neighbour in this direction, coming back to current state
        self._neighbours[state][self._direction_names.index('N')] = state

      # East
      neighbour = (loc[0], loc[1]+1) # East neighbours location
      if self._is_location(neighbour):
        self._neighbours[state][self._direction_names.index('E')] = self._get_state_from_loc(neighbour)
      else: # If there is no neighbour in this direction, coming back to current state
        self._neighbours[state][self._direction_names.index('E')] = state

      # South
      neighbour = (loc[0]+1, loc[1]) # South neighbours location
      if self._is_location(neighbour):
        self._neighbours[state][self._direction_names.index('S')] = self._get_state_from_loc(neighbour)
      else: # If there is no neighbour in this direction, coming back to current state
        self._neighbours[state][self._direction_names.index('S')] = state

      # West
      neighbour = (loc[0], loc[1]-1) # West neighbours location
      if self._is_location(neighbour):
        self._neighbours[state][self._direction_names.index('W')] = self._get_state_from_loc(neighbour)
      else: # If there is no neighbour in this direction, coming back to current state
        self._neighbours[state][self._direction_names.index('W')] = state

    # Absorbing
    self._absorbing = np.zeros((1, self._state_size))
    for a in self._absorbing_locs:
      absorbing_state = self._get_state_from_loc(a)
      self._absorbing[0, absorbing_state] = 1

    # Transition matrix
    self._T = np.zeros((self._state_size, self._state_size, self._action_size)) # Empty matrix of domension S*S*A
    for action in range(self._action_size):
      for outcome in range(4): # For each direction (N, E, S, W)
        # The agent has prob_success probability to go in the correct direction
        if action == outcome:
          prob = 1 - 3.0 * ((1.0 - self._prob_success) / 3.0) # (theoritically equal to self.prob_success but avoid rounding error and garanty a sum of 1)
        # Equal probability to go into one of the other directions
        else:
          prob = (1.0 - self._prob_success) / 3.0
          
        # Write this probability in the transition matrix
        for prior_state in range(self._state_size):
          # If absorbing state, probability of 0 to go to any other states
          if not self._absorbing[0, prior_state]:
            post_state = self._neighbours[prior_state, outcome] # Post state number
            post_state = int(post_state) # Transform in integer to avoid error
            self._T[prior_state, post_state, action] += prob

    # Reward matrix
    self._R = np.ones((self._state_size, self._state_size, self._action_size)) # Matrix filled with 1
    self._R = self._default_reward * self._R # Set default_reward everywhere
    for i in range(len(self._absorbing_rewards)): # Set absorbing states rewards
      post_state = self._get_state_from_loc(self._absorbing_locs[i])
      self._R[:,post_state,:] = self._absorbing_rewards[i]

    # Creating the graphical Maze world
    self._graphics = GraphicsMaze(self._shape, self._locations, self._default_reward, self._obstacle_locs, self._absorbing_locs, self._absorbing_rewards, self._absorbing)
    
    # Reset the environment
    self.reset()


  def _is_location(self, loc):
    """
    Is the location a valid state (not out of Maze and not an obstacle)
    input: loc {tuple} -- location of the state
    output: _ {bool} -- is the location a valid state
    """
    if (loc[0] < 0 or loc[1] < 0 or loc[0] > self._shape[0]-1 or loc[1] > self._shape[1]-1):
      return False
    elif (loc in self._obstacle_locs):
      return False
    else:
      return True


  def _get_state_from_loc(self, loc):
    """
    Get the state number corresponding to a given location
    input: loc {tuple} -- location of the state
    output: index {int} -- corresponding state number
    """
    return self._locations.index(tuple(loc))


  def _get_loc_from_state(self, state):
    """
    Get the state number corresponding to a given location
    input: index {int} -- state number
    output: loc {tuple} -- corresponding location
    """
    return self._locations[state]

  # Getter functions used only for DP agents
  # You DO NOT NEED to modify them
  def get_T(self):
    return self._T

  def get_R(self):
    return self._R

  def get_absorbing(self):
    return self._absorbing

  # Getter functions used for DP, MC and TD agents
  # You DO NOT NEED to modify them
  def get_graphics(self):
    return self._graphics

  def get_action_size(self):
    return self._action_size

  def get_state_size(self):
    return self._state_size

  def get_gamma(self):
    return self._gamma

  # Functions used to perform episodes in the Maze environment
  def reset(self):
    """
    Reset the environment state to one of the possible starting states
    input: /
    output: 
      - t {int} -- current timestep
      - state {int} -- current state of the envionment
      - reward {int} -- current reward
      - done {bool} -- True if reach a terminal state / 0 otherwise
    """
    self._t = 0
    self._state = self._get_state_from_loc(self._starting_locs[random.randrange(len(self._starting_locs))])
    self._reward = 0
    self._done = False
    return self._t, self._state, self._reward, self._done

  def step(self, action):
    """
    Perform an action in the environment
    input: action {int} -- action to perform
    output: 
      - t {int} -- current timestep
      - state {int} -- current state of the envionment
      - reward {int} -- current reward
      - done {bool} -- True if reach a terminal state / 0 otherwise
    """

    # If environment already finished, print an error
    if self._done or self._absorbing[0, self._state]:
      print("Please reset the environment")
      return self._t, self._state, self._reward, self._done

    # Drawing a random number used for probaility of next state
    probability_success = random.uniform(0,1)

    # Look for the first possible next states (so get a reachable state even if probability_success = 0)
    new_state = 0
    while self._T[self._state, new_state, action] == 0: 
      new_state += 1
    assert self._T[self._state, new_state, action] != 0, "Selected initial state should be probability 0, something might be wrong in the environment."

    # Find the first state for which probability of occurence matches the random value
    total_probability = self._T[self._state, new_state, action]
    while (total_probability < probability_success) and (new_state < self._state_size-1):
     new_state += 1
     total_probability += self._T[self._state, new_state, action]
    assert self._T[self._state, new_state, action] != 0, "Selected state should be probability 0, something might be wrong in the environment."
    
    # Setting new t, state, reward and done
    self._t += 1
    self._reward = self._R[self._state, new_state, action]
    self._done = self._absorbing[0, new_state] or self._t > self._max_t
    self._state = new_state
    return self._t, self._state, self._reward, self._done

"""## DP Agent"""

# This class define the Dynamic Programing agent 

class DP_agent(object):

  # [Action required]
  # WARNING: make sure this function can be called by the auto-marking script
  def solve(self, env):
    """
    Solve a given Maze environment using Dynamic Programming
    input: env {Maze object} -- Maze to solve
    output: 
      - policy {np.array} -- Optimal policy found to solve the given Maze environment 
      - V {np.array} -- Corresponding value function 
    """
    
    # Initialisation (can be edited)
    policy = np.zeros((env.get_state_size(), env.get_action_size())) 
    V = np.zeros(env.get_state_size())
    Vnew = np.copy(V)
    epochs = 0
    threshold = 0.01
    delta = threshold # Ensure delta is bigger than the threshold to start the loop

    #### 
    # Add your code here
    # WARNING: for this agent only, you are allowed to access env.get_T(), env.get_R() and env.get_absorbing()
    ####
    state_size = env.get_state_size()
    action_size = env.get_action_size()
    T = env.get_T()
    R = env.get_R()
    gamma = env._gamma
    absorbing = env.get_absorbing()

    while delta >= threshold:
      epochs += 1 # Increment the epoch
      delta = 0 # Reinitialise delta value
      # For each state
      for prior_state in range(state_size):

        # If not an absorbing state
        if not absorbing[0, prior_state]:
                  
          # Store the previous value for that state
          v = V[prior_state] 

          # Compute Q value
          Q = np.zeros(4) # Initialise with value 0
          for post_state in range(state_size):
            Q += T[prior_state, post_state,:] * (R[prior_state, post_state, :] + gamma * V[post_state])
                
          # Set the new value to the maximum of Q
          V[prior_state]= np.max(Q) 

          # Compute the new delta
          delta = max(delta, np.abs(v - V[prior_state]))
            
            
      # When the loop is finished, fill in the optimal policy
      policy = np.zeros((state_size, action_size)) # Initialisation

      for prior_state in range(state_size):
        # Compute the Q value
        Q = np.zeros(4)
        for post_state in range(state_size):
          Q += T[prior_state, post_state,:] * (R[prior_state, post_state, :] + gamma * V[post_state])
              
        # The action that maximises the Q value gets probability 1
        policy[prior_state, np.argmax(Q)] = 1 
    
    return policy, V

"""## MC agent"""

# This class define the Monte-Carlo agent

class MC_agent(object):

    # [Action required]
    # WARNING: make sure this function can be called by the auto-marking script

    def solve(self, env):
        """
        Solve a given Maze environment using Monte Carlo learning
        input: env {Maze object} -- Maze to solve
        output:
          - policy {np.array} -- Optimal policy found to solve the given Maze environment
          - values {list of np.array} -- List of successive value functions for each episode
          - total_rewards {list of float} -- Corresponding list of successive total non-discounted sum of reward for each episode
        """

        # Initialisation
        state_size = env.get_state_size()
        action_size = env.get_action_size()
        gamma = 0.95
        alpha = 0.03
        
        Q = np.random.rand(state_size, action_size)
        V = np.zeros(state_size)
        values = []
        total_rewards = []
        
        # Create random policy by setting wuarter probability
        policy = 0.25 * np.ones((state_size, action_size))
        
        # Set number of episodes/traces/iterations
        n_episodes = 1000
        
        #Set how epsilon decays after every episode
        eps_const = 0.5*np.ones((n_episodes))
        eps_linear, eps_glie, eps_factor = self._get_eps_decay(n_episodes)
        
        eps_decay = eps_factor
        
        # Run through every step
        for i in range(n_episodes):
            episode, sar = self._generate_episode(policy, env)
            rewards = sar[:, 2]
            total_rewards.append(np.sum(rewards))
            
            s_a_visited = []

            for t, step in enumerate(episode[:-1]):
                state = step["state"]
                action = step["action"]
                
                if not (state, action) in s_a_visited:
                    
                    # Take rewards from this index all the way to the bottom, discount all, this is = G
                    fut_rewards = rewards[t:]
                    discounted_fut_rewards = self._generate_discounted_rewards(fut_rewards, gamma)

                    R = np.sum(discounted_fut_rewards)
                    Q[state, action] = Q[state, action] + alpha * (R - Q[state, action])
                    s_a_visited.append((state, action))
            
            eps = eps_decay[i]
            policy = self._update_policy(policy, Q, episode, eps)
            
            # Create value array for this episode, and append to values list
            V = self._compute_value_function(policy, Q)
            values.append(V)

        mc_policy = policy
        mc_values = values
        total_rewards

        return mc_policy, mc_values, total_rewards
    
    
    def _compute_value_function(self, policy, Q):
        state_size = np.shape(policy)[0]
        action_size = np.shape(policy)[1]
        V = np.zeros(state_size)
        for state in range(state_size):
            for action in range(action_size):
                V[state] += policy[state, action] * Q[state, action]
        return V

                  
    def _generate_discounted_rewards(self, fut_rewards, gamma):
        
        discounted_fut_rewards = []
        
        for j in range(len(fut_rewards)):
            discount = gamma**j
            discounted_fut_rewards.append(discount * fut_rewards[j])
            
        discounted_fut_rewards = np.array(discounted_fut_rewards)
        
        return discounted_fut_rewards
        
        
    def _generate_episode(self, policy, env):

        t, state, reward, done = env.reset()
        episode = []
        sar_list = []
        
        while not done:
            
            action = self._select_action_from_policy(policy, state)
            t, next_state, next_reward, done = env.step(action)
            episode.append({"t": t, "state": state, "reward": next_reward, "done": done, "action": action})
            sar_list.append([state, action, next_reward])

            state = next_state

        sar = np.array(sar_list)

        return episode, sar


    def _select_action_from_policy(self, policy, state):
        
        probabilities = policy[state, :]
        action = np.random.choice(range(len(probabilities)), p=probabilities)
        
        return action


    def _update_policy(self, current_policy, Q, episode, eps):
        
        policy = current_policy
    
        for t, step in enumerate(episode):
        
            state = step["state"]
            max_Q = np.max(Q[state, :])
            a_best = np.where(Q[state, :] == max_Q)[0][0]

            for a in range(np.shape(policy)[1]):
                if a == a_best:
                    policy[state, a] = 1 - eps + eps / np.shape(policy)[1]
                else:
                    policy[state, a] = eps / np.shape(policy)[1]
                    
        return policy
    
    def _get_eps_decay(self, n_episodes):
        eps_linear = np.linspace(1, 0.05, n_episodes)
        eps_glie = np.ones(eps_linear.shape)
        eps_factor = np.ones(eps_linear.shape)
        factor = np.power(0.05, 1/n_episodes)

        for k in range(1, len(eps_linear)):
            eps_glie[k] = eps_glie[k - 1] / k
            eps_factor[k] = eps_factor[k - 1] * factor
        
        return eps_linear, eps_glie, eps_factor

"""## TD agent"""

# This class define the Temporal-Difference agent

class TD_agent(object):

    # [Action required]
    # WARNING: make sure this function can be called by the auto-marking script
    def solve(self, env):
        """
        Solve a given Maze environment using Temporal Difference learning
        input: env {Maze object} -- Maze to solve
        output: 
          - policy {np.array} -- Optimal policy found to solve the given Maze environment 
          - values {list of np.array} -- List of successive value functions for each episode 
          - total_rewards {list of float} -- Corresponding list of successive total non-discounted sum of reward for each episode 
        """
      
        # Initialisation 
        state_size = env.get_state_size()
        action_size = env.get_action_size()
        gamma = 0.95
        alpha = 0.3
        
        Q = np.random.rand(state_size, action_size)
        V = np.zeros(state_size)
        values = []
        total_rewards = []
        
        # Create random policy by setting wuarter probability
        policy = 0.25 * np.ones((state_size, action_size))
        
        # Set number of episodes/traces/iterations
        n_episodes = 1000
        
        #Set how epsilon decays after every episode
        eps_linear, eps_glie, eps_factor = self._get_eps_decay(n_episodes)
        
        eps_decay = eps_factor

        # Run through every step
        for i in range(n_episodes):       
            
            episode = []
            sar_list = []
            eps = eps_decay[i]
            t, state, reward, done = env.reset()
            
            while not done:
                
                action = self._select_action_from_policy(policy, state)
                t, next_state, next_reward, done = env.step(action)
                R = next_reward
                next_action = self._select_action_from_policy(policy, next_state)
                
                Q[state, action] = Q[state, action] + alpha * (R + gamma * Q[next_state, next_action] - Q[state, action])
                                    
                episode.append({"t": t, "state": state, "reward": next_reward, "done": done, "action": action})
                sar_list.append([state, action, next_reward])
                  
                state = next_state
                action = next_action
                
            policy = self._update_policy(policy, Q, episode, eps)
            
            sar = np.array(sar_list)
            rewards = sar[:, 2]
            total_rewards.append(np.sum(rewards))
      
            # Create value array for this episode, and append to values list
            V = self._compute_value_function(policy, Q)
            values.append(V)
            
        return policy, values, total_rewards


    def _update_policy(self, current_policy, Q, episode, eps):
     
        policy = current_policy
    
        for t, step in enumerate(episode):
        
            state = step["state"]
            max_Q = np.max(Q[state, :])
            a_best = np.where(Q[state, :] == max_Q)[0][0]
    
            for a in range(np.shape(policy)[1]):
                if a == a_best:
                    policy[state, a] = 1 - eps + eps / np.shape(policy)[1]
                else:
                    policy[state, a] = eps / np.shape(policy)[1]
                    
        return policy
    
    
    def _select_action_from_policy(self, policy, state):
        
        probabilities = policy[state, :]
        action = np.random.choice(range(len(probabilities)), p=probabilities)
        
        return action
    
    def _get_eps_decay(self, n_episodes):
        eps_linear = np.linspace(1, 0.05, n_episodes)
        eps_glie = np.ones(eps_linear.shape)
        eps_factor = np.ones(eps_linear.shape)
        factor = np.power(0.05, 1/n_episodes)

        for k in range(1, len(eps_linear)):
            eps_glie[k] = eps_glie[k - 1] / k
            eps_factor[k] = eps_factor[k - 1] * factor
        
        return eps_linear, eps_glie, eps_factor
    
    
    def _compute_value_function(self, policy, Q):
        state_size = np.shape(policy)[0]
        action_size = np.shape(policy)[1]
        V = np.zeros(state_size)
        for state in range(state_size):
            for action in range(action_size):
                V[state] += policy[state, action] * Q[state, action]
        return V

"""## Example main"""

# Example main (can be edited)

### Question 0: Defining the environment

print("Creating the Maze:\n")
maze = Maze()


### Question 1: Dynamic programming

dp_agent = DP_agent()
dp_policy, dp_value = dp_agent.solve(maze)

print("Results of the DP agent:\n")
maze.get_graphics().draw_policy(dp_policy)
maze.get_graphics().draw_value(dp_value)


### Question 2: Monte-Carlo learning

mc_agent = MC_agent()
mc_policy, mc_values, total_rewards = mc_agent.solve(maze)

print("Results of the MC agent:\n")
maze.get_graphics().draw_policy(mc_policy)
maze.get_graphics().draw_value(mc_values[-1])


# ### Question 3: Temporal-Difference learning

td_agent = TD_agent()
td_policy, td_values, total_rewards = td_agent.solve(maze)

print("Results of the TD agent:\n")
maze.get_graphics().draw_policy(td_policy)
maze.get_graphics().draw_value(td_values[-1])