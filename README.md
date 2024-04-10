# AI Bot World

Welcome to the AI Bot World, an immersive and dynamic starting point for building a vast and engaging AI-driven universe! This project harnesses the power of GPT-4 Turbo as the language model to control each bot individually, enabling you to create a world populated by intelligent entities with unique personalities (in a way), abilities, and interactions.

## Features

- **Diverse Entities**: Create a wide array of AI-driven entities, each with its own distinct personality, abilities, and starting position on the grid. Define their characteristics in the `entities` table and watch them come to life!
- **Realistic Interactions**: Witness the bots interact, communicate, and navigate the world, making decisions based on their surroundings and objectives. With a limited perception range of 2 tiles, the bots must strategize and adapt to their environment.
- **Independent Memory**: Each bot possesses its own memory, allowing them to retain knowledge of their past interactions and experiences. This adds depth and continuity to their behavior and decision-making process.
- **Health Points and Abilities**: Bots have health points (HP) and can engage in combat or healing. With a maximum HP of 100, they can deal 10 damage when attacking or restore 10 HP when healing. This creates a dynamic and evolving world where bots must make strategic choices.
- **Structured Environment**: The world is represented by a 10x10 grid, providing a structured and manageable environment for the bots to explore and interact with. Each cell on the grid can accommodate multiple bots, enabling complex interactions and encounters.
- **Langchain Integration**: The project utilizes Langchain (Flowise) to create an API end point for interactions and generating responses. With a simple flow consisting of an LLMChain, ChatOpenAI model (gpt-4-turbo), a generic prompt template, and a structured output parser, you can easily fine-tune the bot's behavior and communication style.

## Getting Started

To embark on your AI Bot World journey, follow these steps:

1. **Database Setup**: Set up the database using the provided schema. The `entities` table allows you to define the characteristics (personality), abilities (heal or attack), and starting positions of your bots and an image url (recommend small square png). Configure the database settings in `config.py` and `botData.php` to establish a connection to your database.
2. **Langchain (Flowise) Setup**: Set up the API endpoint in `config.py` using Langchain (Flowise). Create a simple flow with the LLMChain, ChatOpenAI model (gpt-4-turbo), a generic prompt template, and a structured output parser to enforce the desired JSON response format (the api should return json with: thought, talk, ability, move (A1 to J10 style coordinates). This will enable seamless communication between the bots and the language model.
3. **Bot Customization**: Customize the bot personalities, abilities, and images in the `entities` table to bring your world to life. Assign them unique names, descriptions, and starting positions to create a diverse and engaging ecosystem.
4. **Run the Scripts**: Run the aiworld.py script to initiate the AI Bot World and witness the bots' interactions and evolution. The scripts will handle the bot's movement, communication, and decision-making based on their individual characteristics and the state of the world using the responses from the LLM and by passing it the history and data from the database.
5. **Explore and Expand**: Observe the bots as they navigate the grid, interact with each other, and make decisions based on their goals and constraints. Use the provided web interface to visualize the world and track the bots' progress. Feel free to expand upon the existing features and add new elements to enrich the AI Bot World experience.

## How it works?

**TODO but the basics are:**

In each turn - json is sent to the endpoint like this - for each bot - it uses the same API which has a prompt template with the generic information about the world, and the additional information sent from the script is the more personal information for that bot (from the entities table). Such as, the bots name, it's "personality", which ability it has.
It also receives information about any nearby bots, their health/positions and if they are using an ability and are talking.
It also does the same for each historical time points.

Will improve this readme in the future if this has any interest.