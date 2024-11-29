import random
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_board(board, hide_ships=True):
    print("   A B C D E F G")
    for i, row in enumerate(board):
        row_display = f"{i+1}  " + " ".join(
            ' ' if hide_ships and cell == 'S' else cell for cell in row
        )
        print(row_display)
    print()


def generate_field():
    field = [[' ' for _ in range(7)] for _ in range(7)]
    ships = [(3, 1), (2, 2), (1, 4)]  # (ship_size, count)

    for size, count in ships:
        for _ in range(count):
            while True:
                orientation = random.choice(['H', 'V'])
                row, col = random.randint(0, 6), random.randint(0, 6)
                if can_place_ship(field, row, col, size, orientation):
                    place_ship(field, row, col, size, orientation)
                    break
    return field


def can_place_ship(field, row, col, size, orientation):
    for i in range(size):
        r = row + i if orientation == 'V' else row
        c = col + i if orientation == 'H' else col
        if not (0 <= r < 7 and 0 <= c < 7) or field[r][c] != ' ':
            return False

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 7 and 0 <= nc < 7 and field[nr][nc] == 'S':
                    return False
    return True


def place_ship(field, row, col, size, orientation):
    for i in range(size):
        r = row + i if orientation == 'V' else row
        c = col + i if orientation == 'H' else col
        field[r][c] = 'S'


def convert_coordinates(coord):
    letter, number = coord[0].upper(), int(coord[1]) - 1
    row = number
    col = ord(letter) - ord('A')
    return row, col


def all_ships_sunk(field):
    return all(cell != 'S' for row in field for cell in row)


def battleship_game():
    scores = []
    while True:
        clear_screen()
        player_name = input("Enter your name: ")


        field = generate_field()
        player_field = [[' ' for _ in range(7)] for _ in range(7)]
        attempts = 0

        while True:
            clear_screen()
            print(f"{player_name}'s Battlefield:")
            display_board(player_field)


            while True:
                shot = input("Enter your shot (e.g., B3): ")
                if len(shot) == 2 and shot[0].upper() in "ABCDEFG" and shot[1].isdigit() and 1 <= int(shot[1]) <= 7:
                    row, col = convert_coordinates(shot)
                    if player_field[row][col] not in ['X', 'O']:
                        break
                    else:
                        print("You already shot there. Try again.")
                else:
                    print("Invalid input. Enter coordinates like B3.")

            attempts += 1

            if field[row][col] == 'S':
                field[row][col] = 'X'
                player_field[row][col] = 'X'
                print("Hit!")

                if is_ship_sunk(field, row, col):
                    print("You sunk a ship!")
            else:
                field[row][col] = 'O'
                player_field[row][col] = 'O'
                print("Miss!")


            if all_ships_sunk(field):
                clear_screen()
                print(f"Congratulations, {player_name}! You won in {attempts} shots.")
                scores.append((player_name, attempts))
                break


        replay = input("Do you want to play again? (yes/no): ").lower()
        if replay != 'yes':

            scores.sort(key=lambda x: x[1])
            print("\nLeaderboard:")
            for i, (name, score) in enumerate(scores, 1):
                print(f"{i}. {name}: {score} shots")
            break


def is_ship_sunk(field, row, col):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        r, c = row, col
        while 0 <= r < 7 and 0 <= c < 7 and field[r][c] == 'X':
            r += dr
            c += dc
        if 0 <= r < 7 and 0 <= c < 7 and field[r][c] == 'S':
            return False
    return True


battleship_game()
