# Python STL

# Packages
import pandas as pd

# Modules
from .block import MasterBlock

class Master():

    def __init__(self, table: pd.DataFrame, name: str = ""):
        self._name = name
        
        #######
        # Processing table data
        
        ### Checks
        
        # Check the table format
        if not isinstance(table, pd.DataFrame):
            raise TypeError("The argument 'table' must be a pandas' dataframe.")

        # Check that the dataframe has exactly 4 columns
        if len(table.columns) != 4:
            raise ValueError("The 'table' dataframe must have exactly 4 columns.")

        # Check columns names
        required_columns = ['weekday', 'equipes', 'room', 'duration']
        for col in required_columns:
            if col not in table.columns:
                raise ValueError(f"The 'table' dataframe must contain the column '{col}'.")

        # Check data type in the column'weekday'
        if not table['weekday'].dtype == int:
            raise TypeError("The 'weekday' column must contain only integer values.")

        # Verifica il tipo di dati nella colonna 'equipe' # TODO
        if not all(isinstance(equipe, str) for equipe in table['equipes']):
            raise TypeError("The 'equipe' column must contain only strings.")

        # TODO: aggiungere verifica colonna 'room'
        
        # Verifica il tipo di dati nella colonna 'duration' # TODO
        if not all(isinstance(duration, (int, float)) for duration in table['duration']):
            raise TypeError("The 'duration' column must contain only integer or float values.")

        ### Processing
        
        self._week_length = table['weekday'].max()

        self._blocks = []
        
        order_in_master = 0
                
        for weekday in range(1, self._week_length + 1):
            weekday_data = table[table['weekday'] == weekday]
            
            # Consistency in weekday numeration check
            if len(weekday_data) == 0:
                raise ValueError(f"Missing data for weekday {weekday}.")
            
            for order_in_day, row in enumerate(weekday_data.itertuples(), start=1):
                
                equipes = [x.strip() for x in row.equipes.split(',')]
                
                block = MasterBlock(duration=row.duration, 
                                    equipes=equipes, 
                                    room = row.room,
                                    weekday=row.weekday,
                                    order_in_day=order_in_day, 
                                    order_in_master=order_in_master)
                
                self._blocks.append(block)
                order_in_master += 1
                
        self._num_of_blocks = len(self._blocks)
        
        
    def __str__(self):
        return f"Master '{self._name}' - {self._num_of_blocks} blocks on {self._week_length} days."    
        

    # Getters and setter
    def get_description(self):
        return self._description
    
    def set_description(self, new: int):
        self._description = new
    
    description = property(get_description, set_description)


    def get_blocks(self):
        return self._blocks
    
    blocks = property(get_blocks)
    
    #def get_block_duration(self, block_index: int):
    #    return self._blocks[block_index].get_duration()
        
    
    # Getters of master's characteristics
    def get_num_of_rooms(self):
        rooms = set()
        for block in self._blocks:
            rooms.add(block.room)
        return len(rooms)

    def get_num_of_blocks(self):
        return self._num_of_blocks

    def get_week_length(self):
        return self._week_length
    
    
