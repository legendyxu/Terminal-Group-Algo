import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, BITS, CORES
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        BITS = 1
        CORES = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []

    
        

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        '''c = gamelib.GameState(self.config, game_state.serialized_string)
        c.game_map.remove_unit( )'''
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.ultimate_strategy(game_state)

        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

   














    # this part is used to add new features from up to down
    # index = 0[not attack],1[left_wint],2[right_wing],3[left_side], 4[right_side]
    attack_index = 0
    left_wing_attack_deploy_location = [[16,2], [17,3]]
    right_wing_attack_deploy_location = [[11,2], [10,3]]
    scrambleers_deploy_location1  = []
    scrambleers_deploy_location2  = []

    attack_next_turn = 0
    on_left_wing_attack_spawn_pos = [[0, 13], [2, 13], [25, 13], [26, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [6, 9], [21, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [10, 6], [11, 6], [16, 6], [17, 6], [18, 6]]
    on_right_wing_attack_spawn_pos = [[0, 13], [1, 13], [2, 13], [25, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [6, 9], [21, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [10, 6], [11, 6], [16, 6], [17, 6], [18, 6]]
    on_left_side_attack_spawn_pos = [[0, 13], [1, 13], [2, 13], [25, 13], [26, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [6, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [10, 6], [11, 6], [16, 6], [17, 6], [18, 6]]
    on_right_side_attack_spawn_pos = [[0, 13], [1, 13], [2, 13], [25, 13], [26, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [21, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [10, 6], [11, 6], [16, 6], [17, 6], [18, 6]]
    mid_pos = [[13,4], [14,4]]
    number_of_scrambleer_spawn = 0
    left_corner = [1,13]
    right_corner = [26,13]
    left_side = [6,9]
    right_side = [21,9]
    def spawn_tier1_defenses(self, game_state):
        tier1_filter_pos = [[0, 13], [1, 13], [2, 13], [4, 13], [23, 13], [25, 13], [26, 13], [27, 13], [3, 12], [5, 12], [22, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [6, 9], [21, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [10, 6], [11, 6], [16, 6], [17, 6], [18, 6],[11,7], [16,7]]
        tier1_destructor_pos = [[4, 12], [23, 12], [11, 5], [16, 5], [3, 13], [24, 13], [10, 5], [17, 5]]
        y = game_state.attempt_spawn(DESTRUCTOR, tier1_destructor_pos)
        x = game_state.attempt_spawn(FILTER, tier1_filter_pos)
        return x + y
    def spawn_tier2_defenses(self, game_state):
        #pleasy enter the pos in symmetric way from up to down
        upgrade_filter_pos = [[1, 13], [26, 13], [2, 13], [25, 13], [27, 13], [0, 13]]
        upgrade_destructor_pos = [[4, 12], [23, 12], [11, 5], [16, 5], [3, 13], [24, 13], [10, 5], [17, 5]]
        tier2_filter_pos = [[6, 12], [21, 12], [7, 11], [20, 11], [8, 10], [19, 10], [9, 9], [18, 9], [10, 8], [17, 8]]
        tier2_destructor_pos = [[6, 11], [21, 11], [7, 10], [20, 10], [8, 9], [19, 9], [9, 8], [18, 8], [10, 7], [17, 7]]
        game_state.attempt_upgrade(upgrade_filter_pos)
        game_state.attempt_upgrade(upgrade_destructor_pos)  
        for x in range(10): # range is the length of filters pos
            a = game_state.attempt_spawn(FILTER, tier2_filter_pos[x])
            b = game_state.attempt_spawn(DESTRUCTOR, tier2_destructor_pos[x])
        for x in range(10): # range is the length of filters pos
            c = game_state.attempt_upgrade(tier2_filter_pos[x])
            d = game_state.attempt_upgrade(tier2_destructor_pos[x])
        return a+b+c+d
    def spawn_tier1_encryptor(self,game_state):
        #pleasy enter the pos in symmetric way from up to down
        tier1_encryptor_pos = [[13, 1], [14, 1], [11, 4], [12, 4], [15, 4]]
        game_state.attempt_spawn(ENCRYPTOR, tier1_encryptor_pos)
    def spawn_tier2_encryptor(self,game_state):
        #pleasy enter the pos in symmetric way from up to down
        tier2_encryptor_pos = [[16, 4], [12, 3], [15, 3], [12, 1], [15, 1], [13, 0], [14, 0]]
        game_state.attempt_spawn(ENCRYPTOR, tier2_encryptor_pos)
    def attack(self,game_state):
        self.wing_attack(game_state)
        self.attack_next_turn = 0
    def spawn_remove_mid(self,game_state):
        game_state.attempt_spawn(FILTER,self.mid_pos)
        game_state.attempt_remove(self.mid_pos)
        x = game_state.attempt_spawn(FILTER,[12,4])
        if x == 1:
            game_state.attempt_remove([12,4])
        y = game_state.attempt_spawn(FILTER,[15,4])
        if y == 1:
            game_state.attempt_remove([15,4])
    def attack_defense_ready(self,game_state):
        temp = 0
        if self.attack_index == 1:
            game_state.attempt_spawn(FILTER, self.on_left_wing_attack_spawn_pos)
            for pos in self.on_left_wing_attack_spawn_pos:
                if game_state.contains_stationary_unit(pos) == False:
                    temp += 1
        if self.attack_index == 2:
            game_state.attempt_spawn(FILTER, self.on_left_wing_attack_spawn_pos)
            for pos in self.on_left_wing_attack_spawn_pos:
                if game_state.contains_stationary_unit(pos) == False:
                    temp += 1
        if self.attack_index == 3:
            game_state.attempt_spawn(FILTER, self.on_left_wing_attack_spawn_pos)
            for pos in self.on_left_wing_attack_spawn_pos:
                if game_state.contains_stationary_unit(pos) == False:
                    temp += 1
        if self.attack_index == 4:
            game_state.attempt_spawn(FILTER, self.on_left_wing_attack_spawn_pos)
            for pos in self.on_left_wing_attack_spawn_pos:
                if game_state.contains_stationary_unit(pos) == False:
                    temp += 1
        return temp


    def wing_attack(self,game_state):
        self.spawn_remove_mid(game_state)
        if self.attack_index == 1:
            #game_state.attempt_spawn(EMP, self.left_wing_attack_deploy_location, 3)
            game_state.attempt_spawn(PING,self.left_wing_attack_deploy_location[0], game_state.number_affordable(PING)/2)
            game_state.attempt_spawn(PING,self.left_wing_attack_deploy_location[1], game_state.number_affordable(PING))  
        else:
            #game_state.attempt_spawn(EMP, self.right_wing_attack_deploy_location, 3)
            game_state.attempt_spawn(PING,self.right_wing_attack_deploy_location[0], game_state.number_affordable(PING)/2)
            game_state.attempt_spawn(PING,self.right_wing_attack_deploy_location[1], game_state.number_affordable(PING))

    def detect(self,game_state):
        right_wing_detect = self.detect_enemy_unit(game_state, unit_type=DESTRUCTOR, valid_x=[23,24,25,26,27], valid_y=None)
        left_wing_detect = self.detect_enemy_unit(game_state, unit_type=DESTRUCTOR, valid_x=[0,1,2,3,4], valid_y=None)
        
        left_attack_start = [6, 10]
        left_side_path = game_state.find_path_to_edge(left_attack_start, game_state.game_map.TOP_RIGHT)
        left_side_end = left_side_path[-1]
        left_success = game_state.is_on_edge(left_side_end, game_state.game_map.TOP_RIGHT)
        
        right_attack_start = [20, 9]
        right_side_path = game_state.find_path_to_edge(right_attack_start, game_state.game_map.TOP_LEFT)
        right_side_end = right_side_path[-1]
        right_success = game_state.is_on_edge(left_side_end, game_state.game_map.TOP_RIGHT)
        
        if (left_success and (not(right_success) or len(left_side_path) <= len(right_side_path))):
            self.attack_index = 4 # right side to enemy's left
        elif (right_success and (not(left_success) or len(right_side_path) <= len(left_side_path))):
            self.attack_index = 3 # left side to enemy's right
        elif right_wing_detect < left_wing_detect:
            self.attack_index = 2 # attack right wing
        elif right_wing_detect > left_wing_detect:
            self.attack_index = 1 # attack left wing
        else:
            self.attack_index = random.randint(1,3)
    
    def spawn_scramblers(self, game_state):
        """
        Send out Scramblers at random locations to defend our base from enemy moving units.
        """ 
        enemy_bits = game_state(BITS,1)
        if enemy_bits >= 15:
            game_state.attempt_spawn(SCRAMBLER, self.scrambleers_deploy_location1,2)
            game_state.attempt_spawn(SCRAMBLER, self.scrambleers_deploy_location2,2)
            self.number_of_scrambleer_spawn = 4
        elif enemy_bits >= 9:
            game_state.attempt_spawn(SCRAMBLER, self.scrambleers_deploy_location1,1)
            game_state.attempt_spawn(SCRAMBLER, self.scrambleers_deploy_location2,1)
            self.number_of_scrambleer_spawn = 2
            """
            We don't have to remove the location since multiple information 
            units can occupy the same space.
            """
        '''if game_state.turn_number % 2 == 1:
                    # To simplify we will just check sending them from back left and right
                ping_spawn_location_options = [[13, 0], [14, 0]]
                best_location = self.least_damage_spawn_location(game_state, ping_spawn_location_options)
                game_state.attempt_spawn(PING, best_location, 1000)

                # Lastly, if we have spare cores, let's build some Encryptors to boost our Pings' health.
                encryptor_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
                game_state.attempt_spawn(ENCRYPTOR, encryptor_locations)'''
    def do_prep_side_attack(self, game_state, target_edge):
        ## on prepping side attack
        if target_edge == game_state.game_map.TOP_RIGHT:
            game_state.attempt_remove([6, 9])
        elif target_edge == game_state.game_map.TOP_LEFT:
            game_state.attempt_remove([21, 9])

    def ultimate_strategy(self, game_state):
        """
        |--------------- {overall strategy} -----------------------------------------------------
        |(basic defence always needs to be checked before doing anything)
        |
        |(if having more than 10 cores, using excessive cores to build tier2 defenses)
        |-these 10 cores are stored for emergency uses(ig.the enemy breaks our tier1 defense) 
        |-when building tier 2 defenses, we will try to build them in symmetric way to minimizes uncertainties
        |-always check if tier1 defenses are broken before doing tier2 defense build.
        |(deploying scramblers to defend)
        |-since the enemy bits decrease 1/4 each turn, they will try to avoid gaining negative amount of bits next turn, 
        | which means if they will gain - bits next turn, they will surely attack this turn.
        |-we deploy 2 scramblers in the middle if the enemy has more than 9 bits
        |-note that if they deploy units before reaching 9 bits, they wont have an effective attck.
        |(if tier2 defences are all spawned, saving cores for the encoders and deploying scramblers to defend)
        |
        |(if we have at least tier1 encoders, or have enought cores to spawn tier 1 encoders, and having enough bits to launch a certain attack, do it!)
        |
        |(if all the defences are intact, start saving cores for the tier2 encoders)
        |
        |(if we are gonna gain negative bits next turn for one of following):
        |-if we have as least a certain amount of encoders(# depends on the actual attributes of destructor and filter) [ half-attack]
        |-else
        |	-if the enemy has too few bits(meaning they just attacked) [we deploy extra pings or emp{since we dont have to deploy scramblers]
        |	-if the enemy has more than 10+ bits, add extra scramblers.
        |
        |suggestions: we can add expectations dmg values to each attack, so that if they didnt meet the expectation value for a certain attack,
        |             we will change attack strategy.
        |
        |-one equation that you may find helpful:
        |this turn bits3/4 + bits gain next turn = next turn bits
        |this turn bits3/4 - this turn bits spent3/4  + bits gain on next turn = next turn bits 
        |so if we spend a single bit, we will gain less bits next turn.(so strategy needs to be changed)
        |
        |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        |
        """
        # First, place basic defenses
        if self.attack_next_turn == 0:
            self.spawn_tier1_defenses(game_state)     
        else:  # this is when we attack
            attack_not_ready = self.attack_defense_ready(game_state)
            # If the enemy has at least 9 BITS, spawn scramblers to defend
            # if game_state.get_resource(BITS, 1) >= 9:
                # self.spawn_scramblers(game_state) # this scrambler spawn function needs to be improved
            if game_state.get_resource(BITS, 0) >= 13:
                if attack_not_ready == 0:
                    self.attack(game_state)

        ## detect whether or not to attack
        if game_state.project_future_bits(1,0,game_state.get_resource(BITS,0)-self.number_of_scrambleer_spawn) >= 13:
            self.attack_next_turn = 1
            self.detect(game_state)
            if self.attack_index == 1:
                game_state.attempt.remove(self.left_corner)
            elif self.attack_index == 2:
                game_state.attempt.remove(self.right_corner)
            elif self.attack_index == 3:
                game_state.attempt.remove(self.left_side)
            else:
                game_state.attempt.remove(self.right_side)
        else:
            self.attack_next_turn = 0

        self.spawn_tier1_encryptor(game_state)
        self.spawn_tier2_encryptor(game_state)
        self.spawn_tier2_defenses(game_state)
            
    # end of adding new features

#try if it works this time
































    def build_defences(self, game_state):
        """
        Build basic defenses using hardcoded locations.
        Remember to defend corners and avoid placing units in the front where enemy EMPs can attack them.
        """
        # Useful tool for setting up your base locations: https://www.kevinbai.design/terminal-map-maker
        # More community tools available at: https://terminal.c1games.com/rules#Download

        # Place destructors that attack enemy units
        destructor_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
        # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)
        
        # Place filters in front of destructors to soak up damage for them
        filter_locations = [[8, 12], [19, 12]]
        game_state.attempt_spawn(FILTER, filter_locations)
        # upgrade filters so they soak more damage
        game_state.attempt_upgrade(filter_locations)

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build destructor one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(DESTRUCTOR, build_location)

    def stall_with_scramblers(self, game_state):
        """
        Send out Scramblers at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        # Remove locations that are blocked by our own firewalls 
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        # While we have remaining bits to spend lets send out scramblers randomly.
        while game_state.get_resource(BITS) >= game_state.type_cost(SCRAMBLER)[BITS] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            
            game_state.attempt_spawn(SCRAMBLER, deploy_location)
            """
            We don't have to remove the location since multiple information 
            units can occupy the same space.
            """

    def emp_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our EMP's can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.BITS] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.BITS]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn EMPs next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(EMP, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR, game_state.config).damage_i
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at: https://docs.c1games.com/json-docs.html
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
