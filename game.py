import random
import os
import platform
import hfclib
import tools

class Elements():
    def __init__(self):
        self.elements_file = hfclib.parseHfc(hfc_path="elements.hfc")

        self.types = []

        self.element_list = hfclib.getSections(self.elements_file)
        
        for elem in self.element_list:
            elem_stat = hfclib.getVariables(section_name=elem, hfc_list=self.elements_file)

            name = elem
            try:
                weakness = elem_stat["weakness"]
                destroys = elem_stat["destroys"]
            except KeyError:
                print(f"elements.hfc is bad!")
                exit(-1)

            # Checking if weakness and destroys has valid elements
            if weakness in self.element_list and destroys in self.element_list:
                self.types.append(Entity(name=name, weakness=weakness, destroys=destroys))
            else:
                print(f"{name} has invalid configuration. Check if 'weakness' and 'destroys' exists on elements.hfc.")
                exit(-1)


class Entity():
    def __init__(self, name: str, weakness: str, destroys: str):
        self.name = name
        self.weakness = weakness
        self.destroys = destroys


class Element():
    
    def __init__(self, max_force: int):
        # Load elements

        element_class = random.choice(Elements().types)

        self.element = element_class.name
        self.original_force = random.randint(1, max_force)
        self.force = self.original_force

        # Defining which element destroys the current element and which it destroys
        self.weakness = element_class.weakness
        self.destroys = element_class.destroys

        self.united = False


class Player():
    name = "Player"
    def show_elements(self):
    
        index = 0
        for i in self.elements:
            index += 1

            print(f"[{index}] {i.element} (+{i.force}): Destroys {i.destroys} and is weak to {i.weakness}")


    def choose(self):
        if len(self.elements) > 0:
            print("Choose an element: ")
            
            self.show_elements()

            move_suffix = self.game.move_suffix
            print("\nPlayer moves:")
            player_moves = ""

            for move in self.game.movements_player:
                player_moves += move+move_suffix

            player_moves = player_moves.removesuffix(move_suffix)
            print(player_moves+"\nComputer moves:")

            computer_moves = ""

            for move in self.game.movements_computer:
                computer_moves += move+move_suffix

            computer_moves = computer_moves.removesuffix(move_suffix)
            print(computer_moves)

            while True:
                try:
                    uinput = input("=> ").lower()

                    if uinput == "buff":
                        if self.buffing_points <= 0:
                            print("You have no buffing points.")
                        else:
                            choice_buff = input(f"Element number to buff: ")
                            if tools.validate_num_input(self.elements, choice_buff):
                                choice_buff = int(choice_buff)   
                                choosen_element = self.elements[choice_buff-1]
                                if choosen_element.force < self.game.max_force:
                                    choosen_element.force += 1
                                    self.buffing_points -= 1
                            else:
                                print("Invalid input.")
                                continue
                        
                        print(f"Buffing points left: {self.buffing_points}")     
                        self.show_elements()   
                        continue
                    elif uinput == "quit":
                        return -1
                    elif uinput == "unite":
                        if self.unifying_points > 0:
                            # Unites all elements of the same type together
                            index = 0
                            list_elements  = Elements().element_list
                            for i in list_elements:
                                index += 1
                                print(f"[{index}] {i}")

                            choice = input("Element to unite => ")
                            
                            if tools.validate_num_input(list_elements, choice):
                                element_to_unite = int(choice)
                                element_to_unite = list_elements[element_to_unite-1]

                                same_types = []
                                for i in self.elements:
                                    if i.element == element_to_unite:
                                        same_types.append(i)
                                found_first = False
                                copy_elements = self.elements.copy()
                                if len(same_types) > 1:
                                    for elem in self.elements:
                                        if elem.element == element_to_unite:
                                            if not found_first:
                                                total_added = 0
                                                for same_elem in same_types:
                                                    total_added += same_elem.force

                                                elem.force = total_added
                                                found_first = True
                                                elem.united = True
                                            else:
                                                # Delete
                                                copy_elements.remove(elem)

                                    print(f"Unified {len(same_types)} elements!")
                                    self.elements = copy_elements[0:-1]
                                    self.show_elements()
                                    same_types = []
                                    self.unifying_points -= 1
                                    continue
                                else:
                                    print("You don't have enough of that element.")
                                    continue
                            else:
                                print("Invalid input.")
                                continue
                        else:  
                            print("You have no union points.")
                            continue
                    else:
                        index = int(uinput) - 1


                    element = self.elements[index]
                    print(f"You chose {element.element} (+{element.force})")
                    self.choice = self.elements[index]

                    if self.extra_force > 0:
                        amount_force = int(input("How many extra force points do you want to use? "))
                        if amount_force > self.extra_force:
                            print("You choose a number bigger than the avaliable. Using the max amount!")
                            self.used_force = self.extra_force
                        else:
                            self.used_force = amount_force
                    total_force = self.choice.force + self.used_force

                    if not element.united:
                        if total_force > self.game.max_force:
                            old_used_force = self.used_force
                            self.used_force = self.game.max_force - self.choice.force
                            print(f"Your input {old_used_force} reaches the limit of force. Used force is now {self.used_force}")
                    else:
                        if self.used_force > 0 and self.choice.force > self.game.max_force:
                            self.used_force = 0
                            print(f"You can't use extra force with tunited elements which force is superior to {self.game.max_force}. Used force is now 0")

                    force_buff = element.force - element.original_force
                    self.game.movements_player.append(f"Use {element.element}: {element.original_force}+{force_buff}+{self.used_force})")

                    break
                except (ValueError, IndexError):
                    print("Invalid input")
            
            return 0

    def __init__(self):
        self.points = 0
        self.elements = []
        self.choice = None
        self.game = None
        self.extra_force = 0 # Extra force points to use in case of a potentital defeat
        self.used_force = 0
        self.buffing_points = 0
        self.unifying_points = 0


