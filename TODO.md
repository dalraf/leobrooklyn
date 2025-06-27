# Lista de Tarefas para Melhorias no Código

Este documento detalha as melhorias sugeridas para o arquivo `main.py`, com foco em legibilidade, manutenção, eficiência e boas práticas de programação.

## 1. Centralização e Nomenclatura de Constantes

### Objetivo
Mover todos os "números mágicos" e valores fixos para o arquivo `config.py`, atribuindo-lhes nomes descritivos e consistentes. Isso melhora a legibilidade, facilita a manutenção e permite ajustes rápidos em um único local.

### Detalhes
- **`main.py`**:
    - **`self.state.tick_enemies = 100`**: Substituir `100` por uma constante como `ENEMY_SPAWN_TICK_RESET`.
    - **`SCREEN_WIDTH * 0.8`**: Substituir `0.8` por uma constante como `PARALLAX_START_THRESHOLD`.
    - **`screen.fill((255, 255, 255))`**: Substituir `(255, 255, 255)` por uma constante como `WHITE_COLOR`.
    - **`self.state.clock.tick(25)`**: Substituir `25` (FPS) por uma constante como `GAME_FPS`.
- **`config.py`**:
    - Adicionar as seguintes constantes:
        - `ENEMY_SPAWN_TICK_RESET = 100`
        - `PARALLAX_START_THRESHOLD = 0.8`
        - `WHITE_COLOR = (255, 255, 255)`
        - `GAME_FPS = 25`
    - Garantir que `DIFICULT_AVANCE` e `DERIVACAO` já estejam bem definidas e com nomes claros.

## 2. Otimização e Gerenciamento de Grupos de Sprites

### Objetivo
Melhorar a eficiência do gerenciamento de sprites, especialmente o grupo `All_sprites`, para evitar operações redundantes a cada frame.

### Detalhes
- **`main.py` - Método `draw_elements`**:
    - A linha `All_sprites.add(...)` para adicionar todos os grupos a `All_sprites` a cada frame é redundante e pode ser ineficiente.
    - **Ação**: Modificar a lógica para que os sprites sejam adicionados a `All_sprites` apenas uma vez (quando são criados) e removidos quando são "mortos" ou se tornam inativos.
    - **Alternativa (se `All_sprites` for apenas para ordenação de desenho)**: Em vez de adicionar a um grupo global, criar uma lista temporária de todos os sprites ativos a cada frame para a ordenação e desenho. Exemplo:
        ```python
        all_active_sprites = []
        all_active_sprites.extend(grupo_player)
        all_active_sprites.extend(grupo_enemy)
        # ... e assim por diante para outros grupos
        for sprite in sorted(all_active_sprites, key=lambda spr: spr.rect.bottom):
            screen.blit(sprite.image, sprite.rect)
        ```
    - **Verificar `grupos.py`**: Entender como `All_sprites` é inicializado e se ele já é um grupo que gerencia a adição/remoção de sprites. Se não for, ajustar a lógica de adição/remoção nas classes `Player`, `Enemy`, `Objetcs` etc.

## 3. Refatoração da Lógica de Colisão e Ataque

### Objetivo
Encapsular a lógica de colisão e ataque dentro das classes dos próprios sprites (`Player`, `Enemy`), tornando o código mais modular e legível.

### Detalhes
- **`main.py` - Métodos `object_sprite_colide`, `object_sprite_get`, `player_enemy_attack_hit`**:
    - A lógica de verificação de distância e direção de ataque está atualmente no `main.py`.
    - **Ação**: Mover a lógica de verificação de colisão e dano para métodos específicos dentro das classes `Player` e `Enemy`.
    - **Exemplo para `player_enemy_attack_hit`**:
        - Criar um método `check_attack_hit(target_sprite)` em `Player` e `Enemy` que retorne `True` se o ataque for bem-sucedido e `False` caso contrário.
        - O método em `main.py` então chamaria esses novos métodos, simplificando sua lógica.
        ```python
        # Exemplo de como ficaria em main.py após a refatoração
        def player_enemy_attack_hit(self):
            for player_single in grupo_player:
                for enemy_single in grupo_enemy:
                    if player_single.check_attack_hit(enemy_single):
                        self.state.placar.add_enemy_kill(enemy_single.speed)
                        enemy_single.move_hit(player_single.calcule_hit())

                    if enemy_single.check_attack_hit(player_single):
                        player_single.move_hit(enemy_single.calcule_hit())
        ```
    - **Considerar `pygame.sprite.groupcollide`**: Para colisões mais simples (sem lógica de direção complexa), as funções de colisão do Pygame podem ser mais eficientes. Avaliar se `calcule_vetor_distance` ainda é a melhor abordagem ou se as funções nativas do Pygame podem ser utilizadas.

## 4. Inicialização do Player no Início do Jogo

### Objetivo
Garantir que o objeto `Player` seja inicializado corretamente tanto no início do jogo quanto ao reiniciar.

### Detalhes
- **`main.py` - Classe `Game`**:
    - Atualmente, o `self.state.player` e a adição ao `grupo_player` só ocorrem no método `restart_game`.
    - **Ação**: Adicionar a inicialização do `player` no método `__init__` da classe `Game` ou em um método `start_game` separado que é chamado uma vez no início. Isso garante que o jogo comece com um jogador válido.

## 5. Melhoria da Legibilidade (Nomenclatura e Comentários)

### Objetivo
Aumentar a clareza do código através de nomes de variáveis e funções mais descritivos, e adicionar comentários onde a lógica é complexa.

### Detalhes
- **Nomenclatura**:
    - `tick_enemies`: Renomear para `enemy_spawn_timer` ou similar.
    - `paralaxe`: Renomear para `parallax_offset` ou `background_scroll_speed`.
    - Avaliar outras variáveis e métodos para garantir que seus nomes reflitam claramente sua função.
- **Comentários**:
    - Adicionar comentários explicativos para blocos de código complexos, como a lógica de geração de inimigos baseada na distância e a lógica detalhada de ataque em `player_enemy_attack_hit` (antes da refatoração).

## 6. Considerações Futuras (Não Prioritário Agora)

### Objetivo
Identificar áreas para possíveis melhorias futuras, como tratamento de erros e modularização adicional.

### Detalhes
- **Tratamento de Erros**: Adicionar blocos `try-except` para operações que podem falhar (ex: carregamento de arquivos, inicialização do Pygame, etc.).
- **Modularização**: Se o `main.py` continuar a crescer, considerar mover partes da lógica (ex: gerenciamento de eventos, atualização de estado) para classes ou módulos separados para manter o `main.py` mais limpo e focado na orquestração geral do jogo.
