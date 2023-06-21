from .item_creator import ItemCreator
from .model_items import Item, Status, Urgency, Due, Description, Recurrence, Effort, Tags
from typing import Any

"""
Concrete Creator component that implement the method to create the Items
"""
class ItemConcreteCreator(ItemCreator):
  """
  Implementation to create the Status for the Model
  """
  def create_status(self, model: Any) -> Item:
    return Status(model)

  """
  Implementation to create the Urgency for the Model
  """
  def create_urgency(self, model: Any) -> Item:
    return Urgency(model)

  """
  Implementation to create the Due for the Model
  """
  def create_due(self, model: Any) -> Item:
    return Due(model)

  """
  Implementation to create the Description for the Model
  """
  def create_description(self, model: Any) -> Item:
    return Description(model)

  """
  Implementation to create the Recurrence for the Model
  """
  def create_recurrence(self, model: Any) -> Item:
    return Recurrence(model)

  """
  Implementation to create the Effort for the Model
  """
  def create_effort(self, model: Any) -> Item:
    return Effort(model)

  """
  Implementation to create the Tags for the Model
  """
  def create_tags(self, model: Any) -> Item:
    return Tags(model)