class Computer(Player):
    name = "Computer"

    def choose(self):
        ai = self.game.gameplay["computer_ai"] 
        if ai == "dummy":
            if len(self.elements) > 0:
                index = random.randint(0, len(self.elements) - 1)
                element = self.elements[index]
                print(f"Computer chose {element.element} (+{element.force})")
                self.choice = self.elements[index]

                self.game.movements_computer.append(f"{element.element} (Force: {element.force}+{self.used_force})")
        else:
            if len(self.elements) > 0:
                # Gets the element with the highest force


                element = tools.highest_force_element(self.elements)[1]
                print(f"Computer chose {element.element} (+{element.force})")

                self.choice = element
                
                force_buff = 0
                # Use buffing points if there is
                if ai == "maxxer":
                    while self.buffing_points > 0 and (element.force + self.used_force) < self.game.max_force:
                        element.force += 1
                        self.buffing_points -= 1
                elif ai in ["buffer", "unifier"]:
                    # Check if the buffing points are 3 or more
                    if self.buffing_points >= 3:
                        # If so, buff the elements with 7 or less of force, from the highest to the lowest
                        elements_force = []
                        for elem in self.elements:
                            elements_force.append({"name": elem.element, "force": elem.force, "object": elem})

                        elements_force.sort(key=lambda x: x["force"], reverse=True)

                        for elem in elements_force:
                            if elem["force"] <= 7:
                                elem["object"].force += 1
                                self.buffing_points -= 1
                            
                            if self.buffing_points == 0:
                                break
                
                force_buff = element.force - element.original_force
                # Spend all union points
                if ai == "unifier":

                    copy_elements = self.elements.copy()
                    while self.unifying_points > 0:
                        elements_types = Elements().element_list
                        self.elements = copy_elements.copy()
                        
                        if len(self.elements) <= len(elements_types):
                            break

                        # Check which sum gives the highest force
                        element_high = ""
                        sum_high = 0

                        for elem_type in elements_types:
                            sum_elem = 0
                            index = 0
                            for elem in copy_elements:
                                if elem.element == elem_type:
                                    index += 1
                                    sum_elem += elem.force

                            if sum_elem > sum_high and index > 1:
                                element_high = elem_type
                                sum_high = sum_elem
                        
                        # After it, sum all the elements of the same type
                        same_type = []
                        for elem in self.elements:
                            if elem.element == element_high:
                                same_type.append(elem)
                        
                        if len(same_type) > 1:
                            found_first = False
                            for elem in self.elements:
                                if elem.element == element_high:
                                    if not found_first:
                                        elem.united = True
                                        found_first = True
                                        elem.force = sum_high
                                    else:
                                        copy_elements.remove(elem)

                            self.unifying_points -= 1
                        else:
                            continue
                    self.elements = copy_elements.copy()
                    element = self.choice = tools.highest_force_element(self.elements)[1]

                # Use the max of force possible to try to reach 10
                while element.force + self.used_force < self.game.max_force:
                    
                    if self.extra_force > 0 and self.used_force < self.extra_force and not element.united:
                        self.used_force += 1
                    else:
                        break

                force_buff =  element.force - element.original_force                
                self.game.movements_computer.append(f"Use {element.element}: {element.original_force}+{force_buff}+{self.used_force})")
    def __init__(self):
        super().__init__()


