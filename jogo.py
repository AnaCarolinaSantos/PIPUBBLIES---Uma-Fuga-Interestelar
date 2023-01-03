from random import randint
import random 
import arcade
import os
import math
# site de referência: https://arcade.academy/examples/sprite_bullets.html#sprite-bullets

largura = 854
altura = 570

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        #telas
        self.tela_menu = arcade.Sprite("imagens/fundoTitulo.png", center_x =427, center_y=285)
        self.tela_informacoes = arcade.Sprite("imagens/telaInformações.png", center_x=427, center_y=285)
        self.tela_itens = arcade.Sprite("imagens/telapowerups.png", center_x=427, center_y=285)
        self.tela_historia = arcade.Sprite("imagens/telaHistoriaTexto.png", center_x=427, center_y=285)

        #botões
        self.botao_play = arcade.Sprite("imagens/botaoStart.png", center_x=427, center_y=200, scale=0.20)
        self.botao_ajuda = arcade.Sprite("imagens/botaoAjuda.png", center_x=80, center_y=50, scale=0.13)
        self.botao_voltar = arcade.Sprite("imagens/botaoVoltar.png", center_x=40, center_y=35, scale=0.60)
        self.botao_comoJogar = arcade.Sprite("imagens/comoJogar.png", center_x=232, center_y=486)
        self.botao_itens = arcade.Sprite("imagens/botaoItens.png", center_x=344, center_y=486)
        self.botao_pular = arcade.Sprite("imagens/botaoPular.png", center_x=770, center_y=35, scale=0.60)

        # troca de telas
        self.tela_2 = False
        self.tela_3 = False
        self.tela_4 = False
        self.tela_5 = False

    def on_draw(self):
        arcade.start_render()
        self.tela_menu.draw()
        self.botao_play.draw()
        self.botao_ajuda.draw()
        if self.tela_3: #tela informações
            self.tela_informacoes.draw()
            self.botao_itens.draw()
            self.botao_comoJogar.draw()
            self.botao_voltar.draw()
        if self.tela_4: #tela itens
            self.tela_itens.draw()
            self.botao_itens.draw()
            self.botao_comoJogar.draw()
            self.botao_voltar.draw()
        if self.tela_5: #tela história
            self.tela_historia.draw()
            self.botao_pular.draw()
            self.botao_voltar.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Parte das telas
       
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_ajuda.right and x > self.botao_ajuda.left and y < self.botao_ajuda.top and y > self.botao_ajuda.bottom:
            self.tela_1 = False #menu
            self.tela_3 = True  # informações
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_play.right and x > self.botao_play.left and y < self.botao_play.top and y > self.botao_play.bottom:
            self.tela_1 = False  # menu
            self.tela_5 = True  # tela história
        if self.tela_5:
            if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_pular.right and x > self.botao_pular.left and y < self.botao_pular.top and y > self.botao_pular.bottom:
                self.tela_5 = False  # menu
                game = GameView() #tela jogo
                self.window.show_view(game)
            if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_voltar.right and x > self.botao_voltar.left and y < self.botao_voltar.top and y > self.botao_voltar.bottom:
                self.tela_5 = False
                self.tela_1 = True #volta para o menu
        if self.tela_3:  # botao voltar tela de itens
            if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_itens.right and x > self.botao_itens.left and y < self.botao_itens.top and y > self.botao_itens.bottom:
                self.tela_3 = False
                self.tela_4 = True
            if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_voltar.right and x > self.botao_voltar.left and y < self.botao_voltar.top and y > self.botao_voltar.bottom:
                self.tela_3 = False
                self.tela_1 = True
        if self.tela_4:  # botao voltar
            if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_comoJogar.right and x > self.botao_comoJogar.left and y < self.botao_comoJogar.top and y > self.botao_comoJogar.bottom:
                self.tela_4 = False
                self.tela_3 = True
            if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_voltar.right and x > self.botao_voltar.left and y < self.botao_voltar.top and y > self.botao_voltar.bottom:
                self.tela_4 = False
                self.tela_1 = True

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        #telas
        self.pos_x = 400
        self.pos_y = 285
        self.tela_jogo = arcade.Sprite("imagens/cenario.png")
        self.pos_x2 = 1200
        self.pos_y2 = 285
        self.cenario2= arcade.Sprite("imagens/cenario2.png")
        
        #telas
        self.botao_pause = arcade.Sprite("imagens/botaoPause.png", center_x=800, center_y=540, scale=0.60)

        #listas
        self.player_list = None
        self.tiro_list = None
        self.player_list = arcade.SpriteList()
        self.tiro_list = arcade.SpriteList()
        self.enemy_list = None
        self.tiro_verde_list = None
        self.enemy_list = arcade.SpriteList()
        self.tiro_verde_list = arcade.SpriteList()

        #teclas
        self.UP = False
        self.DOWN = False

        #Contadores
        self.frame_count = 0
        self.score = 0
        self.time_taken = 0
       
        # sons provisórios
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        #Sprites
        self.navePipubblies = arcade.Sprite("imagens/nave_pipubblies.png", scale=0.80)
        self.navePipubblies.center_x = 650
        self.navePipubblies.center_y = 285
        self.player_list.append(self.navePipubblies)

        self.pos_asteroide1_x = 0
        self.pos_asteroide1_y = 0
        self.pos_asteroide2_x = 0
        self.pos_asteroide2_y = 0
        self.pos_asteroide3_x = 0
        self.pos_asteroide3_y = 0
        self.pos_asteroide4_x = 0
        self.pos_asteroide4_y = 0
        self.asteroide1 = arcade.Sprite("imagens/asteroide.png", center_x=self.pos_asteroide1_x, center_y=self.pos_asteroide1_y)
        self.asteroide2 = arcade.Sprite("imagens/asteroide2.png", center_x=self.pos_asteroide2_x, center_y=self.pos_asteroide2_y)
        self.asteroide3 = arcade.Sprite("imagens/asteroide3.png", center_x=self.pos_asteroide3_x, center_y=self.pos_asteroide3_y)
        self.asteroide4 = arcade.Sprite("imagens/asteroide4.png", center_x=self.pos_asteroide4_x, center_y=self.pos_asteroide4_y)

        
        self.nave_verde1 = arcade.Sprite("imagens/nave_inimigo_verde.png", center_x=200, center_y=430,  scale=0.80)
        self.nave_verde2 = arcade.Sprite("imagens/nave_inimigo_verde.png", center_x=250, center_y=287, scale=0.80)
        self.nave_verde3 = arcade.Sprite("imagens/nave_inimigo_verde.png", center_x=200, center_y=140, scale=0.80)
        self.enemy_list.append(self.nave_verde1)
        self.enemy_list.append(self.nave_verde2)
        self.enemy_list.append(self.nave_verde3)

    def on_draw(self):
        self.tela_jogo.draw()
        self.cenario2.draw()
        self.asteroide1.draw()
        self.asteroide2.draw()
        self.asteroide3.draw()
        self.asteroide4.draw()
        self.botao_pause.draw()
        self.tiro_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.tiro_verde_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 427, 530, arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        self.tiro_list.update()
        self.navePipubblies.update()
        self.tiro_verde_list.update()
        self.enemy_list.update()
        player_speed = 10
        self.frame_count += 1

        #Tiros verdes
     
        for self.nave_verde1 in self.enemy_list:

            start_x = self.nave_verde1.center_x
            start_y = self.nave_verde1.center_y

            dest_x = self.navePipubblies.center_x
            dest_y = self.navePipubblies.center_y
            
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            if self.frame_count % 75 == 0:
                self.disparoVerde = arcade.Sprite("imagens/disparoVerde.png", scale=0.4)
                self.disparoVerde.center_x = start_x
                self.disparoVerde.center_y = start_y
                self.disparoVerde.center_x = self.nave_verde1.center_x
                self.disparoVerde_speed = 3

                # Angle the bullet sprite
                self.disparoVerde.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x and change_y. Velocity is how fast the bullet travels.
                self.disparoVerde.change_x = math.cos(angle) * self.disparoVerde_speed
                self.disparoVerde.change_y = math.sin(angle) * self.disparoVerde_speed
                self.tiro_verde_list.append(self.disparoVerde)

            for self.disparoVerde in self.tiro_verde_list:

                self.hit_list2 = arcade.check_for_collision_with_list(self.disparoVerde, self.player_list)

                if len(self.hit_list2) > 0:
                    self.disparoVerde.remove_from_sprite_lists()

                for self.navePipubblies in self.hit_list2:
                    self.navePipubblies.remove_from_sprite_lists()
                    #self.score += 5
                    arcade.play_sound(self.hit_sound)
            
            for self.disparoVerde in self.tiro_verde_list:
                if self.disparoVerde.bottom < 0:
                    self.disparoVerde.remove_from_sprite_lists()   
      
        #Tiros pipubblies
        for self.tiro_pipubblie in self.tiro_list:

            self.hit_list1 = arcade.check_for_collision_with_list(self.tiro_pipubblie, self.enemy_list)

            if len(self.hit_list1) > 0:
                self.tiro_pipubblie.remove_from_sprite_lists()

            for self.nave_verde1 in self.hit_list1:
                self.nave_verde1.remove_from_sprite_lists()
                self.score += 5
                arcade.play_sound(self.hit_sound)
               
        #Movimentos asteróides
        self.pos_asteroide1_x -= 3
        self.pos_asteroide2_x -= 4
        self.pos_asteroide3_x -= 3
        self.pos_asteroide4_x -= 3

        if self.pos_asteroide1_x <= -45:
            self.pos_asteroide1_y = randint(10, 560)
            self.pos_asteroide1_x = randint(890, 1000)

        if self.pos_asteroide2_x <= -40:
            self.pos_asteroide2_y = randint(10, 560)
            self.pos_asteroide2_x = randint(890, 1000)

        if self.pos_asteroide3_x <= -40:
            self.pos_asteroide3_y = randint(10, 560)
            self.pos_asteroide3_x = randint(890, 1000)

        if self.pos_asteroide4_x <= -40:
            self.pos_asteroide4_y = randint(10, 560)
            self.pos_asteroide4_x = randint(890, 1000)

        self.asteroide1.set_position(self.pos_asteroide1_x, self.pos_asteroide1_y)
        self.asteroide2.set_position(self.pos_asteroide2_x, self.pos_asteroide2_y)
        self.asteroide3.set_position(self.pos_asteroide3_x, self.pos_asteroide3_y)
        self.asteroide4.set_position(self.pos_asteroide4_x, self.pos_asteroide4_y)

        self.asteroide1.update()
        self.asteroide2.update()
        self.asteroide3.update()
        self.asteroide4.update()

       #Movimentos da nave e do fundo
        
        if self.navePipubblies.center_y < 490:
            if self.UP:
                self.navePipubblies.center_y += player_speed
        if self.navePipubblies.center_y > 70:
            if self.DOWN:
                self.navePipubblies.center_y -= player_speed
        
        self.navePipubblies.set_position(self.navePipubblies.center_x, self.navePipubblies.center_y)    
       
        self.pos_x -= 2
        self.pos_x2 -= 2
        
        if self.pos_x <= -400:
            self.pos_x = 1200
        if self.pos_x2 <= -400:
            self.pos_x2 = 1200

        self.tela_jogo.set_position(self.pos_x, self.pos_y)  
        self.cenario2.set_position(self.pos_x2, self.pos_y2)      
        self.tela_jogo.update()
        self.cenario2.update()

        self.time_taken += delta_time

        if len(self.player_list) == 0:
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.show_view(game_over_view)
        
    def on_key_press(self, key, modifiers):  # movimentos da nave
        self.tiro_pipubblie = arcade.Sprite("imagens/disparoPipubblies.png", scale=0.5)
        self.tiro_sepeed = 5
        if key == arcade.key.UP:
            self.UP = True
        if key == arcade.key.DOWN:
            self.DOWN = True
        if key == arcade.key.SPACE:
            self.tiro_pipubblie.change_x -= self.tiro_sepeed
            self.tiro_pipubblie.center_x = self.navePipubblies.center_x
            self.tiro_pipubblie.bottom = self.navePipubblies.bottom
            self.tiro_list.append(self.tiro_pipubblie)
            arcade.play_sound(self.gun_sound)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.UP = False
        if key == arcade.key.DOWN:
            self.DOWN = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_pause.right and x > self.botao_pause.left and y < self.botao_pause.top and y > self.botao_pause.bottom:
            pause = PauseView(self)
            self.window.show_view(pause)
            
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        #telas
        
        self.tela_pause = arcade.Sprite("imagens/telaPause.png", center_x=427, center_y=285)

        #botões
        self.botao_resume = arcade.Sprite("imagens/botaoResume.png", center_x=370, center_y=210)
        self.botao_exit = arcade.Sprite("imagens/botaoExit.png", center_x=490, center_y=210)

    def on_draw(self):
        arcade.start_render()
        self.tela_pause.draw()
        self.botao_resume.draw()
        self.botao_exit.draw()

        self.navePipubblies = self.game_view.navePipubblies
        self.nave_verde1 = self.game_view.nave_verde1
        self.nave_verde2 = self.game_view.nave_verde2
        self.nave_verde3 = self.game_view.nave_verde3
        self.tiro_verde_list = self.game_view.tiro_verde_list
        

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_resume.right and x > self.botao_resume.left and y < self.botao_resume.top and y > self.botao_resume.bottom:
                self.window.show_view(self.game_view)
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_exit.right and x > self.botao_exit.left and y < self.botao_exit.top and y > self.botao_exit.bottom:
            menu_view = MenuView()
            self.window.show_view(menu_view)
  
                
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

        #telas
        self.tela_gameOver = arcade.Sprite("imagens/gameOver.png", center_x=427, center_y=285)

        #botões
        self.botao_exit = arcade.Sprite("imagens/botaoExit.png", center_x=490, center_y=210)
        self.botao_jogarNovamente = arcade.Sprite("imagens/botaoJogarNovamente.png", center_x=365, center_y=210)
        
    def on_draw(self):
        arcade.start_render()
        self.tela_gameOver.draw()
        self.botao_exit.draw()
        self.botao_jogarNovamente.draw()
        time_taken_formatted = f"{round(self.time_taken, 2)} segundos"
        arcade.draw_text(f"Duração: {time_taken_formatted}", largura/2, 280, arcade.color.WHITE, font_size=15, anchor_x="center")
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_jogarNovamente.right and x > self.botao_jogarNovamente.left and y < self.botao_jogarNovamente.top and y > self.botao_jogarNovamente.bottom:
            game_view = GameView()
            self.window.show_view(game_view)
        if button == arcade.MOUSE_BUTTON_LEFT and x < self.botao_exit.right and x > self.botao_exit.left and y < self.botao_exit.top and y > self.botao_exit.bottom:
            menu_view = MenuView()
            self.window.show_view(menu_view)

def main():
    window = arcade.Window(largura, altura, "Pipubblies Uma Fuga Interestelar")
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()