import socket
import random
import threading
from datetime import datetime, timedelta

irregular_verbs = {
    # "-orn" x4
    "bear": ("bore", "born"),
    "swear": ("swore", "sworn"),
    "tear": ("tore", "torn"),
    "wear": ("wore", "worn"),
    # "-ought" x7
    "bring": ("brought", "brought"),
    "buy": ("bought", "bought"),
    "catch": ("caught", "caught"),
    "fight": ("fought", "fought"),
    "seek": ("sought", "sought"),
    "teach": ("taught", "taught"),
    "think": ("thought", "thought"),
    # "-ound" x4
    "bind": ("bound", "bound"),
    "find": ("found", "found"),
    "grind": ("ground", "ground"),
    "wind": ("wound", "wound"),
    # "-own" x6
    "blow": ("blew", "blown"),
    "draw": ("drew", "drawn"),
    "fly": ("flew", "flown"),
    "grow": ("grew", "grown"),
    "know": ("knew", "known"),
    "throw": ("threw", "thrown")
}

HOST = "127.0.0.1"
PORT = 9999

def handle_client(conn, addr):
    conn.sendall(b"welcome to the irregular verbs CTF chall\n")
    conn.sendall(b"type the past simple and past participle of the given verb\n")
    conn.sendall(b"example: go -> went gone\n\n")
    begintime = datetime.now()
    score = 0
    for _ in range(21):
        verb = random.choice(list(irregular_verbs.keys()))
        correct = irregular_verbs[verb]
        conn.sendall(f"what are the past forms of '{verb}'? ".encode())
        try:
            response = conn.recv(1024).decode().strip().lower()
            parts = response.split()

            if len(parts) != 2:
                conn.sendall(b"please answer with two words (e.g., went gone)\n")
                continue

            if (parts[0] == correct[0].lower()) and (parts[1] == correct[1].lower()):
                conn.sendall(b"correct!\n")
                score += 1
            else:
                conn.sendall(f"incorrect! correct answer: {correct[0]} {correct[1]}\n".encode())
        except:
            break
    conn.sendall(f"\nyour final score: {score}/21\n".encode())
    conn.sendall(b"thanks for playing\n")
    now = datetime.now()
    if now - begintime < timedelta(seconds=1) and score == 21:
        conn.sendall(b"and here is your flag: flag{damn_it_was_fast&right!!!}\n")
    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
