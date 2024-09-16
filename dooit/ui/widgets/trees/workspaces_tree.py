from typing import List, Optional
from textual import on
from textual.widgets import ContentSwitcher
from textual.widgets.option_list import Option
from dooit.api.workspace import Workspace
from dooit.ui.widgets.trees.todos_tree import TodosTree
from .model_tree import ModelTree
from ._render_dict import WorkspaceRenderDict


class WorkspacesTree(ModelTree[Workspace, WorkspaceRenderDict]):

    def __init__(self, model: Workspace) -> None:
        render_dict = WorkspaceRenderDict(self)
        super().__init__(model, render_dict)

    def _get_parent(self, id: str) -> Optional[Workspace]:
        return Workspace.from_id(id).parent_workspace

    def _get_children(self, id: str) -> List[Workspace]:
        return Workspace.from_id(id).workspaces

    @on(ModelTree.OptionHighlighted)
    async def update_todo_tree(self, event: ModelTree.OptionHighlighted):
        if not event.option_id:
            return

        switcher = self.screen.query_one("#todo_switcher", expect_type=ContentSwitcher)
        todo_obj = self._renderers[event.option_id].model
        tree = TodosTree(todo_obj)

        if not self.screen.query(f"#{tree.id}"):
            await switcher.add_content(tree, set_current=True)

        switcher.current = tree.id

    def _switch_to_todos(self) -> None:
        try:
            if not self.node.id:
                return

            tree = TodosTree(self.current.model)
            self.screen.query_one(f"#{tree.id}", expect_type=TodosTree).focus()
        except ValueError:
            self.notify("No workspace selected")

    def add_workspace(self) -> str:
        workspace = self.model.add_workspace()
        renderer = self._renderers[workspace.uuid]
        self.add_option(Option(renderer.prompt, id=renderer.id))
        return workspace.uuid

    def _create_child_node(self) -> Workspace:
        return self.current_model.add_workspace()

    def _force_refresh(self) -> None:
        highlighted = self.highlighted
        self.clear_options()

        options = []

        def add_children_recurse(model: Workspace):
            for child in model.workspaces:
                render = self._renderers[child.uuid]
                options.append(Option(render.prompt, id=render.id))

                if self.expanded_nodes[child.uuid]:
                    add_children_recurse(child)

        add_children_recurse(self.model)
        self.add_options(options)
        self.highlighted = highlighted
