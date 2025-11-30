"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Cayden Brockington]

AI Usage: [used ChatGPT to help me format the equip and unequip classes]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    
    #make sure inventory key exists
    if 'inventory' not in character:
        character['inventory'] = []

    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        
        #no room for more items
        raise InventoryFullError('inventory is full')

    character['inventory'].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    
    inv = character.get('inventory', [])
    if item_id not in inv:
        raise ItemNotFoundError(f'item "{item_id}" not found in inventory')

    inv.remove(item_id)
    return True


def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    
    return item_id in character.get('inventory', [])


def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    
    return character.get('inventory', []).count(item_id)


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    
    used = len(character.get('inventory', []))
    return max(0, MAX_INVENTORY_SIZE - used)


def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    
    removed = character.get('inventory', []).copy()
    character['inventory'] = []
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    
    #verify ownership
    if not has_item(character, item_id):
        raise ItemNotFoundError(f'item "{item_id}" not in inventory')

    #check type
    itype = item_data.get('type')
    if itype != 'consumable':
        raise InvalidItemTypeError(f'item "{item_id}" of type "{itype}" cannot be used')

    effect = item_data.get('effect')
    stat_name, value = parse_item_effect(effect)

    #apply effect
    apply_stat_effect(character, stat_name, value)

    #remove one copy
    remove_item_from_inventory(character, item_id)

    return f"used {item_data.get('name', 'item')} -> {stat_name} + {value}"


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    
    #ownership check
    if not has_item(character, item_id):
        raise ItemNotFoundError(f'weapon "{item_id}" is not in inventory')

    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f'item "{item_id}" is not a weapon')

    #make sure equip slots are open
    current_weapon_id = character.get('equipped_weapon')

    #unequip current weapon if present
    if current_weapon_id is not None:
        #before adding, making sure theres space
        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError('no space to unequip current weapon')

        old_weapon_id = current_weapon_id

        #add old weapon back
        add_item_to_inventory(character, old_weapon_id)

        #remove stat bonus if stored
        weapon_bonus = character.pop('_equipped_weapon_bonus', None)
        if weapon_bonus:
            apply_stat_effect(character, weapon_bonus[0], -weapon_bonus[1])

    #apply new weapon effect
    effect = item_data.get('effect')
    stat_name, value = parse_item_effect(effect)

    #apply stat bonus
    apply_stat_effect(character, stat_name, value)
    character['_equipped_weapon_bonus'] = (stat_name, value)
    character['equipped_weapon'] = item_id

    #remove equipped item from inv
    remove_item_from_inventory(character, item_id)

    return f"equipped {item_data.get('name', 'weapon')} (+{value} {stat_name})"


def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if not has_item(character, item_id):
        raise ItemNotFoundError(f'armor "{item_id}" not found in inventory')

    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError(f'item "{item_id}" is not armor')

    current_armor_id = character.get('equipped_armor')

    #unequip existing armor
    if current_armor_id is not None:
        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError('no space to unequip current armor')
        #return old armor to inv
        add_item_to_inventory(character, current_armor_id)
        #remove stoed armor bonus
        armor_bonus = character.pop('_equipped_armor_bonus', None)
        if armor_bonus:
            apply_stat_effect(character, armor_bonus[0], -armor_bonus[1])

    #apply new armor effect
    effect = item_data.get('effect')
    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, value)
    character['_equipped_armor_bonus'] = (stat_name, value)
    character['equipped_armor'] = item_id

    remove_item_from_inventory(character, item_id)

    return f"equipped {item_data.get('name', 'armor')} (+{value} {stat_name})"


def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    
    weapon_id = character.get('equipped_weapon')
    if not weapon_id:
        return None

    #check space
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError('No space to unequip weapon')

    #reverse bonus
    bonus = character.pop('_equipped_weapon_bonus', None)
    if bonus:
        apply_stat_effect(character, bonus[0], -bonus[1])

    #remove equip slot and add item back
    character['equipped_weapon'] = None
    add_item_to_inventory(character, weapon_id)
    return weapon_id


def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    
    armor_id = character.get('equipped_armor')
    if not armor_id:
        return None
    
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError('no space to unequip armor')

    bonus = character.pop('_equipped_armor_bonus', None)
    if bonus:
        apply_stat_effect(character, bonus[0], -bonus[1])

    character['equipped_armor'] = None
    add_item_to_inventory(character, armor_id)
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    
    cost = int(item_data.get('cost', 0))
    if character.get('gold', 0) < cost:
        raise InsufficientResourcesError('not enough gold to purchase item')

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError('inventory is full so you cant purchase')

    #subtract gold and add item
    character['gold'] -= cost
    add_item_to_inventory(character, item_id)
    return True


def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    
    if not has_item(character, item_id):
        raise ItemNotFoundError(f'item "{item_id}" not in inventory')

    cost = int(item_data.get('cost', 0))
    gold_received = cost // 2

    #remove a copy and add gold
    remove_item_from_inventory(character, item_id)
    character['gold'] = character.get('gold', 0) + gold_received
    return gold_received


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer

    #if effect is a str
    if isinstance(effect_string, str):
        if ":" not in effect_string:
            raise ValueError('invalid effect string format')
        stat, raw = effect_string.split(':', 1)
        return stat.strip(), int(raw.strip())
    
    #unknown format
    raise ValueError('unknown effect format')
    

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name not in ('health', 'max_health', 'strength', 'magic'):
        #other stats can be added here
        raise ValueError(f"unknown stat: {stat_name}")

    #make sure key exist
    if stat_name not in character:
        #initialize numeric stats when missing
        character[stat_name] = 0

    #apply change
    character[stat_name] = character.get(stat_name, 0) + int(value)

    #if max_health changed and health exceeds new max
    if stat_name == 'max_health':
        if character.get('health', 0) > character['max_health']:
            character['health'] = character['max_health']
        
    #make sure health is within bounds
    if stat_name == 'health':
        if character.get('health', 0) < 0:
            character['health'] = 0
        if character.get('health', 0) > character.get('max_health', character['health']):
            character['health'] = character.get('max_health', character['health'])
        

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    
    inv = character.get('inventory', [])
    total = len(inv)
    remaining = get_inventory_space_remaining(character)
    print(f"\nInventory ({total}/{MAX_INVENTORY_SIZE}) - Free slots: {remaining}")

    if total == 0:
        print(' (empty)')
        return
    
    #count duplicates
    counts = {}
    for iid in inv:
        counts[iid] = counts.get(iid, 0) + 1

    #print each unique item with its name and count
    for iid, qty in counts.items():
        meta = item_data_dict.get(iid, {})
        name = meta.get('name', iid)
        itype = meta.get('type', 'unknown')
        desc = meta.get('description', '')
        print(f' {qty}x {name} ({itype}) - {desc}')


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

