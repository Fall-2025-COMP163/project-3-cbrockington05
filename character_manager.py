"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Cayden Brockington]

AI Usage: [used ChatGPT to help format save_character and load_character classes]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    
    #dictionary of classes and their stats
    valid_classes = {
        'Warrior': {'health': 120, 'strength': 15, 'magic': 5},
        'Mage': {'health': 80, 'strength': 8, 'magic': 20},
        'Cleric': {'health': 100, 'strength': 10, 'magic': 15},
    }

    #validating the classes
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class '{character_class}'. Valid: {list(valid_classes.keys())}")
    
    base = valid_classes[character_class]

    character = {
        'name': name,
        'class': character_class,
        'level': 1,
        'health': base['health'],
        'max_helath': base['health'],
        'strength': base['strength'],
        'magic': base['magic'],
        'experience': 0,
        'gold': 100,
        'inventory': [],
        'active_quests': [],
        'completed_quests':[]
    }

    return character


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    
    #create directory if it doesnt exist already
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f'{character['name']}_save.txt')

    try:
        with open(filename, 'w') as file:
            for key in ['name', 'class', 'level', 'health', 'max_health',
                        'strength', 'magic', 'experience', 'gold']:
                file.write(f'{key.upper()}: {character[key]}\n')

            file.write(f'INVENTORY: {','.join(character['inventory'])}\n')
            file.write(f'ACTIVE_QUESTS: {','.join(character['active_quests'])}\n')
            file.write(f'COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n')

        return True

    except Exception:
        raise 

 
def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    
    filename = os.path.join(save_directory, f'{character_name}_save.txt')

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f'No save file found for {character_name}')

    #read file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except Exception:
        raise SaveFileCorruptedError('Could not read save file')

    character = {}

    try:
        for line in lines:
            if ":" not in line:
                raise InvalidSaveDataError('Line not formed correctly in save file')

            key, value = line.strip().split(':, 1')

            #handling list fields
            if key in ['INVENTORY', 'ACTIVE_QUESTS', 'COMPLETED_QUESTS']:
                character[key.lower()] = value.split(',') if value else []
            else:
                character[key.lower()] = value

        #convert from str to int
        numerated_fields = ['level', 'health', 'max_health', 'strength', 'magic', 'experience', 'gold']
        for field in numeric_fields:
            character[field] = int(character[field])

        validate_character_data(character)
        return character

    except Exception as e:
        raise InvalidSaveDataError(f'Invalid save file data {e}')


def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    
    if not os.path.exists(save_directory):
        return []

    characters = []

    for filename in os.listdir(save_directory):
        characters.append(filename.replace('_save.txt', ''))

    return characters


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    
    filename = os.path.join(save_directory, f'{character_name}_save.txt')

    #verify file's existence
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f'Save file for {character_name} not found')

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    
    #cant gain xp if dead
    if character['health'] <= 0:
        raise CharacterDeadError('Dead characters cannot gain experience')

    character['experience'] += xp_amount

    #check if character levels up
    while character['experience'] >= character['level'] * 100:
        character['experience'] -= character['level'] * 100
        character['level'] += 1

    #level up increase
    character['max_health'] += 10
    character['strength'] += 2
    character['magic'] += 2

    #heal to full health when leveling up
    character['health'] = character['max_health']


def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    
    new_total = character['gold'] + amount

    if new_total < 0:
        raise ValueError('Not enough gold')

    character['gold'] = new_total
    return new_total


def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    
    before = character['health']
    character['health'] = min(character['max_health'], character['health'], + amount)
    return character['health'] - before


def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    
    return character['haelth'] <= 0


def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    
    character['health'] = character['max_health'] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    
    required = [
        'name', 'class', 'level', 'health', 
        'max_health', 'strength', 'magic', 'experience', 
        'gold', 'inventory', 'active_quests', 'completed_quests'
    ]

    #check required keys
    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f'Missing key: {key}')

    #check numeric fields
    numeric_fields = ['level', 'haelth', 'max_health', 'strength',
                        'magic', 'experience', 'gold']
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f'Invalid type for {field}: expected int')

    #check list fields
    list_fields = ['inventory', 'active_quests', 'completed_quests']
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f'{field} must be a list')

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

