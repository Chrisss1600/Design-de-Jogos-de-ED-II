# Design-de-Jogos-de-ED-II

# Jogo de 20 Questões

Este projeto consiste em uma implementação do jogo **“20 Questões”**, desenvolvido em Python utilizando a biblioteca **Tkinter** para a criação da interface gráfica.

O objetivo do jogo é descobrir qual mamífero o jogador está pensando por meio de uma sequência de perguntas que podem ser respondidas com **“Sim”, “Não”, “Não sei” ou “Talvez”**.

A estrutura principal utilizada no projeto é uma **árvore binária de decisão**. Cada nó da árvore representa uma pergunta, enquanto seus dois filhos representam os possíveis caminhos de resposta. O programa percorre a árvore de acordo com as respostas do jogador até chegar a um nó folha, que contém o possível mamífero escolhido.

Uma das funcionalidades do jogo é a capacidade de **aprender novos mamíferos**. Quando o programa erra o palpite, o jogador pode informar o animal correto e fornecer uma nova pergunta que permita diferenciá-lo do animal que estava cadastrado anteriormente. Dessa forma, a árvore é atualizada e passa a considerar a nova informação nas próximas partidas.

O projeto tem como principal objetivo demonstrar, de forma prática e interativa, a utilização de **árvores binárias, nós, percursos e inserção de novos elementos**, aplicando conceitos estudados na disciplina de **Estrutura de Dados II**.

https://github.com/buyan-kh/20questions_game/tree/main
