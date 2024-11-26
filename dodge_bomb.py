import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}


def check_bound(rct):
    """
    引数：こうかとんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    gm_over = pg.Surface((WIDTH,HEIGHT))
    gm_over.set_alpha(200)
    gm_over.fill((0,0,0))
    screen.blit(gm_over, (0, 0))

    nn_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    nn_rct1 = nn_img.get_rect()
    nn_rct2 = nn_img.get_rect()
    nn_rct1.center = WIDTH // 3, HEIGHT // 2
    nn_rct2.center = (WIDTH //3)*2, HEIGHT // 2
    screen.blit(nn_img, nn_rct1)
    screen.blit(nn_img, nn_rct2)

    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = 5,5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        #衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        kk_rct.move_ip(sum_mv)
        #こうかとんが外に出ないように
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        #爆弾の移動
        bb_rct.move_ip(vx,vy)
        yoko,tate = check_bound(bb_rct)
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
