from typing import Optional

class AliceShortMemory:
    def __init__(self):
        """
        Initializes the class instance with an empty memory dictionary.
        """
        self.memory = {}
    
    async def init_memory(self, id: str):
        """
        Asynchronously initializes the memory for the given id.

        Args:
            self: The current instance of the class.
            id (str): The identifier for the memory to be initialized.

        Returns:
            None
        """
        self.memory[id] = []
    
    async def add_to_memory(self, memory: dict, id: str):
        """
        Asynchronously adds the provided memory to the dictionary with the specified ID.

        Args:
            self: The object instance
            memory (dict): The memory to be added
            id (str): The ID of the dictionary to which the memory will be added
        """
        self.memory[id].append(memory)
        
    async def get_memory(self, id: str):
        """
        A description of the entire function, its parameters, and its return types.
        """
        return self.memory[id]
    
    async def remove_from_memory(self, id: str):
        """
        Removes the memory associated with the given ID.

        Parameters:
            id (str): The ID of the memory to be removed.

        Returns:
            None
        """
        self.memory[id] = []
            
    async def auto_clear_memory(self, id: str, limit: Optional[int] = 20):
        """
        Asynchronous function to automatically clear the memory associated with a given ID. 
        :param id: A string representing the ID of the memory to be cleared. 
        :param limit: An optional integer representing the maximum number of items to retain in the memory. Default is 20. 
        :return: None
        """
        if len(self.memory[id]) > limit:
            self.memory[id] = self.memory[id][-limit:]
            
            
