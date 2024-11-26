import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}

def check_bound(rect):
    """
    rectが画面内か画面外かを判定する関数
    引数: rect - こうかとんRect or 爆弾Rect
    戻り値: 横方向・縦方向の真理値タプル (True: 画面内/False:画面外)
    """
    x_bound = True if 0 <= rect.left and rect.right <= WIDTH else False
    y_bound = True if 0 <= rect.top and rect.bottom <= HEIGHT else False
    return x_bound, y_bound

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面上に「Game Over」と表示し、
    泣いているこうかとん画像を貼り付ける関数
    """
    gm_over = pg.Surface((WIDTH, HEIGHT))
    gm_over.set_alpha(200)
    gm_over.fill((0, 0, 0))
    screen.blit(gm_over, (0, 0))

    nn_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    nn_rct1 = nn_img.get_rect()
    nn_rct2 = nn_img.get_rect()
    nn_rct1.center = WIDTH // 3, HEIGHT // 2
    nn_rct2.center = (WIDTH // 3) * 2, HEIGHT // 2
    screen.blit(nn_img, nn_rct1)
    screen.blit(nn_img, nn_rct2)

    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す関数
    """
    bb_imgs = []
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
    return bb_imgs, accs


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    指定された移動量に基づいて画像を変換する関数。
    この関数は、指定された画像（"fig/3.png"）を読み込み、`sum_mv` で与えられる移動方向に応じて
    回転や反転を行った画像を返します。
    パラメータ:
        sum_mv (tuple[int, int]): 移動量を表す2次元ベクトル (x, y)。この値に基づいて画像の角度が決まります。
    戻り値:
        pg.Surface: 変換後の画像オブジェクト。
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    if (0 <= sum_mv[0]):
        kk_img = pg.transform.flip(kk_img,True,False)
        angle ={
            (0, -5): 90,
            (-5, 0): 0,
            (0, 5): 90,
            (5,-5):45,
            (5,0):0,
            (5, 5): -45,
        }
        angle = angle[sum_mv]
    else:
        angle = {
        (-5, -5): -45,
        (-5, 0): 0,
        (-5, 5): 45,
        }
        angle = angle[sum_mv]
    kk_img = pg.transform.rotozoom(kk_img, angle, 0.9)
    return kk_img
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが外に出ないように
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = get_kk_img(tuple(sum_mv))

        # 爆弾の移動と拡大・加速
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
