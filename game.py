from character import Character
from monster import Dragon
from monster import Goblin
from monster import Troll


class Game:
  def setup(self):

    self.player = Character()
    self.monsters = [
      Goblin(),
      Troll(),
      Dragon()
    ]
    self.monster = self.get_next_monster()
    
  def get_next_monster(self):
    try:
      return self.monsters.pop(0)
    except IndexError:
      return None
    
  def monster_turn(self):
    # check to see if the monster attacks
    if self.monster.attack():
      
      print("With a mighty {} the {} {} attacks you!".format(self.monster.battlecry(), self.monster.color, self.monster.__class__.__name__))
        
      # check if the player wants to dodge
      dodge_input = raw_input("Do you want to dodge? [Y]es [N]o ").lower()
      if (dodge_input == "y"):
        self.player.forfeit_next_turn = True
        if (self.player.dodge()):
          print("Your dodge works! The monster misses you")
        else:
          print("Your dodge doesn't work. The monster hits you :(")
          self.player.hit_points -= self.monster.experience
      else:
        print("The monster hits you!")
        self.player.hit_points -= self.monster.experience

    # if the monster isn't attacking, tell that too
    else:
      print("The monster doesn't attack")
    
  def player_turn(self):

    if not (self.player.forfeit_next_turn):
      # let the player attack, rest, or quit
      action = raw_input("Do you want to [A]ttack, [R]est, or [Q]uit?  ").lower()
      # if they attack:
      if (action == "a"):
        # see if the attack is successful
        if  (self.player.attack()):
          # if so, see if the monster dodges
          if(self.monster.dodge()):
            print("The {} {} dodged!".format(self.monster.color, self.monster.__class__.__name__))
          else:
            print("You hit the monster {}".format(self.monster.hit_points))
            self.monster.hit_points -= 1 + self.player.experience

        # if not a good attack, tell the player
        else:
          print("Your attack failed")
      # if they rest:
      elif (action == "r"):
        # call the player.rest() method
        current_hitpoints = self.player.hit_points
        self.player.rest()
        if (self.player.hit_points > current_hitpoints):
          print("You gained a hit point.")
          self.player.forfeit_next_turn = True
        else:
          print("You are already at maxixmum hit points")
      # if they quit, exit the game
      elif (action == "q"):
        exit()
      # if they pick anything else, re-run this method
    else:
      print("you can't attack this round")
      self.player.forfeit_next_turn = False;
    
  def cleanup(self):

    # if the monster has no more hit points:
    if (self.monster.hit_points == 0):
      # up the player's experience
      self.player.experience += self.monster.experience
      print("You killed the {} {} and gained {} experience!".format(self.monster.color, self.monster.__class__.__name__, self.monster.experience))
      self.monster = self.get_next_monster()

  def __init__(self):

    self.setup()
    
    while (self.player.hit_points > 0) and (self.monster or self.monsters):
      print(self.player)
      self.monster_turn()
      self.player_turn()
      self.cleanup()
      
    if self.player.hit_points:
      print("You win!")
    elif self.monsters or self.monster:
      print("You lose!")