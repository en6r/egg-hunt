import os
import time
import random
import pygame

from PIL import Image, ImageTk
import tkinter as tk

class directory_node_t:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.egg = None  # "good", "bad", or None
        self.parent = None


# # Optional: pip install colorama for colorful text
# try:
#     from colorama import Fore, Style, init
#     init(autoreset=True)
# except ImportError:
#     class FakeColor:
#         def __getattr__(self, name):
#             return ''
#     Fore = Style = FakeColor()

ascii_bunny = r"""
 (\__/)
 (•ㅅ•) 
 / 　 づ🥚
"""

def open_image(image_path, duration=5000):
    try:
        root = tk.Tk()
        # root.geometry("+500+300")  # optional: center it

        # load image
        img = Image.open(image_path)
        tk_img = ImageTk.PhotoImage(img)

        # display image in a label
        label = tk.Label(root, image=tk_img)
        label.pack()

        # automatically close window after duration
        root.after(duration, root.destroy)
        root.mainloop()

    except Exception as e:
        print(f"failed to open image in popup: {e}")

def slow_print(text, delay=0.03):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

# recursively builds maze as a tree
def generate_maze(curr_node, depth, max_depth, max_branch):
    if depth >= max_depth:
        return
    num_children = random.randint(1, max_branch)
    for i in range(num_children):
        child_name = f"{curr_node.name}_sub{i}"
        child_node = directory_node_t(child_name)
        child_node.parent = curr_node
        curr_node.children.append(child_node)
        generate_maze(child_node, depth + 1, max_depth, max_branch)

def reveal_good_egg(num_variants):
    print("🎉 You found a GOOD egg!\n")
    print(ascii_bunny)

    index = random.randint(1, num_variants)
    image_path = f"assets/loving_bunny_{index}.png"
    open_image(image_path)

    pygame.mixer.init()
    pygame.mixer.music.load("assets/spring-easter-day-music-30-seconds-version-320430.mp3")
    pygame.mixer.music.play()

def reveal_bad_egg(num_variants):
    print("😱 BAD EGG!!\n\a")

    index = random.randint(1, num_variants)
    image_path = f"assets/murderous_bunny_{index}.png"
    sound_path = f"assets/jumpscare{index}.mp3"

    open_image(image_path)

    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

def place_eggs(root, num_good, num_bad):
    all_leaves = []

    # depth first search to get leaf nodes
    def find_leaves(node):
        if not node.children:
            all_leaves.append(node)
        for child in node.children:
            find_leaves(child)

    find_leaves(root)
    leaves = random.sample(all_leaves, num_good + num_bad)
    for i, leaf in enumerate(leaves):
        leaf.egg = "good" if i < num_good else "bad"

def in_session(num_loving_bunnyies, num_murderous_bunnies):

    if num_loving_bunnyies == 0:
        print("\n🥚🥚 CONGRATULATIONS! 🥚🥚\nYou found all the Easter eggs" + ascii_bunny)        print(Fore.MAGENTA + )
        return False

    if num_murderous_bunnies == 0:
        print("\n💀 GAME OVER 💀\nYou've been eaten by murderous bunnies.")
        return False

    return True

def search(start_node, num_loving_bunnyies, num_murderous_bunnies):
    current = start_node

    while in_session(num_loving_bunnyies, num_murderous_bunnies):
        print(f"\nYou are in: {current.name}")
        if current.egg == "good":
            reveal_good_egg(num_loving_bunnyies)
            current.egg == None
            num_loving_bunnyies -= 1
            return
        elif current.egg == "bad":
            reveal_bad_egg(num_murderous_bunnies)
            current.egg == None
            num_murderous_bunnies -= 1
            return
        else: 
            print("no egg here... just some lint.")

        for i, child in enumerate(current.children):
            print(f"{i + 1}. {child.name}")
        if current.parent:
            print("0. .. (go back)")

        choice = input("choose a directory: ")

        print(f"\nchecking path {choice}...")
        time.sleep(1)

        if choice == "0" and current.parent:
            current = current.parent
        elif choice.isdigit() and 1 <= int(choice) <= len(current.children):
            current = current.children[int(choice) - 1]
        else:
            print("❌ Invalid choice.")

def main():

    num_loving_bunnyies = 2 
    num_murderous_bunnies  = 3
    slow_print("🐰 Welcome to the Terminal Easter Egg Hunt! 🥚", 0.04)
    slow_print("Find all hidden Easter eggs in the maze.\nBe warned, there may be some bad eggs along the way", 0.04)
    
    root = directory_node_t("root")
    generate_maze(root, depth=0, max_depth=3, max_branch=3)
    place_eggs(root, num_loving_bunnyies, num_murderous_bunnies)
    search(root, num_loving_bunnyies, num_murderous_bunnies)

    slow_print(ascii_bunny + "/tThanks for playing/t" + ascii_bunny)

if __name__ == "__main__":
    main()
