import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font as tkfont

class BinaryTreeNode:
    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None

    def is_leaf(self):
        return self.left_child is None and self.right_child is None

def create_mammal_tree():
    root = BinaryTreeNode("Possui pelos?")

    root.left_child = BinaryTreeNode("Ele é domesticável?")
    root.left_child.left_child = BinaryTreeNode("Eh um gato?")
    root.left_child.right_child = BinaryTreeNode("Eh um cachorro?")

    root.right_child = BinaryTreeNode("É um mamífero grande?")
    root.right_child.left_child = BinaryTreeNode("Eh um elefante?")
    root.right_child.right_child = BinaryTreeNode("Eh um golfinho?")

    return root

class TwentyQuestionsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tree = create_mammal_tree()  # Load the initial mammal tree
        self.current_node = self.tree  # Start at the root of the tree
        self.title("20 Questões legais")
        self.geometry("560x250")

        self.configure(bg="#00C4A9")  # Alice Blue background
        button_font = tkfont.Font(size=12, weight="bold")
        label_font = tkfont.Font(size=22, weight="bold")

        self.label = tk.Label(
            self, text=self.current_node.data, bg="#00C4A9", font=label_font
        )
        self.label.pack(pady=15)

        self.yes_button = tk.Button(
            self, text="Sim", command=self.on_yes, bg="#32CD32", font=button_font, height=2, width=10
        )
        self.no_button = tk.Button(
            self, text="Não", command=self.on_no, bg="#FF4500", font=button_font, height=2, width=10
        )
        self.unknown_button = tk.Button(
            self, text="Não sei", command=self.on_unknown, bg="#FFD700", font=button_font, height=2, width=10
        )
        self.maybe_button = tk.Button(
            self, text="Talvez", command=self.on_maybe, bg="#87CEEB", font=button_font, height=2, width=10
        )

        self.yes_button.pack(side=tk.LEFT, padx=10, pady=15)
        self.no_button.pack(side=tk.LEFT, padx=10, pady=15)
        self.unknown_button.pack(side=tk.LEFT, padx=10, pady=15)
        self.maybe_button.pack(side=tk.RIGHT, padx=10, pady=15)

    def on_yes(self):
        if self.current_node.is_leaf():
            guess = self.current_node.data
            answer = messagebox.askyesno("Palpite", f"Eh um(a) {guess}?")
            if answer:
                messagebox.showinfo(
                    "Parabéns!", f"🎉 Parabéns! Eu adivinhei! 🎉"
                )
                self.restart_game()
            else:
                self.add_new_mammal()
        else:
            self.current_node = self.current_node.left_child
            self.label.config(text=self.current_node.data)

    def on_no(self):
        if self.current_node.is_leaf():
            guess = self.current_node.data
            answer = messagebox.askyesno("Palpite", f"Eh um(a) {guess}?")
            if answer:
                messagebox.showinfo(
                    "Parabéns!", f"🎉 Parabéns! Eu adivinhei! 🎉"
                )
                self.restart_game()
            else:
                self.add_new_mammal()
        else:
            self.current_node = self.current_node.right_child
            self.label.config(text=self.current_node.data)

    def on_unknown(self):
        messagebox.showinfo(
            "Desconhecido",
            "Se você não tiver certeza, vamos considerar isso como uma resposta 'Não' por enquanto.",
        )
        if not self.current_node.is_leaf():
            self.current_node = self.current_node.right_child
            self.label.config(text=self.current_node.data)

    def on_maybe(self):
        messagebox.showinfo(
        "Talvez",
        "Como é um talvez, vamos seguir pelo caminho do 'Sim'.",
        )
        if not self.current_node.is_leaf():
            self.current_node = self.current_node.left_child
            self.label.config(text=self.current_node.data)

    def add_new_mammal(self):
        current_guess = self.current_node.data
        new_mammal = simpledialog.askstring("Adicionar Novo Mamífero", "Qual é a resposta correta?")
        new_question = simpledialog.askstring(
        "Nova Pergunta",
        f"Forneça uma pergunta de sim/não para distinguir {current_guess} de {new_mammal}:"
        )
        correct_answer = messagebox.askyesno(
        "Resposta Correta", f"Para o seu mamífero, {new_question}?"
        )

        self.current_node.data = new_question
        if correct_answer:
            self.current_node.left_child = BinaryTreeNode(new_mammal)
            self.current_node.right_child = BinaryTreeNode(current_guess)
        else:
            self.current_node.left_child = BinaryTreeNode(current_guess)
            self.current_node.right_child = BinaryTreeNode(new_mammal)

        messagebox.showinfo("Banco de Dados Atualizado", f"{new_mammal} foi adicionado ao jogo.")

        self.restart_game()

    def restart_game(self):
        self.current_node = self.tree
        self.label.config(text=self.current_node.data)

if __name__ == "__main__":
    app = TwentyQuestionsGUI()
    app.mainloop()
