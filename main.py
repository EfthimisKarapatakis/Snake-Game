import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 500
SPEED = 75
SPACE_SIZE = 25
BODY_PARTS = 3  # When the game starts.
SNAKE_COLOR = "#00ff00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_turn(snake, food):
    global direction_lock

    if paused:  # Check if the game is paused
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        direction_lock = False  # Reset the direction lock after the snake moves
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction, direction_lock

    # Only allow direction change if no lock is in place
    if not direction_lock:
        if new_direction == "left" and direction != "right":
            direction = new_direction
        elif new_direction == "right" and direction != "left":
            direction = new_direction
        elif new_direction == "up" and direction != "down":
            direction = new_direction
        elif new_direction == "down" and direction != "up":
            direction = new_direction

        # Lock direction change until next turn
        direction_lock = True


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    global game_over_state
    game_over_state = True
    canvas.delete("all")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("consolas", 40), text="GAME OVER",fill="red", tags="game-over-text")


def restart_game(event=None):
    global score, direction, snake, food, game_over_state, paused, direction_lock
    if game_over_state:
        canvas.delete("all")
        game_over_state = False
        paused = False  # Reset paused state
        direction_lock = False  # Reset direction lock
        score = 0
        direction = "down"
        label.config(text=f"Score: {score}")
        snake = Snake()
        food = Food()
        next_turn(snake, food)


def exit_game(event=None):
    window.quit()


def toggle_pause(event=None):
    global paused
    paused = not paused  # Toggle the paused state
    if not paused:  # If unpausing, resume the game
        next_turn(snake, food)


window = tk.Tk()
window.title("Snake Game!")
window.resizable(False, False)

score = 0
direction = "down"
game_over_state = False
paused = False  # Variable to keep track of the paused state
direction_lock = False  # Variable to lock direction changes until next movement

label = tk.Label(window, text=f"Score: {score}", font=("consolas", 40))
label.pack()
label = tk.Label(window, text="esc to exit | p to pause | enter to play again", font=("consolas", 15))
label.pack()
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind keys for movement, restart, exit, and pause
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Return>", restart_game)  # Press "Enter" to restart
window.bind("<Escape>", exit_game)  # Press "Esc" to exit
window.bind("<p>", toggle_pause)  # Press "P" to pause/resume the game

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
