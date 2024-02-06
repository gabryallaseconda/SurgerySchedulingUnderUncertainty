

from block import MasterBlock

class Master():

    def __init__(self, description: str, blocks: list[MasterBlock]):
        self.description = description
        self.blocks = blocks

    # getters and setter
    def get_description(self):
        return self._description
    
    def set_description(self, new: int):
        self._description = new
    
    description = property(get_description, set_description)
        
    def get_blocks(self):
        return self._blocks
    
    def set_blocks(self, new: int):
        self._blocks = new
    
    blocks = property(get_blocks, set_blocks)
