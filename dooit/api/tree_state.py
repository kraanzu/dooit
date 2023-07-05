from typing import Any

"""
Class that stores states of the tree structure
"""
class TreeState:

  """
  Constructor of the TreeState class
  """
  def __init__(self, tree_state: Any) -> None:
    self._tree_states = tree_state

  """
  Returns the value that is stored in the object
  """
  def get_state(self) -> Any:
    return self._tree_states
