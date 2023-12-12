# SI507f23_Final_submit
only for the code in SI507f23 final project submit

##Instruction

This code can be run directly in command. 

During the process of running, the code will give some interactive prompts. You can follow the prompts to enter the relevant content.

Calls to the API use the developer's key and do not require you to provide your own key (if you have one, you also can use it. Here will be place for you to enter).


##Requirements

requests==2.31.0, 
matplotlib==3.7.1, 
pandas==2.0.3, 
json5==0.9.6
jsonpatch==1.32
jsonpointer==2.1
jsonschema==4.17.3


##Data Structure

In this project, the results were initially captured in json format and the "results" were presented as a list. 
Subsequently, I built a ResNode class with class attributes such as leftchild and rightchild. I constructed each result in the list as an instance of the class, and turned the entire result list into a list in which each element is an instance of the class. The treenode based on the size of the rating. If the rating of one node is smaller than the current node, it will be as the left child node, and larger than that as the right child node.
