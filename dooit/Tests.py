from .api.todo import Todo
from .api.item_concrete_creator import ItemConcreteCreator
from dooit.utils.conf_reader import Config
from dooit.utils.keybinder import KeyBinder
from dooit.ui.formatters.todo_tree_formatter import TodoFormatter
from dooit.ui.widgets import StatusBar
from dooit.ui.widgets.tree import TreeList
from dooit.ui.widgets.todo_tree import TodoTree

import unittest



class Test():
  def run():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(FactoryMethodTest))
    suite.addTests(loader.loadTestsFromTestCase(SingletonPatternTest))

    runner = unittest.TextTestRunner()
    runner.run(suite)
  

class FactoryMethodTest(unittest.TestCase):
  def test_factory_method(self):
    print("Factory Method Test")

    todo_test = Todo()
    self.assertIsNotNone(todo_test)
    print("Object Todo created")

    item_creator = ItemConcreteCreator()
    self.assertIsNotNone(item_creator)
    print("Object ItemCreator created")
    
    status = item_creator.create_status(todo_test)
    self.assertIsNotNone(status)
    print("Object Status created")

    description = item_creator.create_description(todo_test)
    self.assertIsNotNone(description)
    print("Object Description created")

    urgency = item_creator.create_urgency(todo_test)
    self.assertIsNotNone(urgency)
    print("Object Urgency created")

    effort = item_creator.create_effort(todo_test)
    self.assertIsNotNone(effort)
    print("Object Effort created")

    tags = item_creator.create_tags(todo_test)
    self.assertIsNotNone(tags)
    print("Object Tags created")

    recurrence = item_creator.create_recurrence(todo_test)
    self.assertIsNotNone(recurrence)
    print("Object Recurrency created")

    due = item_creator.create_due(todo_test)
    self.assertIsNotNone(due)
    print("Object Due created")

    self.assertNotEqual(status, description)
    print("Status and Description Object are NOT equal")

    
class SingletonPatternTest(unittest.TestCase):
    def test_singleton_pattern(self):
        print("\nSingleton Pattern Test ")

        config_instance = Config()
        self.assertIsNotNone(config_instance)
        print("First Config object created with ID: "+ str(id(config_instance)))

        format = config_instance.get("TODO")
        config_TodoFormatter = TodoFormatter(format).c 
        print("Config instance used by TodoFormatter, ID: " + str(id(config_TodoFormatter)))

        config_TreeList = TreeList().conf
        print("Config instance used by TreeList, ID: " + str(id(config_TreeList)))

        config_TodoTree = TodoTree().conf
        print("Config instance used by TodoTree, ID: " + str(id(config_TodoTree)))

        
        config_KeyBinder = KeyBinder().c
        print("Config instance used by KeyBinder, ID: " + str(id(config_KeyBinder)))
  

        self.assertIs(config_instance, config_TodoFormatter, "config_instance and config_TodoFormatter should be the same instance.")
        assert config_TodoFormatter is config_TreeList, "config_TodoFormatter and config_TreeList should be the same instance."
        assert config_TreeList is config_TodoTree, "config_TreeList and config_TodoTree should be the same instance."
        assert config_TodoTree is config_KeyBinder, "config_TodoTree and config_KeyBinder should be the same instance."
