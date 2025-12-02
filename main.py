"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Cayden Brockington]

AI Usage: [used ChatGPT to help format inventory, explore, and shop classes]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

"""
Main Game File - Quest Chronicles
This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *
import random

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    while True:
        print('\n--- MAIN MENU ---')
        print('1. New Game')
        print('2. Load Game')
        print('3. Exit')
        choice = input('Enter choice (1-3): ').strip()
        if choice in ('1', '2', '3'):
            return int(choice)
        print('invalid input, please enter 1, 2, or 3')


def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    print('\n--- NEW GAME ---')
    name = input('Enter your character name: ').strip()
    print('available classes: Warrior, Mage, Rogue, Cleric')
    char_class = input('choose your class: ').strip().capitalize()

    try:
        # Create character
        current_character = character_manager.create_character(name, char_class)
        print(f'character "{name}" the {char_class} created successfully')
        
        # Give starting items
        starter_items = ["Health Potion", "Rusty Sword"]
        for item_name in starter_items:
            if item_name in all_items:
                try:
                    inventory_system.add_item(current_character, all_items[item_name])
                    print(f'received: {item_name}')
                except InventoryFullError:
                    pass

        # Save and start game
        save_game()
        game_loop()
    except InvalidCharacterClassError as e:
        print(f'Error: {e}')
        return


def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    print('\n--- LOAD GAME ---')
    
    # Get list of saved characters
    saved_characters = character_manager.list_saved_characters()

    if not saved_characters:
        print('no saved games found')
        input('press enter to continue...')
        return

    # Display saved characters
    print('saved characters:')
    for i, char_name in enumerate(saved_characters, 1):
        print(f'{i}. {char_name}')
    print(f'{len(saved_characters) + 1}. back')

    # Get user choice
    while True:
        choice = input(f'select character (1-{len(saved_characters) + 1}): ').strip()
        if choice.isdigit():
            choice_num = int(choice)
            if choice_num == len(saved_characters) + 1:
                return
            if 1 <= choice_num <= len(saved_characters):
                char_name = saved_characters[choice_num - 1]
                break
        print(f'please enter a number between 1 and {len(saved_characters) + 1}')

    try:
        # Load character
        current_character = character_manager.load_character(char_name)
        print(f'character "{char_name}" loaded successfully')
        input('press enter to continue...')
        game_loop()
    except CharacterNotFoundError as e:
        print(f'Error: {e}')
        input('press enter to continue...')
    except SaveFileCorruptedError as e:
        print(f'Error: {e}')
        print('save file may be corrupted')
        input('press enter to continue...')


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print('\ngame saved!')
            print('thanks for playing!')
            game_running = False

        # Auto save after each action except save and quit
        if game_running and choice != 6:
            save_game()


def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print('\n' + '=' * 50)
    print(f'GAME MENU - {current_character["name"]} the {current_character["class"]}')
    print('=' * 50)
    # FIXED: changed 'current_health' to 'health'
    print(f'level {current_character["level"]} | HP: {current_character["health"]}/{current_character["max_health"]} | gold: {current_character["gold"]}')
    print('=' * 50)
    print('1. view character stats')
    print('2. view inventory')
    print('3. quest menu')
    print('4. explore (find battles)')
    print('5. shop')
    print('6. save and quit')
    print('=' * 50)

    while True:
        choice = input('enter choice (1-6): ').strip()
        if choice in ('1', '2', '3', '4', '5', '6'):
            return int(choice)
        print('please enter a number between 1 and 6')


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print('\n' + '=' * 50)
    print('CHARACTER STATS')
    print('=' * 50)

    # Basic info
    print(f'\nname: {current_character["name"]}')
    print(f'class: {current_character["class"]}')
    print(f'level: {current_character["level"]}')
    # FIXED: Added function to calculate XP needed
    xp_needed = current_character["level"] * 100
    print(f'experience: {current_character["experience"]}/{xp_needed}')

    # Health and stats (FIXED: removed non-existent fields)
    print(f'\nhealth: {current_character["health"]}/{current_character["max_health"]}')
    print(f'strength: {current_character["strength"]}')
    print(f'magic: {current_character["magic"]}')

    # Resources
    print(f'\ngold: {current_character["gold"]}')

    # Equipment (simplified - these may not exist yet)
    print('\nequipment:')
    weapon = current_character.get('equipped_weapon')
    armor = current_character.get('equipped_armor')
    print(f'  weapon: {weapon["name"] if weapon else "none"}')
    print(f'  armor: {armor["name"] if armor else "none"}')

    # Quest progress
    active = quest_handler.get_active_quests(current_character, all_quests)
    completed = quest_handler.get_completed_quests(current_character, all_quests)
    print(f'\nquests: {len(active)} active, {len(completed)} completed')

    input('\npress enter to continue...')


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    while True:
        print('\n' + '=' * 50)
        print('INVENTORY')
        print('=' * 50)
        
        inventory = current_character.get('inventory', [])

        if not inventory:
            print('\nyour inventory is empty')
            input('\npress enter to go back...')
            return
        
        # Display inventory
        print(f'\ncapacity: {len(inventory)}/{current_character.get("inventory_capacity", 20)}')
        print('\nitems:')
        for i, item in enumerate(inventory, 1):
            print(f'{i}. {item["name"]} - {item["type"]} - {item.get("description", "no description")}')
        
        print(f'\n{len(inventory) + 1}. back')

        # Get choice
        choice = input(f'\nselect item to use/equip (1-{len(inventory) + 1}): ').strip()
        if choice.isdigit():
            choice_num = int(choice)
            if choice_num == len(inventory) + 1:
                return
            if 1 <= choice_num <= len(inventory):
                item = inventory[choice_num - 1]
                use_item_menu(item)
            else:
                print(f'please enter a number between 1 and {len(inventory) + 1}')
        else:
            print('invalid input')


def use_item_menu(item):
    """Menu for using/equipping an item"""
    global current_character
    
    print(f'\n--- {item["name"]} ---')
    print(f'type: {item["type"]}')
    print(f'description: {item.get("description", "no description")}')
    
    if item['type'] == 'consumable':
        print('\n1. use')
        print('2. drop')
        print('3. back')
        
        choice = input('\nchoice: ').strip()
        if choice == '1':
            try:
                inventory_system.use_item(current_character, item)
                print(f'used {item["name"]}!')
            except ItemNotUsableError as e:
                print(f'error: {e}')
        elif choice == '2':
            inventory_system.remove_item(current_character, item)
            print(f'dropped {item["name"]}')
    
    elif item['type'] in ['weapon', 'armor']:
        print('\n1. equip')
        print('2. drop')
        print('3. back')
        
        choice = input('\nchoice: ').strip()
        if choice == '1':
            try:
                inventory_system.equip_item(current_character, item)
                print(f'equipped {item["name"]}!')
            except ItemNotEquippableError as e:
                print(f'error: {e}')
        elif choice == '2':
            inventory_system.remove_item(current_character, item)
            print(f'dropped {item["name"]}')


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    while True:
        print('\n' + '=' * 50)
        print('QUEST MENU')
        print('=' * 50)
        print('1. view active quests')
        print('2. view available quests')
        print('3. view completed quests')
        print('4. accept quest')
        print('5. abandon quest')
        print('6. complete quest (for testing)')
        print('7. back')
        
        choice = input('\nchoice (1-7): ').strip()

        if choice == '1':
            view_active_quests()
        elif choice == '2':
            view_available_quests()
        elif choice == '3':
            view_completed_quests()
        elif choice == '4':
            accept_quest_menu()
        elif choice == '5':
            abandon_quest_menu()
        elif choice == '6':
            test_complete_quest()
        elif choice == '7':
            return
        else:
            print('please enter a number between 1 and 7')


def view_active_quests():
    """Display active quests"""
    active = quest_handler.get_active_quests(current_character, all_quests)
    
    print('\n--- active quests ---')
    if not active:
        print('no active quests')
    else:
        for quest in active:
            print(f'\n{quest["title"]}')
            print(f'  {quest["description"]}')
            print(f'  rewards: XP={quest.get("reward_xp", 0)}, Gold={quest.get("reward_gold", 0)}')
    
    input('\npress enter to continue...')


def view_available_quests():
    """Display available quests"""
    print('\n--- available quests ---')
    available = quest_handler.get_available_quests(current_character, all_quests)
    
    if not available:
        print('no quests available at your level')
    else:
        for quest in available:
            print(f'\n{quest["title"]} (level {quest["required_level"]})')
            print(f'  {quest["description"]}')
            print(f'  rewards: XP={quest.get("reward_xp", 0)}, Gold={quest.get("reward_gold", 0)}')
    
    input('\npress enter to continue...')


def view_completed_quests():
    """Display completed quests"""
    completed = quest_handler.get_completed_quests(current_character, all_quests)
    
    print('\n--- completed quests ---')
    if not completed:
        print('no completed quests yet')
    else:
        for quest in completed:
            print(f'✓ {quest["title"]}')
    
    input('\npress enter to continue...')


def accept_quest_menu():
    """Accept a new quest"""
    print('\n--- accept quest ---')
    
    available = quest_handler.get_available_quests(current_character, all_quests)
    
    if not available:
        print('no quests available')
        input('press enter to continue...')
        return
    
    for i, quest in enumerate(available, 1):
        print(f'{i}. {quest["title"]}')
    
    choice = input(f'\nselect quest (1-{len(available)}): ').strip()
    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= len(available):
            quest = available[choice_num - 1]
            try:
                quest_handler.accept_quest(current_character, quest['quest_id'], all_quests)
                print(f'accepted quest: {quest["title"]}')
            except (QuestAlreadyActiveError, QuestAlreadyCompletedError, 
                    InsufficientLevelError, QuestRequirementsNotMetError) as e:
                print(f'error: {e}')
        else:
            print('invalid choice')
    else:
        print('invalid input')
    
    input('\npress enter to continue...')


def abandon_quest_menu():
    """Abandon an active quest"""
    active = quest_handler.get_active_quests(current_character, all_quests)
    
    if not active:
        print('\nno active quests to abandon')
        input('press enter to continue...')
        return
    
    print('\n--- abandon quest ---')
    for i, quest in enumerate(active, 1):
        print(f'{i}. {quest["title"]}')
    
    choice = input(f'\nselect quest to abandon (1-{len(active)}): ').strip()
    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= len(active):
            quest = active[choice_num - 1]
            try:
                quest_handler.abandon_quest(current_character, quest['quest_id'])
                print('abandoned quest')
            except QuestNotActiveError as e:
                print(f'error: {e}')
        else:
            print('invalid choice')
    else:
        print('invalid input')
    
    input('\npress enter to continue...')


def test_complete_quest():
    """Complete a quest (for testing)"""
    active = quest_handler.get_active_quests(current_character, all_quests)
    
    if not active:
        print('\nno active quests')
        input('press enter to continue...')
        return
    
    print('\n--- complete quest ---')
    for i, quest in enumerate(active, 1):
        print(f'{i}. {quest["title"]}')
    
    choice = input(f'\nselect quest (1-{len(active)}): ').strip()
    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= len(active):
            quest = active[choice_num - 1]
            try:
                rewards = quest_handler.complete_quest(current_character, quest['quest_id'], all_quests)
                print('quest completed!')
                print(f"rewards: XP={rewards.get('xp_gained', 0)}, Gold={rewards.get('gold_gained', 0)}")
            except QuestNotActiveError as e:
                print(f'error: {e}')
        else:
            print('invalid choice')
    else:
        print('invalid input')
    
    input('\npress enter to continue...')

        
def explore():
    """Find and fight random enemies"""
    global current_character
    
    print('\n' + '=' * 50)
    print('EXPLORING...')
    print('=' * 50)
    
    # Generate enemy
    level = current_character['level']
    enemy_level = max(1, level + random.randint(-1, 2))
    
    enemy_types = ["goblin", "orc", "wolf", "bandit", "skeleton"]
    enemy_name = random.choice(enemy_types)
    
    enemy = combat_system.create_enemy(enemy_name, enemy_level)
    
    print(f'\na level {enemy_level} {enemy_name} appears!')
    input('press enter to fight...')

    try:
        # Start combat
        battle = combat_system.SimpleBattle(current_character, enemy)
        winner = battle.fight()
        
        if winner == "player":
            print('\nvictory!')
            xp_gain = enemy['experience_reward']
            gold_gain = enemy['gold_reward']
            
            print(f'gained {xp_gain} XP and {gold_gain} gold!')
            
            character_manager.gain_experience(current_character, xp_gain)
            current_character['gold'] += gold_gain

        else:
            print('\ndefeat!')
            handle_character_death()
    
    except InsufficientHealthError:
        print("\nyou're too weak to fight! heal first")
    except Exception as e:
        print(f'\nbattle error: {e}')
    
    input('\npress enter to continue...')


def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    shop_items = {
        "Health Potion": 50,
        "Iron Sword": 100,
        "Steel Armor": 150,
        "Magic Staff": 200,
        "Leather Boots": 75
    }
    
    while True:
        print('\n' + '=' * 50)
        print('SHOP')
        print('=' * 50)
        print(f'your gold: {current_character["gold"]}')
        print('\n1. buy item')
        print('2. sell item')
        print('3. back')

        choice = input('\nchoice (1-3): ').strip()
        
        if choice == '1':
            print('\n--- available items ---')
            items = list(shop_items.items())
            for i, (item_name, price) in enumerate(items, 1):
                print(f'{i}. {item_name} - {price} gold')
            
            item_choice = input(f'\nselect item (1-{len(items)}): ').strip()
            if item_choice.isdigit():
                choice_num = int(item_choice)
                if 1 <= choice_num <= len(items):
                    item_name, price = items[choice_num - 1]
                    
                    if current_character['gold'] >= price:
                        if item_name in all_items:
                            try:
                                inventory_system.add_item(current_character, all_items[item_name])
                                current_character['gold'] -= price
                                print(f'purchased {item_name}!')
                            except InventoryFullError:
                                print('inventory is full!')
                        else:
                            print('item not available')
                    else:
                        print('not enough gold!')
                else:
                    print('invalid choice')
            else:
                print('invalid input')
        elif choice == '2':
            inventory = current_character.get('inventory', [])
            if not inventory:
                print('\nnothing to sell!')
            else:
                print('\n--- your items ---')
                for i, item in enumerate(inventory, 1):
                    sell_price = item.get('value', 10) // 2
                    print(f'{i}. {item["name"]} - {sell_price} gold')
                
                item_choice = input(f'\nselect item (1-{len(inventory)}): ').strip()
                if item_choice.isdigit():
                    choice_num = int(item_choice)
                    if 1 <= choice_num <= len(inventory):
                        item = inventory[choice_num - 1]
                        sell_price = item.get('value', 10) // 2
                        inventory_system.remove_item(current_character, item)
                        current_character['gold'] += sell_price
                        print(f'sold {item["name"]} for {sell_price} gold!')
                    else:
                        print('invalid choice')
                else:
                    print('invalid input')
        
        elif choice == '3':
            return
        else:
            print('please enter 1, 2, or 3')


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    if current_character:
        try:
            character_manager.save_character(current_character)
        except Exception as e:
            print(f'error saving game: {e}')


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    all_quests = game_data.load_quests()
    all_items = game_data.load_items()


def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print('\n' + '=' * 50)
    print('YOU HAVE DIED')
    print('=' * 50)
    
    revive_cost = current_character['level'] * 50
    
    print(f'\nrevive for {revive_cost} gold?')
    print('1. yes')
    print('2. no (quit)')
    
    choice = input('\nchoice: ').strip()
    if choice == '1':
        if current_character['gold'] >= revive_cost:
            character_manager.revive_character(current_character)
            current_character['gold'] -= revive_cost
            print('\nyou have been revived!')
        else:
            print('\nnot enough gold to revive')
            print('game over')
            game_running = False
    else:
        print('\ngame over')
        game_running = False


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

