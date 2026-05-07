import tkinter as tk

#Creating the canvas
root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

canvas.create_line(0, 300, 200, 300, width=40, fill="gray")
canvas.create_line(200, 320, 200, 100, width=40, fill="gray")
canvas.create_line(180, 100, 500, 100, width=40, fill="gray")
canvas.create_line(480, 100, 480, 320, width=40, fill="gray")
canvas.create_line(480, 320, , 800, width=40, fill="gray")


root.mainloop()