from database.instance import DbInstance
from database.queue import DbQueue

# Kinda dirty but that's how it is
class DbVars:
    # TO BE USED STRICTLY FOR READ TASKS !
    # USE THE QUEUE OTHERWISE !
    ReadInstance = DbInstance("test.db")

    # TO BE USED STRICTLY FOR WRITE TASKS, WITH THE 
    # add_instuction() AND add_important_instruction() FUNCTIONS ! 
    # USE THE ReadInstance TO READ DATA INSTEAD !
    Queue = DbQueue("test.db")
