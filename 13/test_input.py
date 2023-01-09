class InputObj:
    
    def __init__(self):
        self.left = []
        self.right = []
        self.add_to_left = True
        self.total_item = 0

    def add(self, x):
        if self.add_to_left:
            self.total_item += 1
            self.left.append(x)
            self.add_to_left = False
            return
        self.right.append(x)
        self.add_to_left = True
        
input_obj = InputObj()

input_obj.add([1,1,3,1,1])
input_obj.add([1,1,5,1,1])

input_obj.add([[1],[2,3,4]])
input_obj.add([[1],4])

input_obj.add([9])
input_obj.add([[8,7,6]])

input_obj.add([[4,4],4,4])
input_obj.add([[4,4],4,4,4])

input_obj.add([7,7,7,7])
input_obj.add([7,7,7])

input_obj.add([])
input_obj.add([3])

input_obj.add([[[]]])
input_obj.add([[]])

input_obj.add([1,[2,[3,[4,[5,6,7]]]],8,9])
input_obj.add([1,[2,[3,[4,[5,6,0]]]],8,9])