import os
import json

def read_cache():
    #read the json list
    current_directory = os.path.dirname(os.path.abspath(__file__))
    CACHE_FILENAME = os.path.join(current_directory, 'cache.json')
    #CACHE_FILENAME = "/cache.json"
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

class ResNode:

    root=None
    def __init__(self,json):

        self.address=json['formatted_address']
        self.location=json['geometry']["location"]
        self.name=json['name']

        if "plus_code" in json and "global_code" in json["plus_code"]:
            self.id=json["plus_code"]["global_code"]
        else:
            self.rating="no global code"

        if 'rating' in json:
            self.rating=json["rating"]
        else:
            self.rating=0
        
        self.left=None
        self.right=None
        

    def print_node(self):
        print(f"name={self.name}, rating={self.rating}, address={self.address}")
    
    
    def hasLeftChild(self):
        if self.left==None:
            return False
        else:
            return True
        
    def hasRightChild(self):
        if self.right==None:
            return False
        else:
            return True
    
    def tree_text_repr(self, indent=0):
        result = "  " * indent + f"{self.name} (Rating: {self.rating})\n"
        if self.left:
            result += self.left.tree_text_repr(indent + 1)
        if self.right:
            result += self.right.tree_text_repr(indent + 1)
        return result


def json_to_nodelist(place_json):
    NodeList=[]
    for i in range(len(place_json)):
        curNode=ResNode(place_json[i])
        NodeList.append(curNode)
    
    return NodeList

def add_node_totree(putList,currentNode):
    if putList[0].rating < currentNode.rating:
        if currentNode.hasLeftChild():
            add_node_totree(putList,currentNode.left)
        else:
            currentNode.left = putList[0]
    elif putList[0].rating >= currentNode.rating:
        if currentNode.hasRightChild():
            add_node_totree(putList,currentNode.right)
        else:
            currentNode.right = putList[0]
        
def place_to_tree(NodeList):
    if ResNode.root==None: 
        ResNode.root=NodeList[0]
        NodeList=NodeList[1:]  
    while len(NodeList)>=1:
        add_node_totree(NodeList, ResNode.root)
        NodeList=NodeList[1:]
            
def inorder_traversal(node):
    if node:
        inorder_traversal(node.left)
        node.print_node()  # 输出节点信息
        inorder_traversal(node.right)


def print_tree():
    if ResNode.root:
        print(ResNode.root.tree_text_repr())

place_json=read_cache()
NodeList=json_to_nodelist(place_json)

place_to_tree(NodeList)

#inorder_traversal(ResNode.root)

print_tree()