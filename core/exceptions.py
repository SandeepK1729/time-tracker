

class TaskNotFoundException(Exception):
    """ Raised when a task is not found in the database. """
    
    def __init__(self, id: int):
        """ Constructor for TaskNotFoundException class
        
        Args:
            id (int): task id
        """
        self.message = f"Task with {self.args} not found"
        
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    