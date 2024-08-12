import numpy as np
from enum import Enum
from abc import ABC, abstractmethod

class LineType(Enum):
    UNKNOWN = -1
    LEFT = 0
    RIGHT = 1

