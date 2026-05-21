import tkinter as tk
import math
#Money = 0

# Making the window
root = tk.Tk()
root.title("Tower Defense")

WIDTH = 800
HEIGHT = 600

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="green")
canvas.pack()

# Making player health
player_health = 10

health_text = canvas.create_text(
    70,
    30,
    # f means I don't have to put the + str()
    text=f"Health: {player_health}",
    fill="white",
    font=("Arial", 18)

)
#money_text = canvas.create_text()

# Making path
canvas.create_line(0, 300, 1000, 300, width=40, fill="gray")



# Lists
enemies = []
towers = []
projectiles = []

# Making enemy traits
class Enemy:

    def __init__(self, canvas):

        self.canvas = canvas

        self.x = 0
        self.y = 300

        self.speed = 2

        self.health = 3

        self.shape = canvas.create_oval(
            self.x,
            self.y,
            self.x + 20,
            self.y + 20,
            fill="red"
        )

        self.health_text = canvas.create_text(
            self.x + 10,
            self.y - 10,
            text=str(self.health),
            fill="white"
        )

    def move(self):

        global player_health

        self.x += self.speed

        self.canvas.coords(
            self.shape,
            self.x,
            self.y,
            self.x + 20,
            self.y + 20
        )

        self.canvas.coords(
            self.health_text,
            self.x + 10,
            self.y - 10
        )

        # Enemy reaches end
        if self.x > WIDTH:

            player_health -= 1

            canvas.itemconfig(
                health_text,
                text=f"Health: {player_health}"
            )

            self.destroy()

    def take_damage(self, amount):

        self.health -= amount

        self.canvas.itemconfig(
            self.health_text,
            text=str(self.health)
        )

        if self.health <= 0:
            self.destroy()

    def destroy(self):

        if self in enemies:
            enemies.remove(self)

        self.canvas.delete(self.shape)
        self.canvas.delete(self.health_text)

# Making projectile traits
class Projectile:

    def __init__(self, canvas, x, y, target):

        self.canvas = canvas

        self.x = x
        self.y = y

        self.speed = 6

        self.target = target

        self.shape = canvas.create_oval(
            self.x - 5,
            self.y - 5,
            self.x + 5,
            self.y + 5,
            fill="yellow"
        )

    def move(self):

        # Target destroyed already
        if self.target not in enemies:
            self.destroy()
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return

        # Move toward enemy
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed

        self.canvas.coords(
            self.shape,
            self.x - 5,
            self.y - 5,
            self.x + 5,
            self.y + 5
        )

        # Hit enemy
        if distance < 10:

            self.target.take_damage(1)
            self.destroy()

    def destroy(self):

        if self in projectiles:
            projectiles.remove(self)

        self.canvas.delete(self.shape)

# Making tower traits
class Tower:

    def __init__(self, canvas, x, y):

        self.canvas = canvas

        self.x = x
        self.y = y

        self.range = 150

        self.cooldown = 0

        self.shape = canvas.create_rectangle(
            x - 20,
            y - 20,
            x + 20,
            y + 20,
            fill="blue"
        )

    def find_target(self):

        for enemy in enemies:

            distance = math.sqrt(
                (enemy.x - self.x) ** 2 +
                (enemy.y - self.y) ** 2
            )

            if distance <= self.range:
                return enemy

        return None

    def update(self):

        if self.cooldown > 0:
            self.cooldown -= 1

        target = self.find_target()

        if target and self.cooldown == 0:

            projectile = Projectile(
                self.canvas,
                self.x,
                self.y,
                target
            )

            projectiles.append(projectile)


            self.cooldown = 40

class Tower2:

    def __init__(self, canvas, x, y):

        self.canvas = canvas

        self.x = x
        self.y = y

        self.range = 100

        self.cooldown = 3

        self.shape = canvas.create_rectangle(
            x - 20,
            y - 20,
            x + 20,
            y + 20,
            fill="cyan"
        )

    def find_target(self):

        for enemy in enemies:

            distance = math.sqrt(
                (enemy.x - self.x) ** 2 +
                (enemy.y - self.y) ** 2
            )

            if distance <= self.range:
                return enemy

        return None

    def update(self):

        if self.cooldown > 0:
            self.cooldown -= 1

        target = self.find_target()

        if target and self.cooldown == 0:

            projectile = Projectile(
                self.canvas,
                self.x,
                self.y,
                target
            )

            projectiles.append(projectile)

            # Faster shooting
            self.cooldown = 15


# Using mouse clicks to place towers
def place_tower(event):

    tower = Tower(canvas, event.x, event.y)

    towers.append(tower)
canvas.bind("<Button-1>", place_tower)

def place_tower2(event):

    tower2 = Tower2(canvas, event.x, event.y)
    
    towers.append(tower2)
canvas.bind("<Button-3>", place_tower2)

# Spawning enemies/waves
wave = 1

def spawn_enemy():

    enemy = Enemy(canvas)

    enemies.append(enemy)

def start_wave():

    for i in range(wave * 50):

        root.after(i * 150, spawn_enemy)

# Making game loop
def game_loop():

    # Move enemies
    for enemy in enemies[:]:
        enemy.move()

    # Update towers
    for tower in towers:
        tower.update()

    # Move projectiles
    for projectile in projectiles[:]:
        projectile.move()

    # Game Over
    if player_health <= 0:

        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="GAME OVER",
            fill="red",
            font=("Arial", 40)
        )

        return

    root.after(16, game_loop)

# functions for starting the game
start_wave()
game_loop()

root.mainloop()