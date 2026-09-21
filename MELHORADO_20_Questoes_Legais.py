import json
import os
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

    def to_dict(self):
        """Converte a árvore em um dicionário para salvar em JSON."""
        return {
            "data": self.data,
            "left": self.left_child.to_dict() if self.left_child else None,
            "right": self.right_child.to_dict() if self.right_child else None,
        }

    @classmethod
    def from_dict(cls, data):
        """Recria a árvore a partir de um dicionário."""
        if not data:
            return None
        node = cls(data["data"])
        node.left_child = cls.from_dict(data["left"])
        node.right_child = cls.from_dict(data["right"])
        return node


def create_default_tree():
    root = BinaryTreeNode("Possui pelos?")

    root.left_child = BinaryTreeNode("Ele é domesticável?")
    root.left_child.left_child = BinaryTreeNode("Gato")
    root.left_child.right_child = BinaryTreeNode("Cachorro")

    root.right_child = BinaryTreeNode("É um mamífero grande?")
    root.right_child.left_child = BinaryTreeNode("Elefante")
    root.right_child.right_child = BinaryTreeNode("Golfinho")

    return root


class TwentyQuestionsGUI(tk.Tk):
    FILENAME = "mammal_tree.json"

    def __init__(self):
        super().__init__()
        self.tree = self.load_tree()
        self.current_node = self.tree

        self.title("20 Questões - Adivinhação de Mamíferos")
        self.geometry("600x280")
        self.configure(bg="#00C4A9")

        button_font = tkfont.Font(size=12, weight="bold")
        label_font = tkfont.Font(size=18, weight="bold")

        self.label = tk.Label(
            self,
            text=self.current_node.data,
            bg="#00C4A9",
            fg="#FFFFFF",
            font=label_font,
            wraplength=550,
            justify="center",
        )
        self.label.pack(pady=20)

        # Container para os botões para melhor organização
        btn_frame = tk.Frame(self, bg="#00C4A9")
        btn_frame.pack(pady=10)

        self.yes_button = tk.Button(
            btn_frame,
            text="Sim",
            command=self.on_yes,
            bg="#32CD32",
            fg="#FFFFFF",
            font=button_font,
            height=2,
            width=10,
        )
        self.no_button = tk.Button(
            btn_frame,
            text="Não",
            command=self.on_no,
            bg="#FF4500",
            fg="#FFFFFF",
            font=button_font,
            height=2,
            width=10,
        )
        self.unknown_button = tk.Button(
            btn_frame,
            text="Não sei",
            command=self.on_unknown,
            bg="#FFD700",
            fg="#000000",
            font=button_font,
            height=2,
            width=10,
        )
        self.maybe_button = tk.Button(
            btn_frame,
            text="Talvez",
            command=self.on_maybe,
            bg="#87CEEB",
            fg="#000000",
            font=button_font,
            height=2,
            width=10,
        )

        self.yes_button.grid(row=0, column=0, padx=5)
        self.no_button.grid(row=0, column=1, padx=5)
        self.unknown_button.grid(row=0, column=2, padx=5)
        self.maybe_button.grid(row=0, column=3, padx=5)

    def load_tree(self):
        """Carrega a árvore do arquivo JSON se existir, senão cria a padrão."""
        if os.path.exists(self.FILENAME):
            try:
                with open(self.FILENAME, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return BinaryTreeNode.from_dict(data)
            except Exception:
                pass
        return create_default_tree()

    def save_tree(self):
        """Salva a árvore atual em um arquivo JSON."""
        try:
            with open(self.FILENAME, "w", encoding="utf-8") as f:
                json.dump(self.tree.to_dict(), f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o jogo: {e}")

    def on_yes(self):
        self.process_answer(go_left=True)

    def on_no(self):
        self.process_answer(go_left=False)

    def process_answer(self, go_left):
        if self.current_node.is_leaf():
            guess = self.current_node.data
            answer = messagebox.askyesno("Palpite", f"É um(a) {guess}?")
            if answer:
                messagebox.showinfo(
                    "Parabéns!", "🎉 Parabéns! Eu adivinhei! 🎉"
                )
                self.restart_game()
            else:
                self.add_new_mammal()
        else:
            if go_left:
                self.current_node = self.current_node.left_child
            else:
                self.current_node = self.current_node.right_child
            self.label.config(text=self.current_node.data)

    def on_unknown(self):
        messagebox.showinfo(
            "Desconhecido",
            "Vamos considerar isso como uma resposta 'Não' por enquanto.",
        )
        if not self.current_node.is_leaf():
            self.current_node = self.current_node.right_child
            self.label.config(text=self.current_node.data)

    def on_maybe(self):
        messagebox.showinfo(
            "Talvez", "Vamos seguir pelo caminho do 'Sim'."
        )
        if not self.current_node.is_leaf():
            self.current_node = self.current_node.left_child
            self.label.config(text=self.current_node.data)

    def add_new_mammal(self):
        current_guess = self.current_node.data
        new_mammal = simpledialog.askstring(
            "Adicionar Novo Mamífero", "Qual era o animal correto?"
        )
        if not new_mammal:
            self.restart_game()
            return

        new_question = simpledialog.askstring(
            "Nova Pergunta",
            f"Forneça uma pergunta de sim/não para distinguir {current_guess} de {new_mammal}:",
        )
        if not new_question:
            self.restart_game()
            return

        correct_answer = messagebox.askyesno(
            "Resposta Correta", f"Para o seu animal ({new_mammal}), a resposta para '{new_question}' é Sim?"
        )

        self.current_node.data = new_question
        if correct_answer:
            self.current_node.left_child = BinaryTreeNode(new_mammal)
            self.current_node.right_child = BinaryTreeNode(current_guess)
        else:
            self.current_node.left_child = BinaryTreeNode(current_guess)
            self.current_node.right_child = BinaryTreeNode(new_mammal)

        self.save_tree()
        messagebox.showinfo(
            "Banco de Dados Atualizado",
            f"{new_mammal} foi aprendido e salvo com sucesso!",
        )
        self.restart_game()

    def restart_game(self):
        self.current_node = self.tree
        self.label.config(text=self.current_node.data)


if __name__ == "__main__":
    app = TwentyQuestionsGUI()
    app.mainloop()
