import json
import requests
import os
import matplotlib.pyplot as plt
import pandas as pd
import time



def get_location(my_key):

    url="https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    if my_key=="no":
        my_key='AIzaSyA_NPvNiC3cLQX9IsKIOzHG63JGDTecGDw'

    search_kind=input("what kind of place you want to search? ")
    search_location=input("and based on which place? (can be specific to a city/road/address)")
    search_location=replace_spaces(search_location)
    search_radius=input("do you have any radius restrict? if have, enter the number, if no, enter any: ")
    if search_radius.isdigit():
        radius=search_radius
        url_place=url+search_kind+"%20in%20"+search_location+"&radius="+radius+"&key="+my_key
    else:
        url_place=url+search_kind+"%20in%20"+search_location+"&key="+my_key
    

    #start the first search
    place_req=requests.get(url_place)

    if place_req.status_code==200:
        print("loading the first page....")
        place_json_initial=place_req.json()
        place_json=place_json_initial['results']
        if "next_page_token" in place_json_initial:
            next_page_token=place_json_initial["next_page_token"]
        else:
            next_page_token=""

    while next_page_token!="":
        
        url_next=url_place+'&pagetoken='+next_page_token
        time.sleep(2)
        place_req_next=requests.get(url_next)
        print("loading the next page....")
        
        if place_req_next.status_code==200:
            place_json_next=place_req_next.json()
            place_json_new=place_json_next['results']

            place_json.extend(place_json_new)

            if "next_page_token" in place_json_next:
                next_page_token=place_json_next["next_page_token"]
            else:
                next_page_token=""
        else:
            print("Error in the next page request:", place_req_next.status_code)
            print(place_req_next.text)


    return place_json

def save_cache(place_json):
    #save original json list into cache
    current_directory = os.path.dirname(os.path.abspath(__file__))
    CACHE_FILENAME = os.path.join(current_directory, 'cache.json')
    dumped_json_cache = json.dumps(place_json)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

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

def replace_spaces(input_string):
    return input_string.replace(" ", "%20")

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

def json_to_nodelist(place_json):
    NodeList=[]
    for i in range(len(place_json)):
        curNode=ResNode(place_json[i])
        NodeList.append(curNode)
    
    return NodeList
    
def sort_by_bubble(NodeList,attri):
    for i in range(len(NodeList)):
        for j in range(0, len(NodeList)-1):
            try:
                current_value = getattr(NodeList[j], attri)
                next_value = getattr(NodeList[j+1], attri)

                if attri == "name":
                    current_value = current_value.lower()
                    next_value = next_value.lower()

                if current_value >= next_value:
                    NodeList[j], NodeList[j+1] = NodeList[j+1], NodeList[j]
            except TypeError:
                pass
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

def inorder_traversal_filt(node,num):
    if node:
        inorder_traversal_filt(node.left,num)
        if node.rating>=num:
            node.print_node()  # 输出节点信息
        inorder_traversal_filt(node.right,num)

def nodelist_to_chart(NodeList):
    data = {
    'address': [node.address for node in NodeList],
    'name': [node.name for node in NodeList],
    'rating': [node.rating for node in NodeList],
    'latitude': [node.location['lat'] for node in NodeList],
    'longitude': [node.location['lng'] for node in NodeList],
    }
    df = pd.DataFrame(data)

    plt.scatter(df['longitude'], df['latitude'], s=df['rating']*10,c=df['rating'],alpha=0.7,cmap='viridis')

    plt.title('Distribution of the Results')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    colorbar = plt.colorbar()
    colorbar.set_label('Rating')

    plt.show()




def select_func():
    print("select the function you need:\n",
          "1.simply show the result\n",
          "2.sort the result by one of the attributes\n",
          "3.filter result by rating number"
          )
    func=int(input("func="))

    return func

def give_function(func,NodeList):
    if func==1:
        print("and in what form?\n",
          "1.show result in text\n",
          "2.show distribution of result in Figure",)
        form=int(input("form="))
        while form not in [1,2]:
            form=int(input("please input again: "))
        if form==1:
            inorder_traversal(ResNode.root)
        elif form==2:
            nodelist_to_chart(NodeList)
    elif func==2:
        attri=input("which attribute you want to sort by?you can choose among:\nrating, name, id: ")
        while attri not in ['rating', 'name', 'id']:
            attri=input("please input again: ")
        NodeList_sort=sort_by_bubble(NodeList,attri)
        for node in NodeList_sort:
            node.print_node()
    elif func==3:
        print("and in what form?\n",
          "1.show result in text\n",
          "2.show distribution of result in Figure",)
        form=int(input("form="))
        while form not in [1,2]:
            form=int(input("please input again: "))
        filtnum=float(input("you want the rating number >= :"))
        if form==1:
            inorder_traversal_filt(ResNode.root,filtnum)
        elif form==2:
            new_Nodelist=[node for node in NodeList if node.rating>=filtnum]
            nodelist_to_chart(new_Nodelist)
        else:
            pass
    




def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path_cache = os.path.join(current_directory, "cache.json")

    cache_ans="no"

    if os.path.exists(file_path_cache) is True:
        #cache_ans='no'
        cache_ans=input("You have a cache file. Do you want to read the cache? yes/no ")
    
    if cache_ans=="yes":
        place_json=read_cache()
        NodeList=json_to_nodelist(place_json)
    else:
        print(f"Please start a new search: ")
        my_key=input("do you have a key for google map api? If have, enter your key. If not, enter 'no': ")
        place_json=get_location(my_key)
        save_cache(place_json)
        NodeList=json_to_nodelist(place_json)
  
    place_to_tree(NodeList)

    print("We've found the results on google map! Now we can start our interaction!")
    exit_ans=False

    while exit_ans==False:
        func=select_func()
        while func not in [1,2,3,4]:
            print("please input again:")
            func=select_func()
        give_function(func,NodeList)
        play_ans=input("Do you want to exit? If you want, enter 'exit'. If you want to continue, enter anything (except exit): ")
        if play_ans=="exit":
            exit_ans=True
    print("bye!")
        




if __name__ == '__main__':
      
    main()