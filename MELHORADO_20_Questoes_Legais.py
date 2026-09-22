import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font as tkfont

class BinaryTreeNode:
    def __init__(self, data):
        # Cada nó guarda uma informação e pode ter dois "caminhos":
        # um para a esquerda e outro para a direita.
        self.data = data
        self.left_child = None
        self.right_child = None
    def is_leaf(self):
        # Se não existe nenhum filho, significa que chegamos ao final
        # daquele caminho da árvore.
        return self.left_child is None and self.right_child is None
    def to_dict(self):
        # Aqui transformamos a árvore em um formato que o JSON consegue salvar.
        # O nó guarda sua informação e também seus dois possíveis caminhos.
        return {
            "data": self.data,
            "left": self.left_child.to_dict() if self.left_child else None,
            "right": self.right_child.to_dict() if self.right_child else None,
        }
    @classmethod
    def from_dict(cls, data):
        # Essa função faz o caminho contrário da anterior:
        # pega os dados salvos no JSON e monta a árvore novamente.
        if not data:
            return None
        node = cls(data["data"])

        # Recria os filhos da esquerda e da direita.
        node.left_child = cls.from_dict(data["left"])
        node.right_child = cls.from_dict(data["right"])
        return node

def create_default_tree():
    # Aqui criamos uma árvore inicial para o jogo começar
    # caso ainda não exista nenhum arquivo salvo.
    root = BinaryTreeNode("Possui pelos?")

    # Se a resposta for "Sim", seguimos para a esquerda.
    root.left_child = BinaryTreeNode("Ele é domesticável?")
    root.left_child.left_child = BinaryTreeNode("Gato")
    root.left_child.right_child = BinaryTreeNode("Cachorro")

    # Se a resposta for "Não", seguimos para a direita.
    root.right_child = BinaryTreeNode("É um mamífero grande?")
    root.right_child.left_child = BinaryTreeNode("Elefante")
    root.right_child.right_child = BinaryTreeNode("Golfinho")

    return root

