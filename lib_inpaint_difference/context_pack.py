from gradio.context import Context
from gradio.blocks import BlockContext

from modules.scripts import script_callbacks


class WebuiContextPack:
    def __init__(self):
        self.context_blocks = {}

    def _index_of_child(self, elem_id):
        for child in self.context_blocks[elem_id].children:
            if child.elem_id == elem_id:
                return child

        raise ValueError(f'No child {elem_id} in the context block.')

    def _create_new_block(self, elem_id, *args, after=False, **kwargs):
        new_block = BlockContext(*args, **kwargs)
        parent_block = self.context_blocks[elem_id].children
        child_index = self._index_of_child(elem_id) + (1 if after else 0)
        parent_block.children[child_index:child_index] = [new_block]
        new_block.parent = parent_block
        return new_block

    def register_context_block_at(self, elem_id: str) -> None:
        self.context_blocks[elem_id] = Context.block

    def before(self, target_elem_id: str, *args, **kwargs):
        return BlockManager(self._create_new_block(target_elem_id, *args, after=False, **kwargs))

    def after(self, target_elem_id: str, *args, **kwargs):
        return BlockManager(self._create_new_block(target_elem_id, *args, after=True, **kwargs))


WebuiContextPack = WebuiContextPack()


class BlockManager:
    def __init__(self, block):
        self.block = block

    def __enter__(self):
        self.previous_block = Context.block
        Context.block = self.block
        return self

    def __exit__(self, *args, **kwargs):
        Context.block = self.previous_block


class ParentBlock(BlockManager):
    def __init__(self):
        super().__init__(Context.block.parent)


def on_after_component(_, **kwargs):
    elem_id = kwargs.get('elem_id', None)

    if elem_id is not None:
        WebuiContextPack.register_context_block_at(elem_id)


script_callbacks.on_after_component(on_after_component)
