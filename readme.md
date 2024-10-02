# AI Image Guessing Game

This is a web-based game where users try to guess the prompt used to generate an AI image.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/jwalahe/ImageGuess.git
   cd ImageGuess
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. Run the application:
   ```
   python app.py
   ```

6. Open a web browser and navigate to `http://localhost:5000` to play the game.

## Deploying to GitHub Codespaces

1. Create a new GitHub repository and push your code to it.

2. Open the repository in GitHub Codespaces.

3. In the Codespace terminal, install the requirements:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key as a secret in the Codespace:
   - Go to the repository settings
   - Navigate to Secrets > Codespaces
   - Add a new secret named `OPENAI_API_KEY` with your API key as the value

5. Run the application:
   ```
   python app.py
   ```

6. When the Codespace prompts you to open the port, click "Open in Browser" to play the game.

## How to Play

1. An AI-generated image will be displayed.
2. Try to guess the prompt used to generate the image.
3. Enter your guess and submit.
4. You'll receive feedback on how close your guess was to the original prompt.
5. Score points for correct or close guesses!

Enjoy playing the AI Image Guessing Game!
