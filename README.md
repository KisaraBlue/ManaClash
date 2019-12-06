# Mana Clash
Project for the Software Engineering course offered at ENS Paris-Saclay in the first semester of M1 in 2019.


Requirements:
-   Python 3.7+ (should work on 3.5+; but we only tested on 3.7)
-   Check /code/requirements.txt for all required libraries.

How to run the game:
- Admin panel can be accessed by running the run.py file and then going to 127.0.0.1:5000/admin in your browser. You can use this to add or remove anything in the database (say you want to add cards).
- Interface: we could not manage to finish the UI in time. As such, the controller.py file will run a CLI version of the game.
- An html demo of the UI is there to show the final display of one game session

Note on Continuous Integration:
- We did not manage to write any meaningful tests properly (save for the usual printing while testing), and because we ran out of time, we did not set up proper tests or CI.

Rules of the game:
- A player can participate in one game only (by virtue of the CLI for the controller; both the model and controller support multiple games per user).
- There are Monster cards, and Monster Effect cards (the controller does not handle Equipment yet).
- Effects last for the entirety of a game.
