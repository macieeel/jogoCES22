# 3030: Esqueci de Liberar
> Jogo em Python

Projeto CES-22, ITA 2022

### Alunos:
<!--ts-->
* Bernardo Hoffmann da Silva
* Marcos Vinicius Pereira Veloso
* Victor Maciel
<!--te-->


## Como rodar a aplicação:
No terminal, clone o projeto: 
```
git clone https://github.com/macieeel/jogoCES22.git
```
Existem várias branches neste git. 
A final do jogo está na branch main.

O jogo se trata de um entregador que precisa entregar pizzas enquanto está fugindo da polícia.

## INSTRUÇÕES:

Ande pelo mapa com WASD ou Setas (direita e esquerda rotacionam sua moto).
Andar na grama diminui sua velocidade e blocos amarelos e verdes escuro são prédios e árvores, e são intransponíveis.
Para entregar as pizzas, siga a seta vermelha do canto superior esquerdo, e quando chegar no marcador, segure a barra de espaço até realizar a entrega.
Cuidado, cada entrega possui um tempo limite indicado na barra.
Não dirija na água e não deixe a polícia encostar em você!

Para rodar o jogo, execute o arquivo main.py.

## PASTAS:

### img

Pasta que contém as sprites, imagem background, fontes, tiles do mapa.

### maps

Pasta que contém o arquivo TMX do mapa, arquivos utilizados no TILED para gerenciar os tiles do mapa. Existem três versões do mapa diferentes, e a mais atualizada é a mapav2.


### sounds

Pasta com tudo que é relacionado ao som do jogo. Contém as músicas e efeitos sonoros.

### textos

Pasta com todos os arquivos de imagem utilizados para rotular os prédios do mapa.

DESCRIÇÃO DOS ARQUIVOS .py

### main.py

Execute para jogar o jogo. Possui a classe jogo e a declaração dos objetos com as classes declaradas em outros arquivos. Gerencia as telas iniciais, de game over, de jogo e de pause. Possui as funções principais de update e draw. Realiza o controle dos sons e música. 




