from dataclasses import dataclass
import yaml

@dataclass
class GameConfig:
    board_size: int = 4
    win_score: int = 2048
    animation_delay: float = 0.1
    
    @classmethod # A @classmethod allows a method to be called on the class itself (cls), rather than an instance of the class. It receives the cls parameter (instead of self), representing the class.
    def from_yaml(cls, path: str) -> 'GameConfig':
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict) # cls(**config_dict) dynamically creates an instance of GameConfig using the dictionary values.
    


'''
Understanding @dataclass and @classmethod in Python
1. @dataclass Decorator
The @dataclass decorator is used to automatically generate special methods in a class, such as:

__init__() → Generates a constructor based on class attributes.
__repr__() → Provides a string representation of the object.
__eq__() → Implements equality comparison (==).
'''

'''
A @classmethod allows a method to be called on the class itself, rather than an instance of the class. It receives the cls parameter (instead of self), representing the class.

Example Usage:
Assume a config.yaml file contains:

board_size: 5
win_score: 4096
animation_delay: 0.2

You can load the configuration like this:

config = GameConfig.from_yaml("config.yaml")
print(config.board_size)  # Output: 5
print(config.win_score)   # Output: 4096

This avoids manually extracting values and simplifies object creation.

'''