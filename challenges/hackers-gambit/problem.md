# Hacker's Gambit

- Namespace: 18739
- ID: hackersgambit
- Type: custom
- Category: crypto
- Points: 100

## Description
In order to prevent you from winning the game, your opponent has encrypted your chessboard when you were one move away from winning. Luckily, you managed to swipe a file from him that shows what the current board looks like. You're white (represented by upper case letters) and it's your move. Can you find a way to edit the encrypted board and claim your victory?

## Details
Connect to the challenge with:

```bash
nc {{server("nc")}} {{port("nc")}}

You can download the ciphertext {{url_for("ciphertext.bin", "here")}}.
{{url_for("starting-board.txt", "Here")}} is the file for the current board.

## Hints

- Here's a [chess guide](https://www.dummies.com/article/home-auto-hobbies/games/board-games/chess/knowing-the-moves-that-chess-pieces-can-make-186936/") if you don't know how to play.
- Have you heard of CBC bit flipping?

## Tags
- crypto
- bitflip

## Attributes

- author: Mandy Hu
- event: 18739-ctf


