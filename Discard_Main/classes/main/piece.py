from .generic.position import Position

class Piece:
    """Bace Class for Creature and Leader pieces
    # NOTE: Creatures and Leaders will be Classes decended from this.
    """

    def __init__(self, player, name, hp, speed, move_style, position_notation):
        self.player=player #the player object this piece belongs to.
        self.name=name
        self.max_hp=hp
        self.damage=0
        #Current HP= max_hp - damage.
        self.speed=speed
        self.move_style=move_style #The multilined text
        self.move_limit=1
        #Speed is 1-100.
        self.position=Position(notation=position_notation)
    def get_move_options(self, grid): #Wip function.
        """supposed to split move style into list line by line."""
        lines=self.move_style.splitlines()
        for line in lines:
            print(grid.get_all_movements_in_range(self.position, line))

        # print(grid.get_all_movements_in_range(self.position, "SAME COLUMN"))
        # print(grid.get_all_movements_in_range(self.position, "SAME ROW"))
        # print(grid.get_all_movements_in_range(self.position, "SAME COLUMN LIMIT 1"))
        # print(grid.get_all_movements_in_range(self.position, "SAME ROW LIMIT 1"))
        # print(grid.get_all_movements_in_range(self.position, "HOP X 1"))
        # print(grid.get_all_movements_in_range(self.position, "HOP Y 1"))
        # print(grid.get_all_movements_in_range(self.position, "HOP X -1"))
        # print(grid.get_all_movements_in_range(self.position, "HOP Y -1"))
        # print(grid.get_all_movements_in_range(self.position, "HOP Y -1 X -1"))
        # print(grid.get_all_movements_in_range(self.position, "HOP X 1 Y 1"))
    def add_damage(self, damage_add=0):

        self.damage=self.damage+ damage_add

        print("Add Damage is incomplete.")

    def change_position(self, new_position_notation):
        self.position=Position(notation=new_position_notation)
    #To Do- String Rep.  Rep will be Icon, Name, and Position

class Creature(Piece):
    """Creature class.  This is what all creatures will be summoned into."""


#Driver Code.
if __name__ == "__main__":
    testPiece=Piece("LO", "MY_NAME", 5,5, "STEP 1", "B3")
    print(testPiece.position.x_y())
