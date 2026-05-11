import tkinter as tk

#Creating the canvas
root = tk.Tk()
root.title("Tower Defence")

canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

def game_loop():
    update()
    draw()

    root.after(16, game_loop)

canvas.create_line(0, 300, 200, 300, width=40, fill="gray")
canvas.create_line(200, 320, 200, 100, width=40, fill="gray")
canvas.create_line(180, 100, 500, 100, width=40, fill="gray")
canvas.create_line(480, 100, 480, 320, width=40, fill="gray")
canvas.create_line(460, 300, 99999999, 800, width=40, fill="gray")

#Creating Enemies - _Init_ = Initializes/sets up the object 
#Self refers to each enemy
class Enemy:
    def _init_(self, canvas):
        self.canvas = canvas
        self.x = 0
        self.y = 300
        self.speed = 2

        self.shape = canvas.create_oval(
            self.x, self.y, self.x + 20, self.y + 20, fill = "red"
        )

    def move(self):
        self.x += self.speed

        self.canvas.coords(
            self.shape, self.x, self.y, self.x + 20, self.y + 20
        )
    
enemies = []

def spawn_enemies():
    enemies.append(Enemy(canvas))

for enemy in enemies:
    enemy.move()

#Creating Towers
#Self refers to each tower
class Tower:
    def _init_(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.range = 120

        self.shape = canvas.create_rectangle(
            x-20, y-20, x+20, y+20, fill="blue"
        )

    def find_target(self, enemies):
        for enemy in enemies:
            distance = ((enemy.x - self.x)**2 +(enemy.y - self.y)**2) ** 0.5

            if distance <= self.range:
                return enemy
            
        return None
            


root.mainloop()