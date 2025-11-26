import pygame
import sys
import random

# --- Pygameの初期化 ---
pygame.init()

# --- 画面設定 ---
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game - Simple Version")

# --- フレーム管理 ---
CLOCK = pygame.time.Clock()
FPS = 60  # 1秒あたりのフレーム数

# --- プレイヤー設定 ---
PLAYER_SIZE = 50
PLAYER_COLOR = (50, 200, 50)
PLAYER_SPEED = 7

# プレイヤーの Rect（位置と大きさ）
player_rect = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE // 2,   # X：画面中央
    HEIGHT - PLAYER_SIZE - 20,       # Y：画面下から少し上
    PLAYER_SIZE,                     # 幅
    PLAYER_SIZE                      # 高さ
)

# --- 敵の設定（1体） ---
ENEMY_SIZE = 40
ENEMY_COLOR = (200, 50, 50)

# 敵の Rect（Xはランダム、Yは画面上の外）
enemy_rect = pygame.Rect(
    random.randint(0, WIDTH - ENEMY_SIZE),  # X：0〜(WIDTH-ENEMY_SIZE)のランダム
    -ENEMY_SIZE,                            # Y：画面の上の外側
    ENEMY_SIZE,
    ENEMY_SIZE
)
enemy_speed = 5  # 下に落ちるスピード（ピクセル/フレーム）

# --- ゲーム状態 ---
game_over = False  # False：プレイ中 / True：ゲームオーバー


# === メインループ ===
while True:
    # FPSに合わせてループ速度を調整
    CLOCK.tick(FPS)

    # --- イベント処理（×ボタンで終了） ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # プレイ中だけ、入力・移動・当たり判定を行う
    if not game_over:
        # --- キー入力（矢印キー） ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player_rect.y += PLAYER_SPEED

        # --- プレイヤーが画面外に出ないように制限 ---
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > HEIGHT:
            player_rect.bottom = HEIGHT

        # --- 敵の落下 ---
        enemy_rect.y += enemy_speed

        # 敵が画面の下まで落ちたら、上から再出現
        if enemy_rect.top > HEIGHT:
            enemy_rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy_rect.y = -ENEMY_SIZE

        # --- 当たり判定（勝敗判定）---
        if enemy_rect.colliderect(player_rect):
            game_over = True  # 敵とぶつかったらゲームオーバー

    # --- 描画 ---
    # ゲームオーバー時は背景を少し赤っぽく
    if game_over:
        SCREEN.fill((50, 0, 0))
    else:
        SCREEN.fill((30, 30, 50))

    # プレイヤーと敵を描画
    pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect)
    pygame.draw.rect(SCREEN, ENEMY_COLOR, enemy_rect)

    # 画面更新
    pygame.display.flip()
##test
