"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f'quest file not found: {filename}')

    try:
        with open(filename, 'r') as file:
            data = file.read()
    except Exception as e:
        raise CorruptedDataError(f'Could not read quest file: {e}')

    # Split by blank lines
    blocks = [b.strip() for b in data.split('\n\n') if b.strip()]

    quest_dict = {}  # FIXED: was 'qeust.dict'

    for block in blocks:
        lines = block.split('\n')
        quest_data = parse_quest_block(lines)
        validate_quest_data(quest_data)
        quest_dict[quest_data['quest_id']] = quest_data

    return quest_dict  # FIXED: was 'quest_data'


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f'Item file not found: {filename}')

    try:
        with open(filename, 'r') as file:
            data = file.read()
    except Exception as e:
        raise CorruptedDataError(f'could not read item file: {e}')

    blocks = [b.strip() for b in data.split('\n\n') if b.strip()]
    item_dict = {}

    for block in blocks:
        lines = block.split('\n')
        item_data = parse_item_block(lines)
        validate_item_data(item_data)
        item_dict[item_data['item_id']] = item_data

    return item_dict


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required = [
        'quest_id', 'title', 'description',
        'reward_xp', 'reward_gold',
        'required_level', 'prerequisite'
    ]

    # Make sure all fields are present
    for field in required:
        if field not in quest_dict:
            raise InvalidDataFormatError(f'missing quest field: {field}')

    # Validate numeric values
    numeric_fields = ['reward_xp', 'reward_gold', 'required_level']

    for field in numeric_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f'field {field} must be an integer')

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required = ['item_id', 'name', 'type', 'effect', 'cost', 'description']

    for field in required:
        if field not in item_dict:
            raise InvalidDataFormatError(f'missing item field: {field}')

    # Validate item type
    valid_types = ['weapon', 'armor', 'consumable']
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"invalid item type: {item_dict['type']}")  # FIXED: f-string quotes

    # Cost must be int
    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError('item cost must be an integer')

    return True


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    os.makedirs('data', exist_ok=True)

    # Default quests
    if not os.path.exists('data/quests.txt'):
        with open('data/quests.txt', 'w') as f:
            f.write(
                'QUEST_ID: first_steps\n'
                'TITLE: First Steps\n'
                'DESCRIPTION: Begin your adventure\n'
                'REWARD_XP: 50\n'
                'REWARD_GOLD: 25\n'
                'REQUIRED_LEVEL: 1\n'
                'PREREQUISITE: NONE\n\n'
                
                'QUEST_ID: goblin_slayer\n'
                'TITLE: Goblin Slayer\n'
                'DESCRIPTION: Defeat 5 goblins\n'
                'REWARD_XP: 100\n'
                'REWARD_GOLD: 50\n'
                'REQUIRED_LEVEL: 2\n'
                'PREREQUISITE: first_steps\n\n'
                
                'QUEST_ID: treasure_hunter\n'
                'TITLE: Treasure Hunter\n'
                'DESCRIPTION: Find the hidden treasure\n'
                'REWARD_XP: 200\n'
                'REWARD_GOLD: 100\n'
                'REQUIRED_LEVEL: 3\n'
                'PREREQUISITE: goblin_slayer\n'
            )

    # Default items
    if not os.path.exists('data/items.txt'):
        with open('data/items.txt', 'w') as f:
            f.write(
                'ITEM_ID: health_potion\n'
                'NAME: Health Potion\n'
                'TYPE: consumable\n'
                'EFFECT: heal:50\n'
                'COST: 50\n'
                'DESCRIPTION: Restores 50 HP\n\n'
                
                'ITEM_ID: rusty_sword\n'
                'NAME: Rusty Sword\n'
                'TYPE: weapon\n'
                'EFFECT: strength:3\n'
                'COST: 25\n'
                'DESCRIPTION: A worn but functional sword\n\n'
                
                'ITEM_ID: iron_sword\n'
                'NAME: Iron Sword\n'
                'TYPE: weapon\n'
                'EFFECT: strength:5\n'
                'COST: 100\n'
                'DESCRIPTION: A basic iron sword\n\n'
                
                'ITEM_ID: steel_armor\n'
                'NAME: Steel Armor\n'
                'TYPE: armor\n'
                'EFFECT: defense:10\n'
                'COST: 150\n'
                'DESCRIPTION: Strong steel armor\n\n'
                
                'ITEM_ID: magic_staff\n'
                'NAME: Magic Staff\n'
                'TYPE: weapon\n'
                'EFFECT: magic:8\n'
                'COST: 200\n'
                'DESCRIPTION: A magical staff\n\n'
                
                'ITEM_ID: leather_boots\n'
                'NAME: Leather Boots\n'
                'TYPE: armor\n'
                'EFFECT: defense:5\n'
                'COST: 75\n'
                'DESCRIPTION: Light leather boots\n'
            )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}

    try:
        for line in lines:
            if ':' not in line:  # Skip invalid lines
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert numeric fields to integers
            if key in ['reward_xp', 'reward_gold', 'required_level']:
                value = int(value)

            # Handle NONE prerequisite
            if key == 'prerequisite' and value.upper() == 'NONE':
                value = 'NONE'  # FIXED: Keep as string 'NONE', not None

            quest[key] = value

        # Ensure quest_id exists
        if 'quest_id' not in quest:
            raise InvalidDataFormatError('quest_id is required')

    except ValueError as e:  # FIXED: Added specific exception
        raise InvalidDataFormatError(f'invalid quest formatting: {e}')
    except Exception as e:
        raise InvalidDataFormatError(f'invalid quest formatting: {e}')

    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}

    try:
        for line in lines:
            if ':' not in line:  # Skip invalid lines
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert cost to int
            if key == 'cost':
                value = int(value)

            # Parse effect (format: stat:amount)
            if key == 'effect':
                if ':' in value:
                    stat, amount = value.split(':', 1)
                    stat = stat.strip()
                    amount = amount.strip()
                    # Store as string for compatibility
                    value = f"{stat}:{amount}"
                # Keep the original string format for now

            item[key] = value

        # Ensure item_id exists
        if 'item_id' not in item:
            raise InvalidDataFormatError('item_id is required')

    except ValueError as e:  # FIXED: Added specific exception
        raise InvalidDataFormatError(f'invalid item formatting: {e}')
    except Exception as e:
        raise InvalidDataFormatError(f'invalid item formatting: {e}')

    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

