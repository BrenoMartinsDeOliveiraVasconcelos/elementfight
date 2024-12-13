import hfclib
import game
import platform
import os
import tools

class Menu():
    """
    Class for managing the game's menu

    Attributes
    ----------
    options : list
        A list of tuples, where each tuple contains a display name and a callable function
    configs : dict
        A dictionary of configuration options, where each key is a string and each value is a dictionary with the keys "display_name", "type", and "default"
    """
    @staticmethod
    def clear_screen():
        """
        Clear the screen
        """
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def select(self):
        """
        Present the options to the user and let them select one

        This method will first clear the screen by calling the class method clear_screen.
        Then it will iterate over the options and print each one with its index (starting from 1).
        After that, it will enter a loop where it will keep asking the user for input until
        the user enters a valid option. If the user enters a valid option, it will call the
        corresponding function and break out of the loop. If the user enters an invalid option,
        it will print an error message and ask again.
        """
        # Clear the screen
        self.clear_screen()

        # Print the options
        for i in range(len(self.options)):
            print(f"[{i+1}] {self.options[i][0]}")

        # Loop until the user enters a valid option
        while True:
            # Ask the user for input
            selection = input("Select => ")

            # Check if the user entered a valid option
            if tools.validate_num_input(self.options, selection):
                # If the option is valid, call the corresponding function and break out of the loop
                self.options[int(selection)-1][1]()
                break
            else:
                # If the option is invalid, print an error message and ask again
                print("Option needs to be valid.")

    @staticmethod
    def leave():
        """
        Exit the game
        """
        print("Goodbye!")
        exit(0)

    @staticmethod
    def start_game():
        """
        Start a new game
        """
        game.start()

    def settings(self):
        """
        Present the configuration options to the user and let them modify them
        """
        print("Settings")

        # Print all the options
        index = 0
        for value in self.configs.values():
            index += 1

            print(f'[{index}] {value["display_name"]}')

        # Loop until a valid option is selected
        while True:
            # Ask the user for input
            selection = input("Select => ")

            # Check if the user entered a valid option
            if tools.validate_num_input(self.configs, selection):
                # If the option is valid, get the selected key and its name
                selection = int(selection)
                selected_key = list(self.configs.values())[selection-1]
                selected_key_name = list(self.configs.keys())[selection-1]
                key_section = selected_key["section"]

                user_value = ""
                # Ask the user for input depending on the type
                if selected_key["type"] == "int":
                    while True:
                        # Ask the user for input
                        user_value = input(f"Set {selected_key['display_name']} => ")

                        # Check if the input is a valid integer
                        if tools.validate_nonidx_number_input(user_value, 1):
                            user_value = int(user_value)
                            break
                        else:
                            print("Invalid number")
                elif selected_key["type"] == "choice":
                    # Print all the choices
                    index = 0
                    for i in selected_key["choices"]:
                        index += 1
                        print(f"[{index}] {i[0]} - {i[1]}")

                    # Loop until a valid choice is selected
                    while True:
                        # Ask the user for input
                        user = input(f"Set {selected_key['display_name']} => ")

                        # Check if the user entered a valid choice
                        if tools.validate_num_input(selected_key["choices"], user):
                            # If the choice is valid, get the selected value
                            user = int(user)
                            user_value = selected_key["choices"][user-1][0]
                            break
                        else:
                            print("Invalid number")
                elif selected_key["type"] == "string":
                    user_value = input(f"Set {selected_key['display_name']} => ")
                elif selected_key["type"] == "special":
                    # If the option is a special one, handle it accordingly
                    if selected_key_name == "reset_defaults":
                        # Reset the configuration to its default values
                        config_file = hfclib.parseHfc("options.hfc")
                        for key, value in self.configs.items():
                            if value["section"] != "None":
                                config_file = hfclib.editVariable(section_name=value["section"], variable_name=key, new_variable_value=value["default"], hfc_list=config_file)

                        # Write the changes to the file
                        hfclib.parseList(hfc_list=config_file, write_path="options.hfc")

                        # Break out of the loop
                        break
                    elif selected_key_name == "exit":
                        break

                # Edit the configuration file
                config_file = hfclib.parseHfc("options.hfc")
                config_file = hfclib.editVariable(section_name=key_section, variable_name=selected_key_name, new_variable_value=user_value, hfc_list=config_file)

                # Write the changes to the file
                hfclib.parseList(hfc_list=config_file, write_path="options.hfc")

                # Break out of the loop
                break
            else:
                print("Invalid selection")
            
            

    def __init__(self):
        """
        Initialize the menu
        """
        self.options = [["Start game", self.start_game], ["Settings", self.settings], ["Leave", self.leave]]
        self.configs = {
            "rounds": {"display_name": "Rounds", "type": "int", "default": 20, "section": "Gameplay"},
            "computer_ai": {"display_name": "Computer AI", "type": "choice", "choices": [["dummy", "Easy"], ["maxxer", "Low-medium"], ["buffer", "High-medium"], ["unifier", "Hard"]], "default": "buffer", "section": "Gameplay"},
            "elements": {"display_name": "Number of elements", "type": "int", "default": 10, "section": "Gameplay"},
            "reset_defaults": {"display_name": "Reset defaults", "type": "special", "section": "None"},
            "exit": {"display_name": "Exit", "type": "special", "section": "None"}
        }
