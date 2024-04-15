# bot.py
import requests
import json
import datetime
import random
from utils import create_grid, getColumnCharacterToNumber, get_movable_coordinates
from database import get_db_connection
from openai_module import get_openai_response
from abilities import AbilityHandler

class Bot:
    def __init__(self, cursor, cnx, entity='Bob', personality='', initial_position='A1', bots=[], ability='', action=''):
        self.cursor = cursor
        self.cnx = cnx
        self.entity = entity
        self.ability = ability
        self.action = action
        self.personality = personality
        self.position = initial_position
        self.initial_position = initial_position
        self.bots = bots
        self.health_points = 100
        self.ability_handler = AbilityHandler(cursor, cnx)  # Initialize the ability handler

    def use_ability(self, ability_name, target):
        target_entity = self.clean_ability_target(target)
        if target_entity != '0':
            self.ability_handler.use_ability(self.entity, target_entity)

    def fetch_and_set_initial_position(self):
        time, position, history, health_points, ability = self.fetch_last_data()
        if position in create_grid():
            self.position = position
        else:
            self.position = self.initial_position

    def add_bots(self, bots):
        self.bots = bots

    def generate_bot_data(self, time, position, movable_coordinates, nearby_entities, history, health_points):
            data = {
                "present_time":{
                    "your_name": self.entity,
                    "your_personality": self.personality,
                    "available_ability": self.ability,
                    "health_points": health_points,
                    "time": time,
                    "position": position,
                    "movable_coordinates": movable_coordinates,
                    "nearby_entities": nearby_entities
                },
                "history": history
            }
            return data

    def is_alive(self):
        return self.fetch_last_data()[3] > 0

    def send_to_bot(self, data):
        print(f'Data sent to {self.entity} AI Bot:\n', json.dumps(data, indent=2))
        try:
            # Serialize the dictionary to JSON string format
            user_content = json.dumps(data)
            # Getting the raw response from the OpenAI module
            response_json = get_openai_response(user_content)
            print(f"Raw JSON response from OpenAI for {self.entity}:\n", response_json)

            # Try parsing the JSON response to the dictionary
            response_dict = json.loads(response_json)
            print(f"Parsed response for {self.entity} after JSON loads:\n", response_dict)

            return response_dict
        except json.JSONDecodeError as e:
            print(f'JSON Decoding error while processing response for {self.entity}:', e)
        except Exception as error:
            print(f'General error occurred while sending data to {self.entity}:', error)
        
        # If we can't parse or if an error occurs, return None or a default response structure
        return None

    def insert_data(self, entity, thought, talk, position, time, health_points, ability_target):
        query = ("INSERT INTO aiworld "
                "(time, position, entity, thought, talk, move, health_points, ability, timestamp) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
        values = (time, position, entity, thought, talk, position, health_points, ability_target, datetime.datetime.now())
        print("Inserting into Database:\n", query)
        self.cursor.execute(query, values)
        self.cnx.commit()

    def clean_ability_target(self, response_ability):
        """
        Extracts the target entity's name from a response ability string
        """
        # Assume self.bots is a list of all bot instances
        valid_entities = {bot.entity for bot in self.bots}  # Create a set for faster lookup
        for entity in valid_entities:
            if entity in response_ability:
                return entity
        return '0'  # return '0' if no valid entity is found

    def fetch_last_data(self):
        self.cursor.execute("SELECT e.hp, a.time, a.position, a.entity, a.thought, a.talk, a.move, a.health_points, a.ability FROM aiworld a JOIN entities e ON a.entity = e.name WHERE a.entity=? ORDER BY a.time DESC LIMIT 1", (self.entity,))
        row = self.cursor.fetchone()
        if row:
            max_hp = row[0]
            time = row[1] + 1
            position = row[5] if row[5] in create_grid() else row[2]
            health_points = row[7]
            ability = row[8]
            self.cursor.execute("SELECT time, position, entity, thought, talk, move, health_points, ability FROM aiworld WHERE entity=? ORDER BY time DESC LIMIT 12",
                                (self.entity,))
            all_rows = self.cursor.fetchall()
            history = []
            for a_row in all_rows:
                current_dict = dict(zip(('time', 'position', 'entity', 'thought', 'talk', 'move', 'health_points', 'ability'), a_row))
                history.append(current_dict)
        else:
            self.cursor.execute("SELECT hp FROM entities WHERE name=?", (self.entity,))
            max_hp = self.cursor.fetchone()[0]
            time = 1
            position = self.initial_position
            health_points = max_hp  # Initialize to max_hp if no history
            ability = ''
            history = []
        self.health_points = health_points  # Update the bot's health_points attribute
        return time, position, history, health_points, ability, max_hp
    
    def fetch_nearby_entities_for_history(self):
        history = []
        for a_row in self.history:
            current_dict = a_row
            nearby_entities_from_past = []
            for other_bot in self.bots:
                if other_bot.entity == self.entity:
                    # Update the current bot's action in the same format as nearby entities
                    if current_dict['ability'] and current_dict['ability'] != '0':
                        current_dict['action'] = f"{self.ability}:{current_dict['ability']}"
                    else:
                        current_dict.pop('ability', None)  # Remove the 'ability' field if it's '0' or empty
                    continue
                self.cursor.execute("SELECT position, talk, health_points, ability FROM aiworld WHERE entity=? AND time<=? ORDER BY time DESC LIMIT 1", (other_bot.entity, a_row['time']))
                row = self.cursor.fetchone()
                if row:
                    other_bot_position, other_bot_talk, other_bot_health_points, other_bot_ability = row[0], row[1], row[2], row[3]
                    if ':' in other_bot_ability:
                        other_bot_action = other_bot_ability
                    else:
                        other_bot_action = f"{other_bot.ability}:{other_bot_ability}" if other_bot_ability and other_bot_ability != '0' else ''
                    pos_col = getColumnCharacterToNumber(other_bot_position[0])
                    pos_row = int(other_bot_position[1:])
                    self_col = getColumnCharacterToNumber(current_dict['position'][0])
                    self_row = int(current_dict['position'][1:])
                    if max(abs(pos_col - self_col), abs(pos_row - self_row)) <= 2:
                        nearby_entity = {
                            "name": other_bot.entity,
                            "talks": other_bot_talk,
                            "position": other_bot_position,
                            "health_points": other_bot_health_points
                        }
                        if other_bot_action:
                            nearby_entity["action"] = other_bot_action
                        nearby_entities_from_past.append(nearby_entity)
            current_dict["nearby_entities"] = nearby_entities_from_past if nearby_entities_from_past else {"nearby": []}
            history.append(current_dict)
        return history

    def fetch_current_talk_and_position(self, entity):
        self.cursor.execute("SELECT position, talk FROM aiworld WHERE entity=? ORDER BY time DESC LIMIT 1", (entity,))
        row = self.cursor.fetchone()
        if row:
            position, talk = row[0], row[1]
        else:
            position, talk = self.initial_position, ""
        return position, talk

    def communicate_with_bot(self, bot_data):
        # Fetch the last data stored from the previous communications or initial defaults
        time, position, self.history, health_points, ability, max_hp = self.fetch_last_data()
        self.position = position

        # Define current bot's column and row based on its position
        col = getColumnCharacterToNumber(self.position[0])
        row = int(self.position[1:])

        # Create a list of valid positions that the bot can move to on a grid
        grid = create_grid()
        movable_coordinates = get_movable_coordinates(position, grid)
        nearby_entities = {}

        # Evaluate and collect data on bots within a certain distance
        for other_bot in self.bots:
            if other_bot.entity == self.entity:
                continue
            other_bot_position, other_bot_talk = other_bot.fetch_current_talk_and_position(other_bot.entity)
            other_bot_health_points, other_bot_ability, other_bot_max_hp = other_bot.fetch_last_data()[3], other_bot.fetch_last_data()[4], other_bot.fetch_last_data()[5]
            other_bot_action = f"{other_bot.ability}:{other_bot_ability}" if other_bot_ability else ''
            if max(abs(getColumnCharacterToNumber(other_bot_position[0]) - col), abs(int(other_bot_position[1:]) - row)) <= 2:
                if not nearby_entities:
                    nearby_entities = {"nearby": []}
                nearby_entity = {
                    "name": other_bot.entity,
                    "talks": other_bot_talk if other_bot_talk else "",
                    "position": other_bot_position,
                    "health_points": other_bot_health_points
                }
                if other_bot_action and other_bot_action not in ["attack:0", "heal:0"]:
                    nearby_entity["action"] = other_bot_action
                nearby_entities['nearby'].append(nearby_entity)

        # Fetch and format the history data for nearby entities compared with the current bot
        updated_history = self.fetch_nearby_entities_for_history()
        bot_info = self.generate_bot_data(time, position, movable_coordinates, nearby_entities, updated_history, health_points)

        # Send formatted data to the openai module and receive a response dict
        response = self.send_to_bot(bot_info)
        print(f"Response from {self.entity} AI Bot:\n", json.dumps(response, indent=2))

        # Process the received response, check and manipulate data based on the action defined
        if response:
            next_position = response.get('move', position)
            ability_target = response.get('ability', '0')
            cleaned_ability_target = self.clean_ability_target(ability_target)
            thought = response.get('thought', '')
            talk = response.get('talk', '')
            
            # Check if the next_position is valid and among the movable coordinates
            if next_position != '0' and next_position in movable_coordinates:
                # Update the position only if it's valid
                position = next_position
            
            # Insert the processed data back into the database
            self.insert_data(self.entity, thought, talk, position, time, health_points, cleaned_ability_target)

            # Use the ability if specified
            if cleaned_ability_target != '0':
                self.use_ability(ability, cleaned_ability_target)

        else:
            print("No valid data received from bot")

        for bdata in bot_data:
            if bdata['entity'] == self.entity:
                bdata['position'] = self.position
                bdata['time'] = self.fetch_last_data()[0]
                bdata['talk'] = self.fetch_current_talk_and_position(self.entity)[1]
                bdata['pos_col'] = getColumnCharacterToNumber(self.position[0])
                bdata['pos_row'] = int(self.position[1:])
                bdata['health_points'] = self.health_points
                bdata['action'] = f"{self.ability}:{ability_target}" if ability_target != '0' else ''