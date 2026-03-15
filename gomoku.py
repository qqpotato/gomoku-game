#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五子棋游戏 (Gomoku Game)
使用 Python + Pygame 开发
功能：双人对战、人机对战、悔棋、重新开始、退出
"""

import pygame
import sys
import math
import random
from enum import Enum
from typing import List, Tuple, Optional

# ==================== 常量定义 ====================
# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
GRID_SIZE = 15  # 15x15 棋盘
CELL_SIZE = 40  # 每个格子的大小
MARGIN = 60     # 棋盘边缘留白

# 棋盘绘制区域
BOARD_TOP = MARGIN
BOARD_LEFT = MARGIN
BOARD_SIZE = (GRID_SIZE - 1) * CELL_SIZE

# 颜色定义
COLOR_BACKGROUND = (220, 179, 130)  # 木纹色
COLOR_LINE = (0, 0, 0)               # 线条颜色
COLOR_BLACK = (0, 0, 0)              # 黑棋
COLOR_WHITE = (255, 255, 255)        # 白棋
COLOR_HIGHLIGHT = (255, 0, 0)        # 最后落子位置高亮
COLOR_BUTTON_BG = (70, 130, 180)     # 按钮背景色
COLOR_BUTTON_HOVER = (100, 160, 200) # 按钮悬停色
COLOR_TEXT = (255, 255, 255)         # 文字颜色

# 游戏状态
class GameState(Enum):
    MENU = 1        # 主菜单
    PLAYING = 2     # 游戏中
    GAME_OVER = 3   # 游戏结束

# 游戏模式
class GameMode(Enum):
    PVP = 1         # 双人对战
    PVE = 2         # 人机对战

# 棋子类型
class PieceType(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

# ==================== AI 引擎 ====================
class AIEngine:
    """简单的五子棋 AI，使用评分系统"""
    
    def __init__(self, board_size: int = 15):
        self.board_size = board_size
        # 不同棋型的评分
        self.score_map = {
            'FIVE': 100000,      # 五连
            'LIVE_FOUR': 10000,  # 活四
            'RUSH_FOUR': 1000,   # 冲四
            'LIVE_THREE': 1000,  # 活三
            'RUSH_THREE': 100,   # 冲三
            'LIVE_TWO': 100,     # 活二
            'RUSH_TWO': 10,      # 冲二
        }
    
    def evaluate_position(self, board: List[List[int]], row: int, col: int, 
                         player: int) -> int:
        """评估某个位置的分数"""
        if board[row][col] != PieceType.EMPTY.value:
            return 0
        
        # 临时落子
        board[row][col] = player
        score = self.evaluate_board(board, player)
        board[row][col] = PieceType.EMPTY.value
        
        return score
    
    def evaluate_board(self, board: List[List[int]], player: int) -> int:
        """评估整个棋盘的分数"""
        total_score = 0
        
        # 评估所有方向
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 横、竖、左斜、右斜
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == player:
                    for dr, dc in directions:
                        score = self.evaluate_line(board, row, col, dr, dc, player)
                        total_score += score
        
        return total_score
    
    def evaluate_line(self, board: List[List[int]], row: int, col: int, 
                     dr: int, dc: int, player: int) -> int:
        """评估一条线上的棋型"""
        # 统计连续棋子数
        count = 1
        left_open = True
        right_open = True
        
        # 向正方向统计
        r, c = row + dr, col + dc
        while 0 <= r < self.board_size and 0 <= c < self.board_size:
            if board[r][c] == player:
                count += 1
            elif board[r][c] == PieceType.EMPTY.value:
                break
            else:
                right_open = False
                break
            r += dr
            c += dc
        else:
            right_open = False
        
        # 向反方向统计
        r, c = row - dr, col - dc
        while 0 <= r < self.board_size and 0 <= c < self.board_size:
            if board[r][c] == player:
                count += 1
            elif board[r][c] == PieceType.EMPTY.value:
                break
            else:
                left_open = False
                break
            r -= dr
            c -= dc
        else:
            left_open = False
        
        # 根据棋型评分
        if count >= 5:
            return self.score_map['FIVE']
        elif count == 4:
            if left_open and right_open:
                return self.score_map['LIVE_FOUR']
            elif left_open or right_open:
                return self.score_map['RUSH_FOUR']
        elif count == 3:
            if left_open and right_open:
                return self.score_map['LIVE_THREE']
            elif left_open or right_open:
                return self.score_map['RUSH_THREE']
        elif count == 2:
            if left_open and right_open:
                return self.score_map['LIVE_TWO']
            elif left_open or right_open:
                return self.score_map['RUSH_TWO']
        
        return 0
    
    def get_best_move(self, board: List[List[int]], ai_player: int) -> Tuple[int, int]:
        """获取 AI 的最佳落子位置"""
        opponent = PieceType.WHITE.value if ai_player == PieceType.BLACK.value else PieceType.BLACK.value
        
        best_score = -float('inf')
        best_moves = []
        
        # 获取所有空位
        empty_positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == PieceType.EMPTY.value:
                    empty_positions.append((row, col))
        
        if not empty_positions:
            return (-1, -1)
        
        # 优先选择中心附近的空位（开局策略）
        center = self.board_size // 2
        if len(empty_positions) == self.board_size * self.board_size:
            return (center, center)
        
        # 评估每个空位
        for row, col in empty_positions:
            # 进攻分数
            attack_score = self.evaluate_position(board, row, col, ai_player)
            # 防守分数（阻止对手）
            defend_score = self.evaluate_position(board, row, col, opponent)
            
            # 综合评分（略微偏向进攻）
            score = attack_score + defend_score * 0.9
            
            # 位置加成（中心位置略优）
            distance_from_center = abs(row - center) + abs(col - center)
            score += (self.board_size - distance_from_center)
            
            if score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))
        
        # 从最佳位置中随机选择一个
        return random.choice(best_moves)


# ==================== 游戏主类 ====================
class GomokuGame:
    """五子棋游戏主类"""
    
    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        pygame.font.init()
        
        # 创建窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("五子棋 - Gomoku")
        
        # 加载中文字体 (macOS 系统字体)
        chinese_font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
        self.font_large = pygame.font.Font(chinese_font_path, 48)
        self.font_medium = pygame.font.Font(chinese_font_path, 36)
        self.font_small = pygame.font.Font(chinese_font_path, 24)
        
        # 游戏状态
        self.state = GameState.MENU
        self.mode = GameMode.PVP
        self.board: List[List[int]] = []
        self.current_player = PieceType.BLACK.value
        self.move_history: List[Tuple[int, int]] = []
        self.game_over = False
        self.winner: Optional[int] = None
        self.last_move: Optional[Tuple[int, int]] = None
        
        # AI 引擎
        self.ai = AIEngine()
        self.ai_player = PieceType.WHITE.value  # AI 执白
        
        # 按钮区域 - 调整位置避免遮挡棋盘
        # 棋盘底部位置：MARGIN + (GRID_SIZE-1)*CELL_SIZE = 60 + 14*40 = 620
        # 按钮放在棋盘下方区域
        self.buttons = {
            'pvp': pygame.Rect(300, 250, 200, 50),
            'pve': pygame.Rect(300, 320, 200, 50),
            'restart': pygame.Rect(180, 640, 100, 35),    # 左移，下移
            'undo': pygame.Rect(300, 640, 100, 35),       # 居中，下移
            'menu': pygame.Rect(420, 640, 100, 35),       # 右移，下移
            'exit': pygame.Rect(300, 600, 200, 50),
            'ok': pygame.Rect(350, 450, 100, 40),
        }
        
        # 时钟
        self.clock = pygame.time.Clock()
        
        # 初始化棋盘
        self.init_board()
    
    def init_board(self):
        """初始化棋盘"""
        self.board = [[PieceType.EMPTY.value for _ in range(GRID_SIZE)] 
                      for _ in range(GRID_SIZE)]
        self.current_player = PieceType.BLACK.value
        self.move_history = []
        self.game_over = False
        self.winner = None
        self.last_move = None
    
    def reset_game(self):
        """重置游戏"""
        self.init_board()
        self.state = GameState.PLAYING
    
    def place_piece(self, row: int, col: int) -> bool:
        """落子"""
        if self.game_over:
            return False
        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
            return False
        if self.board[row][col] != PieceType.EMPTY.value:
            return False
        
        # 落子
        self.board[row][col] = self.current_player
        self.move_history.append((row, col))
        self.last_move = (row, col)
        
        # 检查胜利
        if self.check_win(row, col, self.current_player):
            self.game_over = True
            self.winner = self.current_player
            return True
        
        # 检查平局
        if len(self.move_history) >= GRID_SIZE * GRID_SIZE:
            self.game_over = True
            self.winner = PieceType.EMPTY.value
            return True
        
        # 切换玩家
        self.current_player = (PieceType.WHITE.value if self.current_player == PieceType.BLACK.value 
                               else PieceType.BLACK.value)
        
        # 如果是人机模式且轮到 AI
        if (self.mode == GameMode.PVE and 
            self.current_player == self.ai_player and 
            not self.game_over):
            self.ai_move()
        
        return True
    
    def ai_move(self):
        """AI 落子"""
        row, col = self.ai.get_best_move(self.board, self.ai_player)
        if row >= 0 and col >= 0:
            self.place_piece(row, col)
    
    def undo(self):
        """悔棋"""
        if not self.move_history or self.game_over:
            return
        
        # 双人对战：悔一步；人机对战：悔两步（回到玩家回合）
        steps = 2 if self.mode == GameMode.PVE else 1
        
        for _ in range(steps):
            if not self.move_history:
                break
            row, col = self.move_history.pop()
            self.board[row][col] = PieceType.EMPTY.value
        
        if self.move_history:
            self.last_move = self.move_history[-1]
        else:
            self.last_move = None
        
        # 切换回当前玩家
        if self.mode == GameMode.PVE:
            self.current_player = PieceType.BLACK.value
        else:
            self.current_player = (PieceType.WHITE.value if len(self.move_history) % 2 == 0 
                                   else PieceType.BLACK.value)
    
    def check_win(self, row: int, col: int, player: int) -> bool:
        """检查是否获胜"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 横、竖、左斜、右斜
        
        for dr, dc in directions:
            count = 1
            
            # 正方向
            r, c = row + dr, col + dc
            while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if self.board[r][c] == player:
                    count += 1
                else:
                    break
                r += dr
                c += dc
            
            # 反方向
            r, c = row - dr, col - dc
            while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if self.board[r][c] == player:
                    count += 1
                else:
                    break
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False
    
    def get_grid_position(self, x: int, y: int) -> Tuple[int, int]:
        """将像素坐标转换为网格坐标"""
        col = round((x - BOARD_LEFT) / CELL_SIZE)
        row = round((y - BOARD_TOP) / CELL_SIZE)
        return row, col
    
    def draw_board(self):
        """绘制棋盘"""
        # 背景
        self.screen.fill(COLOR_BACKGROUND)
        
        # 绘制棋盘线条
        for i in range(GRID_SIZE):
            # 横线
            start_x = BOARD_LEFT
            end_x = BOARD_LEFT + BOARD_SIZE
            y = BOARD_TOP + i * CELL_SIZE
            pygame.draw.line(self.screen, COLOR_LINE, (start_x, y), (end_x, y), 1)
            
            # 竖线
            start_y = BOARD_TOP
            end_y = BOARD_TOP + BOARD_SIZE
            x = BOARD_LEFT + i * CELL_SIZE
            pygame.draw.line(self.screen, COLOR_LINE, (x, start_y), (x, end_y), 1)
        
        # 绘制天元和星位（15 路棋盘的星位在 3, 7, 11）
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7), 
                      (3, 7), (11, 7), (7, 3), (7, 11)]
        for row, col in star_points:
            x = BOARD_LEFT + col * CELL_SIZE
            y = BOARD_TOP + row * CELL_SIZE
            pygame.draw.circle(self.screen, COLOR_LINE, (x, y), 4)
        
        # 绘制棋子
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] != PieceType.EMPTY.value:
                    self.draw_piece(row, col, self.board[row][col])
        
        # 高亮最后落子位置
        if self.last_move:
            row, col = self.last_move
            x = BOARD_LEFT + col * CELL_SIZE
            y = BOARD_TOP + row * CELL_SIZE
            pygame.draw.circle(self.screen, COLOR_HIGHLIGHT, (x, y), 5, 2)
    
    def draw_piece(self, row: int, col: int, piece_type: int):
        """绘制棋子"""
        x = BOARD_LEFT + col * CELL_SIZE
        y = BOARD_TOP + row * CELL_SIZE
        radius = CELL_SIZE // 2 - 2
        
        if piece_type == PieceType.BLACK.value:
            # 黑棋（带渐变效果）
            pygame.draw.circle(self.screen, COLOR_BLACK, (x, y), radius)
            # 高光
            highlight_pos = (x - radius // 3, y - radius // 3)
            pygame.draw.circle(self.screen, (50, 50, 50), highlight_pos, radius // 4)
        else:
            # 白棋
            pygame.draw.circle(self.screen, COLOR_WHITE, (x, y), radius)
            pygame.draw.circle(self.screen, COLOR_LINE, (x, y), radius, 1)
            # 高光
            highlight_pos = (x - radius // 3, y - radius // 3)
            pygame.draw.circle(self.screen, (230, 230, 230), highlight_pos, radius // 4)
    
    def draw_menu(self):
        """绘制主菜单"""
        self.screen.fill(COLOR_BACKGROUND)
        
        # 标题
        title = self.font_large.render("五子棋", True, COLOR_LINE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_small.render("Gomoku Game", True, COLOR_LINE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 绘制按钮
        mouse_pos = pygame.mouse.get_pos()
        
        # 双人对战按钮
        pvp_color = COLOR_BUTTON_HOVER if self.buttons['pvp'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        pygame.draw.rect(self.screen, pvp_color, self.buttons['pvp'], border_radius=10)
        pvp_text = self.font_medium.render("双人对战", True, COLOR_TEXT)
        pvp_rect = pvp_text.get_rect(center=self.buttons['pvp'].center)
        self.screen.blit(pvp_text, pvp_rect)
        
        # 人机对战按钮
        pve_color = COLOR_BUTTON_HOVER if self.buttons['pve'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        pygame.draw.rect(self.screen, pve_color, self.buttons['pve'], border_radius=10)
        pve_text = self.font_medium.render("人机对战", True, COLOR_TEXT)
        pve_rect = pve_text.get_rect(center=self.buttons['pve'].center)
        self.screen.blit(pve_text, pve_rect)
        
        # 退出按钮
        exit_color = COLOR_BUTTON_HOVER if self.buttons['exit'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        pygame.draw.rect(self.screen, exit_color, self.buttons['exit'], border_radius=10)
        exit_text = self.font_medium.render("退出游戏", True, COLOR_TEXT)
        exit_rect = exit_text.get_rect(center=self.buttons['exit'].center)
        self.screen.blit(exit_text, exit_rect)
    
    def draw_game_ui(self):
        """绘制游戏界面 UI"""
        # 显示当前玩家
        player_text = "黑方回合" if self.current_player == PieceType.BLACK.value else "白方回合"
        if self.mode == GameMode.PVE and self.current_player == self.ai_player:
            player_text = "AI 思考中..."
        
        text = self.font_medium.render(player_text, True, COLOR_LINE)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 10))
        
        # 显示模式
        mode_text = "双人对战" if self.mode == GameMode.PVP else "人机对战"
        mode = self.font_small.render(f"模式：{mode_text}", True, COLOR_LINE)
        self.screen.blit(mode, (20, 10))
        
        # 按钮区域
        mouse_pos = pygame.mouse.get_pos()
        
        # 悔棋按钮
        undo_color = COLOR_BUTTON_HOVER if self.buttons['undo'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        if self.mode == GameMode.PVE:
            undo_color = (150, 150, 150)  # 人机模式下悔棋按钮灰色
        pygame.draw.rect(self.screen, undo_color, self.buttons['undo'], border_radius=8)
        undo_text = self.font_small.render("悔棋", True, COLOR_TEXT)
        undo_rect = undo_text.get_rect(center=self.buttons['undo'].center)
        self.screen.blit(undo_text, undo_rect)
        
        # 重新开始按钮
        restart_color = COLOR_BUTTON_HOVER if self.buttons['restart'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        pygame.draw.rect(self.screen, restart_color, self.buttons['restart'], border_radius=8)
        restart_text = self.font_small.render("重新开始", True, COLOR_TEXT)
        restart_rect = restart_text.get_rect(center=self.buttons['restart'].center)
        self.screen.blit(restart_text, restart_rect)
        
        # 返回菜单按钮
        menu_color = COLOR_BUTTON_HOVER if self.buttons['menu'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        pygame.draw.rect(self.screen, menu_color, self.buttons['menu'], border_radius=8)
        menu_text = self.font_small.render("返回菜单", True, COLOR_TEXT)
        menu_rect = menu_text.get_rect(center=self.buttons['menu'].center)
        self.screen.blit(menu_text, menu_rect)
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 结果显示
        if self.winner == PieceType.BLACK.value:
            result_text = "黑方获胜！"
        elif self.winner == PieceType.WHITE.value:
            result_text = "白方获胜！"
        else:
            result_text = "平局！"
        
        text = self.font_large.render(result_text, True, COLOR_TEXT)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 350))
        self.screen.blit(text, text_rect)
        
        # 确定按钮
        mouse_pos = pygame.mouse.get_pos()
        ok_color = COLOR_BUTTON_HOVER if self.buttons['ok'].collidepoint(mouse_pos) else COLOR_BUTTON_BG
        pygame.draw.rect(self.screen, ok_color, self.buttons['ok'], border_radius=10)
        ok_text = self.font_medium.render("确定", True, COLOR_TEXT)
        ok_rect = ok_text.get_rect(center=self.buttons['ok'].center)
        self.screen.blit(ok_text, ok_rect)
    
    def handle_menu_click(self, pos: Tuple[int, int]):
        """处理菜单点击"""
        if self.buttons['pvp'].collidepoint(pos):
            self.mode = GameMode.PVP
            self.reset_game()
        elif self.buttons['pve'].collidepoint(pos):
            self.mode = GameMode.PVE
            self.reset_game()
        elif self.buttons['exit'].collidepoint(pos):
            pygame.quit()
            sys.exit()
    
    def handle_game_click(self, pos: Tuple[int, int]):
        """处理游戏界面点击"""
        # 检查是否点击在棋盘上
        if (BOARD_LEFT <= pos[0] <= BOARD_LEFT + BOARD_SIZE and
            BOARD_TOP <= pos[1] <= BOARD_TOP + BOARD_SIZE):
            row, col = self.get_grid_position(pos[0], pos[1])
            self.place_piece(row, col)
        
        # 检查按钮点击
        if self.buttons['restart'].collidepoint(pos):
            self.reset_game()
        elif self.buttons['undo'].collidepoint(pos) and self.mode == GameMode.PVP:
            self.undo()
        elif self.buttons['menu'].collidepoint(pos):
            self.state = GameState.MENU
            self.init_board()
    
    def handle_game_over_click(self, pos: Tuple[int, int]):
        """处理游戏结束界面点击"""
        if self.buttons['ok'].collidepoint(pos):
            self.state = GameState.MENU
            self.init_board()
    
    def run(self):
        """游戏主循环"""
        running = True
        
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键
                        pos = pygame.mouse.get_pos()
                        if self.state == GameState.MENU:
                            self.handle_menu_click(pos)
                        elif self.state == GameState.PLAYING:
                            self.handle_game_click(pos)
                        elif self.state == GameState.GAME_OVER:
                            self.handle_game_over_click(pos)
            
            # 绘制
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_board()
                self.draw_game_ui()
                if self.game_over:
                    self.state = GameState.GAME_OVER
            elif self.state == GameState.GAME_OVER:
                self.draw_board()
                self.draw_game_ui()
                self.draw_game_over()
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


# ==================== 程序入口 ====================
if __name__ == "__main__":
    try:
        game = GomokuGame()
        game.run()
    except Exception as e:
        print(f"游戏运行出错：{e}")
        pygame.quit()
        sys.exit(1)
