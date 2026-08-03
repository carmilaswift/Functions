"""
Dating Proposal App
--------------------
A playful little Tkinter app that pops the question.
The "No" button runs away whenever you try to click it,
so "Yes" is the only button you can actually press!

Run with: python dating_proposal.py
"""

import tkinter as tk
import random

# ---- Customize these! ----
YOUR_NAME = "You"
THEIR_NAME = "Someone Special"
QUESTION = f"Will you go on a date with {YOUR_NAME}?"
YES_MESSAGE = "Yay! 🎉 I knew you'd say yes! Can't wait to see you 💕"
# ---------------------------


class ProposalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A Question For You...")
        self.root.geometry("500x350")
        self.root.configure(bg="#ffe6f0")
        self.root.resizable(False, False)

        self.yes_size = 1.0  # grows every time "No" is dodged

        self.heart_label = tk.Label(
            root, text="💖", font=("Arial", 40), bg="#ffe6f0"
        )
        self.heart_label.pack(pady=(20, 0))

        self.question_label = tk.Label(
            root,
            text=QUESTION,
            font=("Helvetica", 18, "bold"),
            bg="#ffe6f0",
            fg="#d6336c",
            wraplength=420,
            justify="center",
        )
        self.question_label.pack(pady=20)

        self.button_frame = tk.Frame(root, bg="#ffe6f0", height=150)
        self.button_frame.pack(fill="both", expand=True)
        self.button_frame.pack_propagate(False)

        self.yes_button = tk.Button(
            self.button_frame,
            text="Yes! 💘",
            font=("Helvetica", 14, "bold"),
            bg="#ff8fab",
            fg="white",
            activebackground="#ff6f91",
            relief="raised",
            command=self.say_yes,
        )
        self.yes_button.place(x=180, y=60, width=100, height=45)

        self.no_button = tk.Button(
            self.button_frame,
            text="No",
            font=("Helvetica", 12),
            bg="#cfcfcf",
            command=self.say_no,
        )
        self.no_button.place(x=300, y=60, width=80, height=40)
        # Dodge whenever the mouse gets near
        self.no_button.bind("<Enter>", self.dodge)

    def dodge(self, event=None):
        """Move the No button to a random spot and shrink it a little."""
        frame_w = self.button_frame.winfo_width() or 480
        frame_h = self.button_frame.winfo_height() or 150

        w = max(40, 80 - int(self.yes_size * 4))
        h = max(25, 40 - int(self.yes_size * 2))

        max_x = max(10, frame_w - w - 10)
        max_y = max(10, frame_h - h - 10)

        new_x = random.randint(10, max_x)
        new_y = random.randint(10, max_y)

        self.no_button.place(x=new_x, y=new_y, width=w, height=h)

        # Grow the Yes button a bit each time, for fun
        self.yes_size += 1
        new_font_size = min(28, 14 + int(self.yes_size))
        self.yes_button.config(font=("Helvetica", new_font_size, "bold"))
        new_w = min(300, 100 + int(self.yes_size * 8))
        new_h = min(100, 45 + int(self.yes_size * 3))
        self.yes_button.place(x=180, y=60, width=new_w, height=new_h)

    def say_no(self):
        # Should basically be unreachable, but just in case!
        self.dodge()

    def say_yes(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.question_label.config(text=YES_MESSAGE)
        self.heart_label.config(text="🎉💕🎉")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProposalApp(root)
    root.mainloop()gi