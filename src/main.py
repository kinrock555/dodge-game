import pygame
import sys
import random
from pathlib import Path  # 追加：パス操作用

# --- ベースディレクトリ設定（main.py の場所からの相対パス用） ---
BASE_DIR = Path(__file__).resolve().parent        # .../dodge-game/src
ASSETS_DIR = BASE_DIR.parent / "assets" / "images"  # .../dodge-game/assets/images

# --- Pygameの初期化 ---
pygame.init()

# --- 画面設定 ---
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game - Simple Version")

# --- フレーム管理 ---
CLOCK = pygame.time.Clock()
FPS = 60  # 1秒あたりのフレーム数

# --- フォント設定（ゲームオーバー表示用） ---
FONT_BIG = pygame.font.SysFont(None, 80)    # 大きい文字
FONT_SMALL = pygame.font.SysFont(None, 40)  # 説明用

# --- 背景画像の読み込み ---
background_image_path = ASSETS_DIR / "background.png"
background_image = pygame.image.load(background_image_path.as_posix()).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# 背景スクロール用の変数
BG_SCROLL_SPEED = 2   # 背景が流れる速さ（お好みで調整）
bg_y1 = 0             # 1枚目のY座標
bg_y2 = -HEIGHT       # 2枚目のY座標（画面の上にもう1枚）

# --- プレイヤー設定 ---
PLAYER_SIZE = 100
PLAYER_SPEED = 7

# プレイヤー画像の読み込み
player_image_path = ASSETS_DIR / "Player.png"
player_image = pygame.image.load(player_image_path.as_posix()).convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# プレイヤーの Rect
player_rect = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE // 2,
    HEIGHT - PLAYER_SIZE - 20,
    PLAYER_SIZE,
    PLAYER_SIZE
)

# --- 敵の設定 ---
ENEMY_SIZE = 150
enemy_speed = 13

# 敵画像の読み込み
enemy_image_path = ASSETS_DIR / "Enemy.png"
enemy_image = pygame.image.load(enemy_image_path.as_posix()).convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))

# 敵の Rect
enemy_rect = pygame.Rect(
    random.randint(0, WIDTH - ENEMY_SIZE),
    -ENEMY_SIZE,
    ENEMY_SIZE,
    ENEMY_SIZE
)

# --- ゲーム状態 ---
game_over = False

# ★ 生存時間用の変数 ---
#   start_time: ゲーム開始（またはリトライ）した瞬間の時刻（ミリ秒）
#   survival_time: ゲームオーバーまでに生き残った秒数
start_time = pygame.time.get_ticks()
survival_time = 0.0


def reset_game():
    """ゲームを初期状態に戻す"""
    global game_over, player_rect, enemy_rect, bg_y1, bg_y2
    global start_time, survival_time

    game_over = False

    # プレイヤー初期位置
    player_rect.x = WIDTH // 2 - PLAYER_SIZE // 2
    player_rect.y = HEIGHT - PLAYER_SIZE - 20

    # 敵を上から再スタート
    enemy_rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
    enemy_rect.y = -ENEMY_SIZE

    # 背景位置もリセット
    bg_y1 = 0
    bg_y2 = -HEIGHT

    # ★ 生存時間のリセット＆開始時刻を記録
    start_time = pygame.time.get_ticks()
    survival_time = 0.0


# === メインループ ===
while True:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ゲームオーバー中のキー操作
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                reset_game()

    # --- プレイ中の処理 ---
    if not game_over:

        # キー入力
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player_rect.y += PLAYER_SPEED

        # 画面外に出ないように補正
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > HEIGHT:
            player_rect.bottom = HEIGHT

        # 敵の落下
        enemy_rect.y += enemy_speed

        # 敵が下に落ちきったらリセット
        if enemy_rect.top > HEIGHT:
            enemy_rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy_rect.y = -ENEMY_SIZE

        # 当たり判定
        if enemy_rect.colliderect(player_rect):
            # ★ ゲームオーバーになった瞬間に生存時間を計算
            game_over = True
            # ミリ秒 → 秒 に変換（小数点2桁くらい）
            elapsed_ms = pygame.time.get_ticks() - start_time
            survival_time = elapsed_ms / 1000.0

        # ★ 背景スクロール更新（プレイ中のみ）
        bg_y1 += BG_SCROLL_SPEED
        bg_y2 += BG_SCROLL_SPEED

        # 画面の下に出きった背景を上に戻す
        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

    # --- 描画 ---
    if game_over:
        # ゲームオーバー時は、今までどおり暗い背景でもOK
        SCREEN.fill((50, 0, 0))

        text_gameover = FONT_BIG.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_gameover.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        SCREEN.blit(text_gameover, text_rect)

        # ★ 生存時間の表示
        # 例）"Survival Time: 8.32 sec"
        time_text = FONT_SMALL.render(
            f"Survival Time: {survival_time:.2f} sec", True, (255, 255, 0)
        )
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(time_text, time_rect)

        # 操作説明
        text_info = FONT_SMALL.render("Press R to Retry / ESC to Quit", True, (255, 255, 255))
        info_rect = text_info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        SCREEN.blit(text_info, info_rect)

    else:
        # ★ スクロールする背景を2枚描画
        SCREEN.blit(background_image, (0, bg_y1))
        SCREEN.blit(background_image, (0, bg_y2))

        # プレイヤー & 敵
        SCREEN.blit(player_image, player_rect)
        SCREEN.blit(enemy_image, enemy_rect)

    pygame.display.flip()
