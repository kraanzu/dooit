from typing import List, Any
from .tree_state import TreeState

"""
Class that keeps the states of the tree structure
"""
class StateKeeper:

  """
  List with the states of the tree structure
  """
  tree_states: List[TreeState]
  removed_states: List[TreeState]

  """
  Constructor of the StateKeeper class
  """
  def __init__(self) -> None:
    self.tree_states = []
    self.removed_states = []
  
  """
  Save the actual state of the tree structure
  """
  def save_state(self, new_state: Any) -> None:
    if len(new_state) > 0:
      self.tree_states.append(TreeState(new_state))

  """
  Returns the last state of the tree structure
  """
  def return_state(self) -> Any:
    if len(self.tree_states) > 0:
      previous_state = self.tree_states.pop()
      self.removed_states.append(previous_state)
      return previous_state.get_state()
    return []

  def return_undo(self) -> Any:
    if len(self.removed_states) > 0:
      previous_state = self.removed_states.pop()
      self.tree_states.append(previous_state)
      return previous_state.get_state()
    return []
