import json

from flask import Flask
import pyautogui
import time
from pynput import keyboard

app = Flask(__name__)

with open('actions.json', 'r') as file:
    actions = json.load(file)


def perform_action(action_name):
    if action_name in actions:
        for action in actions[action_name]:
            action_type = action["type"]
            if action_type == "keypress":
                key = action["key"]
                hold_duration = action["hold_duration"]
                pyautogui.keyDown(key)
                time.sleep(hold_duration)
                pyautogui.keyUp(key)
                time.sleep(action["delay_after"])
            elif action_type == "mouse_click":
                # Check if a position is provided
                position = action.get("position")
                button = action["button"]
                clicks = action.get("clicks", 1)
                if position:
                    pyautogui.click(x=position[0], y=position[1], button=button, clicks=clicks)
                else:
                    pyautogui.click(button=button, clicks=clicks)
                time.sleep(action["delay_after"])
            # Add other action types like mouse_move, mouse_drag, etc. if necessary
    else:
        print(f"Action '{action_name}' not found.")


@app.route('/<action_name>')
def trigger_action(action_name):
    if action_name in actions:
        perform_action(action_name)
        return f"Performed action: {action_name}", 200
    else:
        return f"Action '{action_name}' not found.", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
