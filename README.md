# AI Bot World

Welcome to the AI Bot World, an immersive and dynamic starting point for building a vast and engaging AI-driven universe! This project harnesses the power of GPT-4 Turbo as the language model to control each bot individually, enabling you to create a world populated by intelligent entities with unique personalities (in a way), abilities, and interactions.

Now completely standalone using sqlite - only need OpenAI key - todo - allow other llm.

(this readme was mostly generated by AI, on the TODO to do properly..)

## Features

- **Diverse Entities**: Create a wide array of AI-driven entities, each with its own distinct personality (in a way), abilities, and starting position on the grid. Define their characteristics in the config page and watch them come to life!
- **Realistic Interactions**: Witness the bots interact, communicate, and navigate the world, making decisions based on their surroundings and objectives. With a limited perception range of 2 tiles, the bots must strategize and adapt to their environment.
- **Independent Memory**: Each bot possesses its own memory, allowing them to retain knowledge of their past interactions and experiences. This adds depth and continuity to their behavior and decision-making process.
- **Health Points and Abilities**: Bots have health points (HP) and can engage in combat or healing. With a maximum HP of 100, they can deal 10 damage when attacking or restore 10 HP when healing. This creates a dynamic and evolving world where bots must make strategic choices. Boss Bots (boss=1 in the entities table) do 10 to 60 damage or healing (random) depending on their ability.
- **Structured Environment**: The world is represented by a 10x10 grid, providing a structured and manageable environment for the bots to explore and interact with. Each cell on the grid can accommodate multiple bots, enabling complex interactions and encounters.
- **Langchain Integration**: The project utilizes OpenAI's API for interactions and generating responses. You can easily fine-tune the bot's behavior and communication style.

### AI World Demo Video
Click on the image below to watch the demo video:

[![Watch the video](https://downloads.xaya.io/screenshot.jpg)](https://downloads.xaya.io/AI-world-v1.mp4)

## Getting Started

To embark on your AI Bot World journey, follow these steps:

1. **Bot Customization**: Customize the bot personalities, abilities, and images on the config page. You can add as many as you want (to pay for).
2. **OpenAI Key**: Add your openAI key to the openai_module.py
4. **Run the Scripts**: Run the app.py script to initiate the AI Bot World and witness the bots' interactions and evolution. The scripts will handle the bot's movement, communication, and decision-making based on their individual characteristics and the state of the world using the responses from the LLM and by passing it the history and data from the database. To view the world real time you can connect to http://127.0.0.1:5000 (built in flask app included).
5. **Explore and Expand**: Observe the bots as they navigate the grid, interact with each other, and make decisions based on their goals and constraints. Use the provided web interface to visualize the world and track the bots' progress. Feel free to expand upon the existing features and add new elements to enrich the AI Bot World experience.

## How it works?

**TODO**

- To do the TODO.

