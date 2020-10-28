class TreeNode:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data is None:
            self.data = data
        else:
            if data < self.data:
                if self.left is None:       
                    self.left = TreeNode(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = TreeNode(data)
                else:
                    self.right.insert(data)
 
    def pre_order_print_tree(self):
       if not self.data:
           return 
       print(self.data)
       if self.left:
           self.left.pre_order_print_tree()
       if self.right:
           self.right.pre_order_print_tree()

    def in_order_print_tree(self):
       if not self.data:
           return 
       if self.left:
           self.left.in_order_print_tree()
       print(self.data)
       if self.right:
           self.right.in_order_print_tree()


    def pre_order_traverse(self, root):
        result = []
        if root:
            result.append(root.data)
            result = result + self.pre_order_traverse(root.left)
            result = result + self.pre_order_traverse(root.right)
        return result


    def in_order_traverse(self, root):
        result = []
        if root:
            result = self.in_order_traverse(root.left)
            result.append(root.data)
            result = result + self.in_order_traverse(root.right)
        return result


    def post_order_traverse(self, root):
        result = []
        if root:
            result = self.post_order_traverse(root.left)
            result = result + self.in_order_traverse(root.right)
            result.append(root.data)
        return result

    def find_value(self, value_to_find):
        if value_to_find < self.data:
            if self.left is None:
                return str(value_to_find)+" Not Found"
            return self.left.find_value(value_to_find)
        elif value_to_find > self.data:
            if self.right is None:
                return str(value_to_find)+" Not Found"
            return self.right.find_value(value_to_find)
        else:
            return(str(self.data) + ' is found')

root = TreeNode(15)
root.insert(8)
root.insert(22)
root.insert(7)
root.insert(24)
root.insert(6)
root.insert(10)
root.insert(21)

root.pre_order_print_tree()
root.in_order_print_tree()

print(root.pre_order_traverse(root))
print(root.in_order_traverse(root))
print(root.post_order_traverse(root))

print(root.find_value(7))
print(root.find_value(33))
print(root.find_value(15))
print(root.find_value(98))