class TwentyQuestionsGUI(tk.Tk):
    # Nome do arquivo onde vamos guardar os animais que o jogo aprendeu.
    FILENAME = "mammal_tree.json"
    def __init__(self):
        # Inicializa a janela do Tkinter.
        super().__init__()

        # Tenta carregar uma árvore que já tenha sido salva anteriormente.
        self.tree = self.load_tree()

        # Começamos o jogo pela raiz da árvore.
        self.current_node = self.tree

        # Configurações básicas da janela.
        self.title("20 Questões - Adivinhação de Mamíferos")
        self.geometry("600x280")
        self.configure(bg="#00C4A9")

        # Criamos as fontes que serão usadas nos textos e botões.
        button_font = tkfont.Font(size=12, weight="bold")
        label_font = tkfont.Font(size=18, weight="bold")

        # Esse texto mostra a pergunta ou o animal que está sendo analisado.
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

        # Criamos um espaço para deixar os botões organizados.
        btn_frame = tk.Frame(self, bg="#00C4A9")
        btn_frame.pack(pady=10)

        # Botão para quando a resposta for "Sim".
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

        # Botão para quando a resposta for "Não".
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

        # Botão para quando o jogador não souber responder.
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

        # Botão para quando a resposta estiver entre sim e não.
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

        # Organizamos os quatro botões lado a lado.
        self.yes_button.grid(row=0, column=0, padx=5)
        self.no_button.grid(row=0, column=1, padx=5)
        self.unknown_button.grid(row=0, column=2, padx=5)
        self.maybe_button.grid(row=0, column=3, padx=5)

    def load_tree(self):
        # Primeiro verificamos se já existe um arquivo com os dados do jogo.
        if os.path.exists(self.FILENAME):
            try:
                # Se existir, abrimos o arquivo e pegamos os dados salvos.
                with open(self.FILENAME, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Transformamos os dados do JSON novamente em uma árvore.
                    return BinaryTreeNode.from_dict(data)

            except Exception:
                # Se acontecer algum problema ao carregar o arquivo,
                # simplesmente começamos com a árvore padrão.
                pass

        # Caso seja a primeira vez que o jogo está sendo executado,
        # usamos os animais que já deixamos cadastrados.
        return create_default_tree()

    def save_tree(self):
        # Essa função salva o que o jogo aprendeu para não perder
        # os novos animais quando o programa for fechado.
        try:
            with open(self.FILENAME, "w", encoding="utf-8") as f:
                json.dump(
                    self.tree.to_dict(),
                    f,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as e:
            # Se não conseguir salvar, mostramos uma mensagem de erro.
            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar o jogo: {e}"
            )

    def on_yes(self):
        # Quando o usuário clicar em "Sim", seguimos para o caminho da esquerda.
        self.process_answer(go_left=True)

    def on_no(self):
        # Quando o usuário clicar em "Não", seguimos para o caminho da direita.
        self.process_answer(go_left=False)

    def process_answer(self, go_left):
        # Se chegamos em uma folha, significa que não há mais perguntas
        # e o programa chegou a um possível animal.
        if self.current_node.is_leaf():

            guess = self.current_node.data

            # Perguntamos ao jogador se o animal que pensamos está correto.
            answer = messagebox.askyesno(
                "Palpite",
                f"É um(a) {guess}?"
            )

            if answer:
                # Se acertamos, mostramos uma mensagem de parabéns
                # e começamos uma nova rodada.
                messagebox.showinfo(
                    "Parabéns!",
                    "🎉 Parabéns! Eu adivinhei! 🎉"
                )
                self.restart_game()

            else:
                # Se erramos, damos a oportunidade de ensinar
                # um novo animal para o programa.
                self.add_new_mammal()

        else:
            # Se ainda existem perguntas, seguimos para o próximo nó.
            if go_left:
                self.current_node = self.current_node.left_child
            else:
                self.current_node = self.current_node.right_child

            # Atualizamos o texto da tela para mostrar a nova pergunta.
            self.label.config(text=self.current_node.data)

    def on_unknown(self):
        # Quando o jogador não sabe a resposta, vamos considerar
        # temporariamente como se tivesse respondido "Não".
        messagebox.showinfo(
            "Desconhecido",
            "Vamos considerar isso como uma resposta 'Não' por enquanto.",
        )

        # Só avançamos se ainda estivermos em uma pergunta.
        if not self.current_node.is_leaf():
            self.current_node = self.current_node.right_child
            self.label.config(text=self.current_node.data)

    def on_maybe(self):
        # Como a resposta "Talvez" não é exatamente "Sim" ou "Não",
        # escolhemos seguir pelo caminho do "Sim".
        messagebox.showinfo(
            "Talvez",
            "Vamos seguir pelo caminho do 'Sim'."
        )

        if not self.current_node.is_leaf():
            self.current_node = self.current_node.left_child
            self.label.config(text=self.current_node.data)

    def add_new_mammal(self):
        # Guardamos o animal que o programa achou que era a resposta.
        current_guess = self.current_node.data

        # Perguntamos ao jogador qual era o animal correto.
        new_mammal = simpledialog.askstring(
            "Adicionar Novo Mamífero",
            "Qual era o animal correto?"
        )

        # Se o jogador cancelar ou não digitar nada,
        # voltamos para o começo do jogo.
        if not new_mammal:
            self.restart_game()
            return

        # Agora precisamos de uma pergunta que consiga diferenciar
        # o animal antigo do novo animal.
        new_question = simpledialog.askstring(
            "Nova Pergunta",
            f"Forneça uma pergunta de sim/não para distinguir "
            f"{current_guess} de {new_mammal}:",
        )

        if not new_question:
            self.restart_game()
            return

        # Perguntamos se a resposta para o novo animal seria "Sim".
        # Isso define em qual lado da árvore o novo animal ficará.
        correct_answer = messagebox.askyesno(
            "Resposta Correta",
            f"Para o seu animal ({new_mammal}), a resposta para "
            f"'{new_question}' é Sim?"
        )

        # O antigo animal deixa de ser uma folha e passa a fazer parte
        # de uma nova pergunta.
        self.current_node.data = new_question

        if correct_answer:
            # Se a resposta for "Sim", o novo animal fica à esquerda
            # e o animal antigo fica à direita.
            self.current_node.left_child = BinaryTreeNode(new_mammal)
            self.current_node.right_child = BinaryTreeNode(current_guess)

        else:
            # Se a resposta for "Não", fazemos o contrário.
            self.current_node.left_child = BinaryTreeNode(current_guess)
            self.current_node.right_child = BinaryTreeNode(new_mammal)

        # Depois de aprender o novo animal, salvamos a árvore.
        self.save_tree()

        messagebox.showinfo(
            "Banco de Dados Atualizado",
            f"{new_mammal} foi aprendido e salvo com sucesso!",
        )

        # Começamos uma nova rodada.
        self.restart_game()

    def restart_game(self):
        # Voltamos para o primeiro nó da árvore para começar novamente.
        self.current_node = self.tree

        # Atualizamos a pergunta mostrada na tela.
        self.label.config(text=self.current_node.data)


# Essa parte só é executada quando este arquivo é executado diretamente.
if __name__ == "__main__":

    # Criamos o programa.
    app = TwentyQuestionsGUI()

    # Mantemos a janela aberta esperando as ações do usuário.
    app.mainloop()
