# AI Bot World

Welcome to the AI Bot World, an immersive and dynamic starting point for building a vast and engaging AI-driven universe! This project harnesses the power of GPT-4 Turbo as the language model to control each bot individually, enabling you to create a world populated by intelligent entities with unique personalities (in a way), abilities, and interactions.

Now completely standalone using sqlite - only need OpenAI key - todo - allow other llm.

(this readme was mostly generated by AI, on the TODO to do properly..)

## Features

- **Diverse Entities**: Create a wide array of AI-driven entities, each with its own distinct personality (in a way), abilities, and starting position on the grid. Define their characteristics in the config page and watch them come to life! You can add and remove as many bots as you like.
- **Realistic Interactions**: Witness the bots interact, communicate, and navigate the world, making decisions based on their surroundings and objectives. With a limited perception range of 2 tiles, the bots must strategize and adapt to their environment.
- **Independent Memory**: Each bot possesses its own memory, allowing them to retain knowledge of their past interactions and experiences. This adds depth and continuity to their behavior and decision-making process.
- **Health Points and Abilities**: Bots have health points (HP) and can engage in combat or healing. With a maximum HP of 100, they can deal 10 damage when attacking or restore 10 HP when healing. This creates a dynamic and evolving world where bots must make strategic choices. Boss Bots (boss=1 in the entities table) do 10 to 60 damage or healing (random) depending on their ability.
- **Structured Environment**: The world is represented by a 500x500 grid, providing a structured and manageable environment for the bots to explore and interact with. Each cell on the grid can accommodate multiple bots, enabling complex interactions and encounters.

### AI World Demo Video
Click on the image below to watch the demo video:

[![Watch the video](https://downloads.xaya.io/screenshot.jpg)](https://downloads.xaya.io/AI-world-v1.mp4)

[![A-Star Algo for obstacle Avoidance and advancing to destinations ](https://downloads.xaya.io/astar.jpg)](https://downloads.xaya.io/astar.mp4)

## Getting Started

To embark on your AI Bot World journey, follow these steps:

1. **Bot Customization**: Customize the bot personalities, abilities, and images on the config page. You can add as many as you want (to pay for).
2. **OpenAI Key**: Add your openAI key to the openai_module.py
4. **Run the Scripts**: Run the app.py script to initiate the AI Bot World and witness the bots' interactions and evolution. The scripts will handle the bot's movement, communication, and decision-making based on their individual characteristics and the state of the world using the responses from the LLM and by passing it the history and data from the database. To view the world real time you can connect to http://127.0.0.1:5000 (built in flask app included).
5. **Explore and Expand**: Observe the bots as they navigate the grid, interact with each other, and make decisions based on their goals and constraints. Use the provided web interface to visualize the world and track the bots' progress. Feel free to expand upon the existing features and add new elements to enrich the AI Bot World experience.

## How it works?

To do - but essentially we are sending each of the bots information to the LLM, such as health points, nearby information, and historical information (unique to them) and getting a formatted json output response (output parser).

```Data sent to Mira AI Bot:
 {
  "present_time": {
    "your_name": "Lilith",
    "your_personality": "Lilith, strong evil killer. You hate Hulk. You have a heal ability and can heal yourself.",
    "available_ability": "heal",
    "health_points": 163,
    "time": 6,
    "position": [
      90,
      0
    ],
    "possible_directions": {
      "E": 10,
      "SE": 10,
      "S": 10,
      "SW": 10,
      "W": 10
    },
    "nearby_entities": {
      "Hulk": {
        "direction": "SW",
        "distance": 8,
        "health_points": 200,
        "in_talk_range": true,
        "talk": "No peace with Hulk! Hulk crush Lilith!",
        "ability": "attack",
        "ability_target": "Lilith",
        "in_range_of_heal": true
      }
    }
  },
  "history": [
    {
      "time": 5,
      "x": 90,
      "y": 0,
      "entity": "Lilith",
      "thought": "Hulk continues his aggression; I must heal and move swiftly to avoid conflict.",
      "talk": "Cease your hostility, Hulk. I seek no quarrel with you!",
      "move_direction": "NE",
      "move_distance": 10,
      "health_points": 163,
      "ability": "heal",
      "nearby_entities": [
        {
          "name": "Hulk",
          "direction": "SW",
          "distance": 8,
          "talks": "No peace with Hulk! Hulk crush Lilith!",
          "ability": "attack",
          "ability_target": "Lilith"
        }
      ]
    },]}```

A Response can look like this:

```Response from Drake AI Bot:
{
  "thought": "Hulk smash Lilith! Hulk no listen!",
  "talk": "No peace with Hulk! Hulk crush Lilith!",
  "move": "NE",
  "distance": 10,
  "ability": "attack",
  "ability_target": "Lilith"
}```


**TODO**

~~- add max ability range~~
- add more abiltiies
- add actions 
- add inventory
- add purpose
- add hunger
~~- add obstacle layer~~
~~- create map~~
- add currency
- history summary
~~- different models for different entities (set in config and allow changing model configs).~~
~~- add talk range (fixed low value)~~
- add whispering (only the target bot will receive the message and it will only be shown in their own histories).
~~- add "in talk range", "in ability range" in send_to_bot. Since the latest updates with independent distances (sight/movement) this has broken the talk range. Bot needs to know who is in range of ability and who can hear. Also needs to be checked for cheating too... (make sure it's a valid move before changing anything).~~
- 3D Map viewer.
~~- Local LLM - (just need to test how well they can handle outputting the json)~~
~~- destinations for path finding.~~
- Allow human to be one of the turns.
- Preset situations / Sets (modern day town, a bar, bridge of a star ship).
- dynamically create maps, dungeons.
- AI Dungeon Master (for any time period).
- Move Long distances - sets a path and misses turns (to save costs) but actually takes that path (updates position every round of turns but doens't trigger the llm) and only if interupted will the llm be triggered (maybe if crosses path with another bot, or player)
- End Goal - Unreal 5 AI driven World that you can enter for fun.. Westworld.
- Todo = Checkout if anyone else is doing something similar - though this is mostly for fun and a learning experience.