class Game():
    def populate_elements(self):
        players = [self.player, self.computer]
        for p in players:
            while len(p.elements) < self.max_elements:
                p.elements.append(Element(self.max_force))

    def next_round(self):
        players = [self.player, self.computer]

        if self.round > 1:
            input("Press enter to continue...")
        else:
            for player in players:
                player.unifying_points = len(Elements().element_list)

        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        
        for player in players:
            if random.randint(1, 1000) <= 250:
                player.buffing_points += 1

        if self.round % 5 == 0:
            for player in players:
                player.unifying_points += 1

        if self.round % 2 == 0:
            for player in players:
                player.extra_force += 1

        print(f"Round {self.round}/{self.max_rounds}\nPlayer points: {self.player.points}, Computer points: {self.computer.points}\nExtra froce: {self.player.extra_force}, Buffing points: {self.player.buffing_points}")
        print(f"Union points: {self.player.unifying_points}\n\n")

        if self.gameplay["dev_mode"]:
            print(f"Computer extra force: {self.computer.extra_force}, Computer buffing points: {self.computer.buffing_points}")
            print(f"Computer union points: {self.computer.unifying_points}\n\n")

    def is_over(self):
        if self.round > self.max_rounds:
            self.game_over = True

            point_diff = self.player.points - self.computer.points

            if point_diff > 0:
                print("You won the game!")
            elif point_diff < 0:
                print("You lost the game!")
            else:
                print("It's a draw!")


    def define_winner(self):
        winner = None
        loser = None
        used_force = False
        
        # First, check if player element destroys the computer element
        if self.player.choice.destroys == self.computer.choice.element:
            print("You won!")
            winner = self.player
            loser = self.computer
        # Second, check if computer element destroys the player element
        elif self.player.choice.element == self.computer.choice.destroys:
            print("You lost!")
            winner = self.computer
            loser = self.player
        else:
            # If neither, check force instead
            used_force = True

            player_used_force = self.player.used_force
            computer_used_force = self.computer.used_force

            player_choice = self.player.choice
            computer_choice = self.computer.choice

            buffed_player_choice = self.player.choice.force + player_used_force
            buffed_computer_choice = self.computer.choice.force + computer_used_force
            
            # Checking buffed forces
            if buffed_computer_choice > buffed_player_choice:
                winner = self.computer
                loser = self.player
            elif buffed_computer_choice < buffed_player_choice:
                winner = self.player
                loser = self.computer
            else:
                winner = None
                loser = None

            if winner is not None and loser is not None:
                print(f"{winner.name} won! {player_choice.element} +{player_choice.force} (+{player_used_force} extra force) -> {buffed_player_choice} vs. {computer_choice.element} +{computer_choice.force} (+{computer_used_force} extra force) -> {buffed_computer_choice}")
                winner.extra_force -= winner.used_force
            else:
                print("Draw!")

        # Add points to winner
        if winner is not None:
            winner.points += 1
            if used_force:
                winner.extra_force += abs(winner.choice.force - loser.choice.force)
                loser.extra_force -= 1
            else:
                winner.extra_force -= 1
                loser.extra_force -= 1
        else:
            self.player.extra_force += 1
            self.computer.extra_force += 1

        # Set extra force to zero if lower than zero
        self.player.extra_force = 0 if self.player.extra_force < 0 else self.player.extra_force
        self.computer.extra_force = 0 if self.computer.extra_force < 0 else self.computer.extra_force

        # Remove the choosen elements from computer and player lists
        self.player.elements.remove(self.player.choice)
        self.computer.elements.remove(self.computer.choice)

        # Reset choice
        self.player.choice = None
        self.computer.choice = None
        self.player.used_force = 0
        self.computer.used_force = 0

        # New round
        self.round += 1

        self.populate_elements()
        


    def __init__(self):
        # Load config file
        self.config = hfclib.parseHfc(hfc_path="options.hfc")
        self.gameplay = hfclib.getVariables("Gameplay", self.config)

        self.movements_player = []
        self.movements_computer = []

        self.max_rounds = self.gameplay["rounds"]
        self.max_force = 10
        self.round = 1
        self.game_over = False

        self.player = Player()
        self.computer = Computer()


        self.computer.game = self
        self.player.game = self

        # Define elements for player and computer for game to start
        self.max_elements = self.gameplay["elements"]
        self.max_force = 10

        self.player.elements = [Element(self.max_force) for _ in range(self.max_elements)]
        self.computer.elements = [Element(self.max_force) for _ in range(self.max_elements)]

        self.move_suffix = " -> "


def start():
    game = Game()

    while not game.game_over:
        game.next_round()
        if game.player.choose() < 0:
            return 0
        game.computer.choose()
        game.define_winner()
        game.is_over()

    return 0
