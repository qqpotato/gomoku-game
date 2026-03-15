#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五子棋游戏 - 图片按钮版
保留完整 AI 和规则，使用图片避免字体问题
"""

import pygame
import sys
import random
import os
from PIL import Image

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
GRID_SIZE = 15
CELL_SIZE = 40
MARGIN = 60
BOARD_SIZE = (GRID_SIZE - 1) * CELL_SIZE

COLOR_BG = (220, 179, 130)
COLOR_LINE = (0, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)


def get_resource_path(name):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, name)
    return os.path.join(os.path.dirname(__file__), name)


class GomokuGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("五子棋")
        self.load_buttons()
        self.reset_game()
        self.clock = pygame.time.Clock()
    
    def load_buttons(self):
        self.btn_imgs = {}
        btn_dir = get_resource_path('resources/buttons')
        for name in ['btn_pvp', 'btn_pve', 'btn_exit', 'btn_restart', 'btn_undo', 'btn_menu', 'btn_ok']:
            path = os.path.join(btn_dir, f'{name}.png')
            if os.path.exists(path):
                try:
                    img = Image.open(path).convert('RGBA')
                    raw = img.tobytes('raw', 'RGBA')
                    self.btn_imgs[name] = pygame.image.fromstring(raw, img.size, 'RGBA').convert_alpha()
                except Exception as e:
                    print(f"加载 {name} 失败：{e}")
    
    def reset_game(self):
        self.state = 'menu'
        self.mode = 'pvp'
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.current_player = 1
        self.move_history = []
        self.game_over = False
        self.winner = None
        self.last_move = None
        
        self.buttons = {
            'pvp': pygame.Rect(300, 250, 200, 60),
            'pve': pygame.Rect(300, 320, 200, 60),
            'exit': pygame.Rect(300, 400, 200, 60),
            'restart': pygame.Rect(180, 640, 100, 40),
            'undo': pygame.Rect(300, 640, 100, 40),
            'menu': pygame.Rect(420, 640, 100, 40),
            'ok': pygame.Rect(350, 450, 100, 50),
        }
    
    def draw_button(self, key, hover=False):
        rect = self.buttons[key]
        img = self.btn_imgs.get(f'btn_{key}')
        if img:
            img_scaled = pygame.transform.smoothscale(img, (rect.width, rect.height))
            if hover:
                img_scaled = img_scaled.copy()
                img_scaled.fill((255, 255, 255, 50), special_flags=pygame.BLEND_RGBA_ADD)
            self.screen.blit(img_scaled, rect)
        else:
            color = (100, 160, 200) if hover else (70, 130, 180)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, COLOR_WHITE, rect, 2, border_radius=10)
    
    def draw_menu(self):
        self.screen.fill(COLOR_BG)
        # 标题
        for i in range(5):
            pygame.draw.line(self.screen, COLOR_BLACK, (310+i*40, 70), (310+i*40, 110), 2)
            pygame.draw.line(self.screen, COLOR_BLACK, (310, 70+i*40), (490, 70+i*40), 2)
        
        mouse_pos = pygame.mouse.get_pos()
        for key in ['pvp', 'pve', 'exit']:
            self.draw_button(key, self.buttons[key].collidepoint(mouse_pos))
    
    def draw_board(self):
        self.screen.fill(COLOR_BG)
        
        # 棋盘
        for i in range(GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_LINE, (MARGIN, MARGIN+i*CELL_SIZE), (MARGIN+BOARD_SIZE, MARGIN+i*CELL_SIZE), 2)
            pygame.draw.line(self.screen, COLOR_LINE, (MARGIN+i*CELL_SIZE, MARGIN), (MARGIN+i*CELL_SIZE, MARGIN+BOARD_SIZE), 2)
        
        # 棋子
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c]:
                    x, y = MARGIN + c*CELL_SIZE, MARGIN + r*CELL_SIZE
                    color = COLOR_BLACK if self.board[r][c] == 1 else COLOR_WHITE
                    pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE//2 - 2)
        
        # 最后一步
        if self.last_move:
            pygame.draw.circle(self.screen, COLOR_RED, (MARGIN+self.last_move[1]*CELL_SIZE, MARGIN+self.last_move[0]*CELL_SIZE), 5)
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        for key in ['restart', 'undo', 'menu']:
            self.draw_button(key, self.buttons[key].collidepoint(mouse_pos))
        
        # 当前玩家
        ind = COLOR_BLACK if self.current_player == 1 else COLOR_WHITE
        pygame.draw.circle(self.screen, ind, (400, 25), 15)
        pygame.draw.circle(self.screen, COLOR_RED, (400, 25), 15, 2)
    
    def draw_game_over(self):
        self.draw_board()
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        win = COLOR_BLACK if self.winner == 1 else COLOR_WHITE
        pygame.draw.circle(self.screen, win, (400, 320), 50)
        pygame.draw.circle(self.screen, COLOR_RED, (400, 320), 50, 5)
        
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button('ok', self.buttons['ok'].collidepoint(mouse_pos))
    
    def handle_click(self, pos):
        if self.state == 'menu':
            if self.buttons['pvp'].collidepoint(pos):
                self.reset_game()
                self.mode = 'pvp'
                self.state = 'playing'
            elif self.buttons['pve'].collidepoint(pos):
                self.reset_game()
                self.mode = 'pve'
                self.state = 'playing'
            elif self.buttons['exit'].collidepoint(pos):
                return False
        elif self.state == 'playing':
            if self.buttons['restart'].collidepoint(pos):
                self.reset_game()
            elif self.buttons['undo'].collidepoint(pos):
                self.undo()
            elif self.buttons['menu'].collidepoint(pos):
                self.state = 'menu'
            else:
                self.board_click(pos)
        elif self.state == 'gameover':
            if self.buttons['ok'].collidepoint(pos):
                self.state = 'menu'
        return True
    
    def board_click(self, pos):
        if self.game_over:
            return
        x, y = pos
        if x < MARGIN or x > MARGIN+BOARD_SIZE or y < MARGIN or y > MARGIN+BOARD_SIZE:
            return
        c = (x - MARGIN + CELL_SIZE//2) // CELL_SIZE
        r = (y - MARGIN + CELL_SIZE//2) // CELL_SIZE
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == 0:
            self.make_move(r, c)
    
    def make_move(self, r, c):
        self.board[r][c] = self.current_player
        self.move_history.append((r, c))
        self.last_move = (r, c)
        
        if self.check_win(r, c):
            self.game_over = True
            self.winner = self.current_player
            self.state = 'gameover'
        else:
            self.current_player = 3 - self.current_player
            if self.mode == 'pve' and self.current_player == 2:
                pygame.time.wait(300)
                self.ai_move()
    
    def ai_move(self):
        # 简单 AI：优先中心，然后随机
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.board[r][c] == 0]
        if not empty:
            return
        
        # 如果有棋子，优先下在附近
        if self.move_history:
            last_r, last_c = self.move_history[-1]
            near = [(r, c) for r, c in empty if abs(r-last_r) <= 2 and abs(c-last_c) <= 2]
            if near:
                empty = near
        
        r, c = random.choice(empty)
        self.make_move(r, c)
    
    def undo(self):
        if self.move_history and not self.game_over:
            r, c = self.move_history.pop()
            self.board[r][c] = 0
            self.current_player = 3 - self.current_player
            self.last_move = self.move_history[-1] if self.move_history else None
    
    def check_win(self, r, c):
        p = self.board[r][c]
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            cnt = 1
            nr, nc = r+dr, c+dc
            while 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.board[nr][nc] == p:
                cnt += 1
                nr += dr
                nc += dc
            nr, nc = r-dr, c-dc
            while 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.board[nr][nc] == p:
                cnt += 1
                nr -= dr
                nc -= dc
            if cnt >= 5:
                return True
        return False
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    running = self.handle_click(event.pos)
            
            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'playing':
                self.draw_board()
            elif self.state == 'gameover':
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        GomokuGame().run()
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()
