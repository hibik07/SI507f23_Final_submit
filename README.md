# SI507f23_Final_submit
only for the code in SI507f23 final project submit<br>


##Instruction

This code can be run directly in command. To execute the code, just execute the main.py file in the prompt.<br>

During the process of running, the code will give some interactive prompts. You can follow the prompts to enter the relevant content.

Calls to the API use the developer's key and do not require you to provide your own key (if you have one, you also can use it. Here will be place for you to enter).

At any moment, try to type the words that are suggested on the command line as possible as you can.

Some of the parameters that need to be entered when interacting are referenced below:<br>
--cache: type yes/no to load/not-load the cache file <br>
--key: type your key or type 'no' to use author's key <br>
--kind of place: a possible tag among google map's POI tags (hospital/cafe/school...) <br>
--which place: be specific to a name of city/street/address (Detroit/LA/123 Main St...) <br>
--radius: a distance away from centre point of place. Type 1000 to represent 1000 meters <br>
--func & form: type given number to choose corresponding function. Entering anything else will not report an error, but will enter a re-type. <br>
--sorting attributes: type rating/name/id. Entering anything else will not report an error, but will enter a re-type. <br>
--filter number: type any number (can be int/double) between 0-5. Beyond number won't report an error but will show empty result. Negative number will show all the results. <br>


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
