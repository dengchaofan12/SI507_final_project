from tree_generator import *
import pandas as pd
import json
from flask import Flask, render_template

LAKE_DATA = {}
def load_cache():
    try:
        cache_file = open(TREE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def print_first_user_command_choice(continent):
    i=1
    for item in continent:
        print(str(i)+ ". " + str(item['name']))
        i= i+1
    
def print_second_user_command_choice(countries):
    i=1
    for item in countries:
        print(str(i)+ ". " + str(item['name']))
        i= i+1


def print_third_user_command_choice(lake_list):
    i=1
    for item in lake_list:
        print(str(i)+ ". " + str(item['name']))
        i= i+1
def text_display(data):
    headers=["Picture", "Max_Depth", "Altitude", "Volume",  "Country", "Continent"]
    df = pd.DataFrame(data, headers)
    print(df)


app = Flask(__name__)

@app.route('/')
def index():
    lake_name = list(LAKE_DATA.keys())
    return render_template('display_data.html', name = lake_name[0], list = LAKE_DATA[lake_name[0]])   

if __name__ == '__main__':
    continent_dict = load_cache()
    continent_dict = continent_dict['children']
    print_first_user_command_choice(continent_dict)
    #ask first question
    while True:
        user_input = input("Enter an integer number or specific continent name: ")
        lake_country_network = None
        if (user_input == "exit"):
            break
        else:
            if (user_input.isdigit()):
                try:
                    lake_country_network = continent_dict[int(user_input)-1]
                    continent_name = lake_country_network['name']
                except:
                    print("[Error] Please enter integer number")
                    continue
            else:
                
                for continent in continent_dict:
                    if (continent['name'] == user_input):
                        lake_country_network = continent
                        continent_name = user_input
                if (lake_country_network == None):
                    print("[Error] Please enter an integer number")
                    continue
            
            lake_country_network = lake_country_network["children"]
            country_lake_data = print_second_user_command_choice(lake_country_network)
            country_lakes = None

            # ask second question
            while True:
                user_input = input("Enter an integer number or specific country name: ")
                if (user_input == "exit"):
                    exit_flag = 1
                    break
                else:
                    if (user_input.isdigit()):
                        try:
                            country_lakes = lake_country_network[int(user_input)-1]
                            country_name = country_lakes['name']
                        except:
                            print("[Error] Please enter integer number")
                            continue
                    else:
                        for country in lake_country_network:
                            if (country['name'] == user_input):
                                country_lakes = country
                                continent_name = user_input
                        if (country_lakes == None):
                            print("[Error] Please enter an integer number")
                            continue
                    
                    country_lakes = country_lakes['children']
                    single_lake_data = print_third_user_command_choice(country_lakes)
                    lake_data = None

                    #ask third question
                    while True:
                        user_input = input("Enter an integer number or specific lake name: ")
                        if (user_input == "exit"):
                            exit_flag = 1
                            break
                        else:
                            if (user_input.isdigit()):
                                try:
                                    lake_data = country_lakes[int(user_input)-1]
                                    lake_name = lake_data['name']
                                except:
                                    print("[Error] Please enter integer number")
                                    continue
                            else:
                                for lake in country_lakes:
                                    if (lake['name'] == user_input):
                                        lake_data = lake
                                        lake_name = user_input
                                    if (lake_data == None):
                                        print("[Error] Please enter an integer number")
                                        continue
                            
                            lake_list = lake_data['values']
                            lake_list.append(country_name)
                            lake_list.append(continent_name)
                            lake_data = {}
                            lake_data[lake_name] = lake_list
                            LAKE_DATA = lake_data
                            while True:
                                user_command =  input("Display in Text or Flask Table 1. Text 2.Flask: ")
                                if (user_command == '1'):
                                    text_display(lake_data)
                                    exit_flag = 1
                                    break
                                elif (user_command == '2'):
                                    app.run()
                                    exit_flag = 1
                                    break
                                elif (user_command == "exit"):
                                    exit_flag = 1
                                    break
                                else:
                                    print("[Error] Please enter proper information")
                                    continue
                        if exit_flag == 1:
                            break
                if exit_flag == 1:
                    break
        if exit_flag == 1:
            break
    print()