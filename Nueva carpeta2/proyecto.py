import tkinter as tk
import random
import urllib.request
import os

class MemoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de Memoria")

        # Descargar imágenes
        self.download_images()

        # Cargar imágenes
        self.card_images = {i: tk.PhotoImage(file=f"{i}.png") for i in range(1, 9)}
        self.back_image = tk.PhotoImage(file="back.png")

        # Crear un tablero de 4x4
        self.buttons = {}
        self.cards = list(range(1, 9)) * 2  # Dos cartas de cada tipo
        random.shuffle(self.cards)
        self.selected_cards = []  # Lista de cartas volteadas
        self.matches = 0

        # Crear botones para cada carta
        for row in range(4):
            for col in range(4):
                button = tk.Button(self.master, image=self.back_image, width=100, height=100,
                                   command=lambda r=row, c=col: self.card_clicked(r, c))
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

        # Asignar valores de las cartas
        self.card_values = {}
        for row in range(4):
            for col in range(4):
                self.card_values[(row, col)] = self.cards.pop()

        # Crear un label de mensaje
        self.message_label = tk.Label(self.master, text="", font=("Arial", 16))
        self.message_label.grid(row=4, column=0, columnspan=4)

    def card_clicked(self, row, col):
        if (row, col) in self.selected_cards:
            return  # Evitar clics en la misma carta ya seleccionada

        button = self.buttons[(row, col)]
        card_value = self.card_values[(row, col)]

        # Mostrar la imagen de la carta
        button.config(image=self.card_images[card_value])
        self.selected_cards.append((row, col))

        if len(self.selected_cards) == 2:
            self.check_match()

    def check_match(self):
        first, second = self.selected_cards
        first_value = self.card_values[first]
        second_value = self.card_values[second]

        if first_value == second_value:
            self.matches += 1
            self.selected_cards = []  # Reiniciar selección
            if self.matches == 8:  # Todos los pares encontrados
                self.show_win_message()
        else:
            # Ocultar las cartas incorrectas después de 1 segundo
            self.master.after(1000, self.hide_cards)

    def hide_cards(self):
        for row, col in self.selected_cards:
            self.buttons[(row, col)].config(image=self.back_image)
        self.selected_cards = []  # Reiniciar selección

    def show_win_message(self):
        self.message_label.config(text="¡Ganaste!")

    def download_images(self):
        # Enlaces de imágenes mejoradas para los números del 1 al 8
        image_links = {
            "back": "https://via.placeholder.com/100/AAAAAA/FFFFFF?text=Back",  # Imagen de la parte posterior
            1: "https://via.placeholder.com/100/FFFFFF/000000?text=1",  # Carta número 1
            2: "https://via.placeholder.com/100/FFFFFF/000000?text=2",  # Carta número 2
            3: "https://via.placeholder.com/100/FFFFFF/000000?text=3",  # Carta número 3
            4: "https://via.placeholder.com/100/FFFFFF/000000?text=4",  # Carta número 4
            5: "https://via.placeholder.com/100/FFFFFF/000000?text=5",  # Carta número 5
            6: "https://via.placeholder.com/100/FFFFFF/000000?text=6",  # Carta número 6
            7: "https://via.placeholder.com/100/FFFFFF/000000?text=7",  # Carta número 7
            8: "https://via.placeholder.com/100/FFFFFF/000000?text=8",  # Carta número 8
        }

        # Descargar imágenes si no existen
        for name, url in image_links.items():
            filename = f"{name}.png"
            if not os.path.exists(filename):
                try:
                    print(f"Descargando {filename} desde {url}")
                    urllib.request.urlretrieve(url, filename)
                except Exception as e:
                    print(f"Error al descargar {filename}: {e}")
                    # Si la descarga falla, usar una imagen de respaldo
                    if name == "back":
                        url = "https://via.placeholder.com/100/AAAAAA/FFFFFF?text=Back"  # Imagen de respaldo para la parte posterior
                    else:
                        url = "https://via.placeholder.com/100/AAAAAA/FFFFFF?text=Missing"
                    urllib.request.urlretrieve(url, filename)

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
