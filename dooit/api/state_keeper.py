from typing import List, Any
from tree_state import TreeState

"""
Class that keep the states of the tree structure
"""
class StateKeeper:

  """
  List with the states of the tree structure
  """
  _tree_states: List[Any]

  """
  Constructor of the StateKeeper class
  """
  def __init__(self) -> None:
    self._tree_states = []
  
  """
  Safe the actual state of the tree structure
  """
  def safe_state(self, new_state: Any) -> None:
    if len(new_state) > 0:
      self._tree_states.append(TreeState(new_state))

  """
  Returns the last state of the tree structure
  """
  def return_state(self) -> Any:
    if len(self._tree_states) > 0:
      return self._tree_states.pop().get_state()
    return []

