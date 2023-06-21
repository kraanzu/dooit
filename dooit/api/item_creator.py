from .model_items import Item
from typing import Any

"""
Creator component that declare the interface to create items
"""
class ItemCreator:
  """
  Interface to create the Status for the Model
  """
  def create_status(self, model: Any) -> Item:
    pass

  """
  Interface to create the Urgency for the Model
  """
  def create_urgency(self, model: Any) -> Item:
    pass

  """
  Interface to create the Due for the Model
  """
  def create_due(self, model: Any) -> Item:
    pass

  """
  Interface to create the Description for the Model
  """
  def create_description(self, model: Any) -> Item:
    pass

  """
  Interface to create the Recurrence for the Model
  """
  def create_recurrence(self, model: Any) -> Item:
    pass

  """
  Interface to create the Effort for the Model
  """
  def create_effort(self, model: Any) -> Item:
    pass

  """
  Interface to create the Tags for the Model
  """
  def create_tags(self, model: Any) -> Item:
    pass
  