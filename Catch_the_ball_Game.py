from tkinter import Tk, Button, Label, Canvas
from random import randint

base = Tk()
base.title("BALL GAME")
base.resizable(False, False)
base.configure(bg='#1a1a2e', highlightthickness=6, highlightbackground="#12cad6")

color = Canvas(base, width=600, height=650, bg='#16213e', highlightthickness=6, highlightbackground="#12cad6")
color.pack(pady=10)

points_label = Label(base, text="Points: 0", font=("Helvetica", 14, "bold"), bg="#1a1a2e", fg="#f8f8f8")
points_label.pack()

highest_score_label = Label(base, text="Highest Score: 0", font=("Helvetica", 12, "bold"), bg="#1a1a2e", fg="yellow")
highest_score_label.pack()

standard = 0
length = 5
marks = 0
highest_score = 0
speed_factor = 10
current_slide = None

class Model:
    def __init__(self, color, m1, n1, m2, n2):
        # Stylish cricket-style ball (red with white seam)
        self.color = color
        self.circle_main = color.create_oval(m1, n1, m2, n2, fill="red", outline="white", width=2, tags='dot1')
        self.seam = color.create_line(m1 + 15, n1, m1 + 15, n2, fill="white", width=2, tags='dot1')

    def game(self):
        global marks, speed_factor
        pos = self.color.coords(self.circle_main)
        if pos and pos[3] >= 570:
            if (length <= pos[0]) and (length + 60 >= pos[2]):
                marks += 5
                points_label.config(text=f"Points: {marks}")
                speed_factor = max(2, speed_factor - 1)
                color.delete('dot1')
                game_play()
            else:
                color.delete('dot1')
                remove_slide()
                result()
            return

        self.color.move(self.circle_main, 0, 4)
        self.color.move(self.seam, 0, 4)
        self.color.after(speed_factor, self.game)


class Slide:
    def __init__(self, color, m1, n1, m2, n2):
        # Cricket-style bat (wooden color with grip highlight)
        self.color = color
        self.shadow = color.create_rectangle(m1 + 2, n1 + 3, m2 + 2, n2 + 3, fill="#4d2600", outline="", tags='dot2')
        self.num = color.create_rectangle(m1, n1, m2, n2, fill="#cc9966", outline="black", width=2, tags='dot2')

    def push(self, direction):
        global length
        if direction == 1 and length <= 540:
            self.color.move(self.num, 20, 0)
            self.color.move(self.shadow, 20, 0)
            length += 20
        elif direction == 0 and length >= 20:
            self.color.move(self.num, -20, 0)
            self.color.move(self.shadow, -20, 0)
            length -= 20

    def remove(self):
        color.delete('dot2')


def game_play():
    size = randint(20, 570)
    game1 = Model(color, size, 20, size + 30, 50)
    game1.game()


def remove_slide():
    color.delete('dot2')


def result():
    global marks, highest_score
    if marks > highest_score:
        highest_score = marks
        highest_score_label.config(text=f"Highest Score: {highest_score}")

    color.configure(highlightbackground="#ff4c4c")
    base2 = Tk()
    base2.title("Game Over")
    base2.resizable(False, False)
    base2.configure(bg='#ff6b6b', highlightthickness=4, highlightbackground="#ff0000")

    canvas_result = Canvas(base2, width=320, height=270, bg='#ff6b6b', highlightthickness=0)
    canvas_result.pack(pady=10)

    Label(canvas_result, text=f"GAME OVER!", font=("Helvetica", 22, "bold"), bg='#ff6b6b', fg='white').pack(pady=12)
    Label(canvas_result, text=f"Your Score: {marks}", font=("Helvetica", 16, "bold"), bg='#ff6b6b', fg='white').pack(pady=8)

    play_again = Button(canvas_result, text="▶ Play Again", font=("Helvetica", 14, "bold"), bg="#12cad6", fg="white", relief="groove", borderwidth=4, command=lambda: repeat(base2))
    play_again.pack(pady=10)
    play_again.bind("<Enter>", lambda e: play_again.config(bg="#00ffcc"))
    play_again.bind("<Leave>", lambda e: play_again.config(bg="#12cad6"))

    exit_btn = Button(canvas_result, text="❌ Exit", font=("Helvetica", 14, "bold"), bg="#ff0000", fg="white", relief="groove", borderwidth=4, command=lambda: close_game(base2))
    exit_btn.pack(pady=5)
    exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#ff5555"))
    exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#ff0000"))


def repeat(base2):
    base2.destroy()
    color.configure(highlightbackground="#12cad6")
    restart_game()


def close_game(base2):
    base2.destroy()
    base.destroy()


def restart_game():
    global marks, length, speed_factor, current_slide
    marks = 0
    length = 5
    speed_factor = 10
    color.delete('dot2')

    current_slide = Slide(color, 5, 570, 65, 585)

    base.bind('<Right>', lambda e: current_slide.push(1))
    base.bind('<Left>', lambda e: current_slide.push(0))

    game_play()


if __name__ == "__main__":
    restart_game()
    base.mainloop()