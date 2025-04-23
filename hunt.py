import os
import time
import random
import contextlib
import io

from PIL import Image, ImageTk
import tkinter as tk

from colorama import Fore, Style, init

with contextlib.redirect_stdout(io.StringIO()):
    import pygame

class maze_node_t:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.egg = None  # "good", "bad", or None
        self.parent = None
        self.visited = False

ascii_bunny = r"""
 (\__/)
 (•ㅅ•) 
 / 　 づ🩚
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def open_image(image_path, duration=2000):
    try:
        root = tk.Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # calculate position to center the window
        x = (screen_width - 1920) // 2
        y = (screen_height - 1080) // 2

        root.geometry(f"{1920}x{1080}+{x}+{y}")

        # load image
        img = Image.open(image_path)
        img.thumbnail((1920 , 1080), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(img)

        # display image in a label
        label = tk.Label(root, image=tk_img)
        label.pack()

        # automatically close window after duration
        root.after(duration, root.destroy)
        root.mainloop()

    except Exception as e:
        print(f"failed to open image in popup: {e}")

def slow_print(text, delay=0.03, color=Fore.WHITE):
    for c in text:
        print(color + c, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def generate_maze(curr_node, depth, max_depth, max_branch):
    if depth >= max_depth:
        return
    num_children = random.randint(1, max_branch)
    for i in range(num_children):
        child_name = f"room_{random.randint(100, 999)}"
        child_node = maze_node_t(child_name)
        child_node.parent = curr_node
        curr_node.children.append(child_node)
        generate_maze(child_node, depth + 1, max_depth, max_branch)

def reveal_good_egg():
    print(Fore.GREEN + "\n🎉 You found a GOOD egg!\n")
    print(Fore.MAGENTA + ascii_bunny)

    pygame.mixer.init()
    pygame.mixer.music.load("assets/spring-easter-day-music-30-seconds-version-320430.mp3")
    pygame.mixer.music.play()

    open_image("assets/nice_bunny.png", 3500)
    pygame.mixer.music.stop()

def reveal_bad_egg():
    print(Fore.RED + "\n😱 BAD EGG!! 😱\n\a")

    pygame.mixer.init()
    pygame.mixer.music.load("assets/jumpscare.mp3")
    pygame.mixer.music.play()

    open_image("assets/murderous_bunny.png", duration=2500)

def place_eggs(root, num_good, num_bad):
    all_leaves = []

    def find_leaves(node):
        if not node.children:
            all_leaves.append(node)
        for child in node.children:
            find_leaves(child)

    find_leaves(root)
    leaves = random.sample(all_leaves, num_good + num_bad)
    for i, leaf in enumerate(leaves):
        leaf.egg = "good" if i < num_good else "bad"

def in_session(num_nice_bunnies, num_murderous_bunnies):
    if num_nice_bunnies == 0:
        print(Fore.GREEN + "\n🎊 CONGRATULATIONS! 🎊")
        slow_print("You found all the Easter eggs!", 0.03, Fore.GREEN)
        print(ascii_bunny)
        return False

    if num_murderous_bunnies == 0:
        print(Fore.RED + "\n💀 GAME OVER 💀")
        slow_print("You've been eaten by murderous bunnies.", 0.03, Fore.RED)
        return False

    return True

def search(start_node, num_nice_bunnies, num_murderous_bunnies):
    current = start_node
    while in_session(num_nice_bunnies, num_murderous_bunnies):

        current.visited = True

        clear_screen()
        draw_minimap(current, num_nice_bunnies)
        print(Fore.GREEN + f"\n📍 You are in: {current.name}")
        print(Fore.YELLOW + f"🥚 Good eggs remaining: {num_nice_bunnies}")

        if current.egg == "good":
            reveal_good_egg()
            num_nice_bunnies -= 1
        elif current.egg == "bad":
            reveal_bad_egg()
            num_murderous_bunnies -= 1
        else:
            print(Fore.BLUE + "🧹 No egg here... just some lint.")

        print(Fore.CYAN + "\n🚪 Choose a path:")

        for i, child in enumerate(current.children):
            print(Fore.CYAN + f"{i + 1}. Path to {child.name}")
        if current.parent:
            print(Fore.CYAN + "0. .. (go back)")

        choice = input(Fore.YELLOW + "\n➡️  Your choice: ")

        print(Fore.LIGHTBLACK_EX + f"🔎 Checking path '{choice}'...")
        time.sleep(1)

        if choice == "0" and current.parent:
            current = current.parent
        elif choice.isdigit() and 1 <= int(choice) <= len(current.children):
            current = current.children[int(choice) - 1]
        else:
            print(Fore.RED + "❌ Invalid choice.")

def welcome_message():
    print(Fore.YELLOW + "=" * 50)
    slow_print("🐰 WELCOME TO THE TERMINAL EASTER EGG HUNT 🐰", 0.04, Fore.MAGENTA)
    print(Fore.YELLOW + "=" * 50)
    slow_print("Find all hidden Easter eggs in the maze.", 0.04, Fore.CYAN)
    slow_print("But beware... some bunnies are not so nice 🐇🔪", 0.04, Fore.RED)
    print(Fore.YELLOW + "=" * 50)

def goodbye_message():
    print(Fore.YELLOW + "\n" + "=" * 50)
    slow_print("🎮 Thanks for playing!", 0.04, Fore.CYAN)
    print(ascii_bunny)
    print(Fore.YELLOW + "=" * 50)

def get_maze_root(node):
    while node.parent is not None:
        node = node.parent
    return node

def draw_minimap(current_node, num_nice_bunnies):
    def recurse(node, prefix=""):
        icon = "⬛"
        if node == current_node:
            icon = "🧍"  # Current location
        elif node.visited:
            icon = "🟩"
            if node.egg == "good":
                icon += "🥚"
            elif node.egg == "bad":
                icon += "💀"

        line = f"{prefix}{icon} {node.name}"
        lines.append(line)

        for i, child in enumerate(node.children):
            branch_prefix = prefix + ("│   " if i < len(node.children) - 1 else "    ")
            recurse(child, branch_prefix)

    lines = []
    recurse(get_maze_root(current_node))
    print(Fore.LIGHTBLACK_EX + "\n".join(lines))

def main():
    init(autoreset=True) # colorama

    num_nice_bunnies = 2 
    num_murderous_bunnies  = 2

    welcome_message()

    root = maze_node_t("root")
    generate_maze(root, depth=0, max_depth=3, max_branch=3)
    place_eggs(root, num_nice_bunnies, num_murderous_bunnies)
    search(root, num_nice_bunnies, num_murderous_bunnies)

    goodbye_message()

if __name__ == "__main__":
    main()
