"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Cayden Brockington]

AI Usage: [ChatGPT helped me format the special abilities classes]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type, level=1):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # "Goblin" or "GOBLIN" will work
    enemy_type = enemy_type.lower()

    # Define default stats for every enemy
    enemy_data = {
        'goblin': {'health': 50, 'strength': 8, 'magic': 2, 'xp': 25, 'gold': 10},
        'orc': {'health': 80, 'strength': 12, 'magic': 5, 'xp': 50, 'gold': 25},
        'dragon': {'health': 200, 'strength': 25, 'magic': 15, 'xp': 200, 'gold': 100},
    }

    # If type not found in dict
    if enemy_type not in enemy_data:
        raise InvalidTargetError(f'Unknown enemy type: {enemy_type}')
    
    stats = enemy_data[enemy_type]

    # Build final enemy dict (with level scaling)
    health = stats['health'] + (level - 1) * 10
    return {
        'name': enemy_type.capitalize(),
        'health': stats['health'],
        'max_health': stats['health'],
        'strength': stats['strength'],
        'magic': stats['magic'],
        'xp_reward': stats['xp'],
        'gold_reward': stats['gold'],
    }


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        return create_enemy('goblin', character_level)
    elif character_level <= 5:
        return create_enemy('orc', character_level)
    else:
        return create_enemy('dragon', character_level)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        
        self.character = character
        self.enemy = enemy
        self.combat_active = True  # We'll know when battles are occurring
        self.turn = 0 # Track whose turn it is fighting
    
    def fight(self):
        """
        Simplified fight method that auto-completes battle
        
        Returns: 'player' if player wins, 'enemy' if player loses
        """
        return self.start_battle()['winner']
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character['health'] <= 0:
            raise CharacterDeadError('Cannot battle while dead!')

        print(f"\n=== BATTLE START ===")
        print(f"{self.character['name']} vs {self.enemy['name']}")

        # Combat will loop until someone dies or succeeds
        while self.combat_active:
            
            display_combat_stats(self.character, self.enemy)

            # Player takes a turn
            self.player_turn()

            # Check if player won
            winner = self.check_battle_end()
            if winner:
                return self._finish_battle(winner)
            
            # Enemy takes a turn
            self.enemy_turn()

            # Check if enemy won
            winner = self.check_battle_end()
            if winner:
                return self._finish_battle(winner) 

    
    def _finish_battle(self, winner):
        """Finish battle and return results"""
            
        self.combat_active = False
        
        if winner == 'player':
            rewards = get_victory_rewards(self.enemy)
            display_battle_log(f"You defeated the {self.enemy['name']}!")
            display_battle_log(f"Gained {rewards['xp']} XP and {rewards['gold']} gold!")
            return {"winner": "player", **rewards}
        else:
            print(f"\n*** DEFEAT ***")
            return  {"winner": "enemy", "xp": 0, "gold": 0}

    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError('Cannot act because combat is not active')
        
        print('\nYour turn:')
        print('1. Basic Attack')
        print('2. Special Ability')
        print('3. Try to Run')

        choice = input('> ').strip()

        if choice == '1':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You hit the {self.enemy['name']} for {damage} damage!")

        elif choice == '2':
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)

        elif choice == '3':
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log('You escaped the battle!')
                self.combat_active = False
                return
            else:
                display_battle_log('Escape failed!')

        else:
            display_battle_log('Invalid choice. You lose your turn.')


    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError('Enemy cannot act because combat is not active')

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"The {self.enemy['name']} hits you for {damage} damage!")  # FIXED: 'your' -> 'you'

    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        base = attacker['strength']
        reduction = defender['strength'] // 4  # Defender absorbs some damage

        damage = base - reduction
        return max(damage, 1)

    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target['health'] = max(0, target['health'] - damage)

    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy['health'] <= 0:
            return 'player'

        if self.character['health'] <= 0:
            return 'enemy'
        
        return None

    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        return random.random() < 0.5
    

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    char_class = character['class'].lower()

    if char_class == 'Warrior':
        return warrior_power_strike(character, enemy)

    elif char_class == 'Mage':
        return mage_fireball(character, enemy)

    elif char_class == 'Rogue':
        return rogue_critical_strike(character, enemy)

    elif char_class == 'Cleric':
        return cleric_heal(character)
    
    else:
        return 'Your class has no special ability'


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    
    damage = character['strength'] * 2
    enemy['health'] = max(0, enemy['health'] - damage)
    
    return f'Power strike hits for {damage} damage!'


def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character['magic'] * 2
    enemy['health'] -= damage
    
    if enemy['health'] < 0:
        enemy['health'] = 0
    return f'Fireball burns for {damage} damage!'


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        damage = character['strength'] * 3
        enemy['health'] -= damage
        if enemy['health'] < 0:
            enemy['health'] = 0
        return f'Critical strike! You deal {damage} damage!'
    
    else:
        return 'Critical strike failed! No extra damage.'


def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = 30
    character['health'] += heal_amount

    # Cap health at max_health
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return 'You cast heal and restore 30 health!'

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    return character['health'] > 0


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }


def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    print('\n=== Battle Status ===')
    print(f"{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    print('=====================')


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

