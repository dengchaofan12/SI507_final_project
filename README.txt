Before run the program, user need to change the PATH in data_fetch.py into corresponding path

The run sequence is data_fetch ---   tree_generator  ---   user_interact_load_tree

This program will help user find specific lake around the world and display its depth, volume and so on.


There are four question user will be asked:
    1.	Which continent you are choosing?
    2.	Which Country you are choosing?
    3.	Which lake you are choosing?
    4.	Which format you want to display (text or flask table)?
Before making decision, choices will be print out in the command window. User can either type in speicific name
or choose numerial number to make decision. User is free to exit at all time.

There are three programs in this project:
    1. data_fetch.py     this program will fetch all required data from APIs and stored all HTML code in data_storage/final_project_source.json
                         and all processed information in data_storage/data_structure.json
    2. tree_generator.py   this program will generate a tree struture based on data_structure created by data_fetch.py 
                           and stored into data_storage/tree_structure.json
    3. user_interact_load_tree.py    this program will load tree structure from json and prompt user questions, after receive all answer, result
                                     will be displayed based on user choice, either on text table in command line or flask table

            