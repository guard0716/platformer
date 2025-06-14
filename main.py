import pyxel
import random

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320

class Platformer:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ひなころじゃんぷ")
        pyxel.load("my_resource.pyxres")

        # 主人公の状態
        self.player_x = 72
        self.player_y = 236
        self.player_vy = 0
        self.player_on_ground = False
        self.player_direction = 0
        # 足場リスト（x, y, width, height, vx）
        self.platforms = [
            [64, 310, 32, 4, 1],  # vx: 左右の移動速度
            [32, 260, 32, 4, -1],
            [96, 210, 32, 4, 1],
            [16, 160, 32, 4, -1],
            [80, 110, 32, 4, 1],
            [48, 60, 32, 4, -1]
        ]
        self.scroll_y = 0
        self.highest_platform_y = 60
        self.game_state = "PLAYING"
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_state != "PLAYING":
            if pyxel.btnp(pyxel.KEY_SPACE):
                # リスタート
                self.player_x = 72
                self.player_y = 236
                self.player_vy = 0
                self.scroll_y = 0
                self.game_state = "PLAYING"
                self.platforms = [
                    [64, 310, 32, 4, 1],
                    [32, 260, 32, 4, -1],
                    [96, 210, 32, 4, 1],
                    [16, 160, 32, 4, -1],
                    [80, 110, 32, 4, 1],
                    [48, 60, 32, 4, -1]
                ]
                self.highest_platform_y = 60
            return

        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 0:
            self.player_x -= 2
            self.player_direction = 1
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < 256:
            self.player_x += 2
            self.player_direction = 0

        # ジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE) and self.player_on_ground:
            self.player_vy = -6
            self.player_on_ground = False

        # 重力と垂直移動
        self.player_vy += 0.2
        self.player_y += self.player_vy

        # 足場との衝突判定
        self.player_on_ground = False
        for plat in self.platforms:
            px, py, pw, ph, vx = plat
            if (self.player_x + 40 > px and (self.player_x + 20) < px + pw and
                self.player_y + 60 > py and self.player_y + 60 < py + ph + 5 and
                self.player_vy > 0):
                self.player_y = py - 60
                self.player_vy = 0
                self.player_on_ground = True
                # 足場の移動に追従（着地時のみ）
                self.player_x += vx

        # 足場の左右移動
        for plat in self.platforms:
            px, py, pw, ph, vx = plat
            plat[0] += vx  # x座標を更新
            # 画面端で反転
            if plat[0] <= 0 or plat[0] + pw >= SCREEN_WIDTH:
                plat[4] = -vx

        # スクロール処理
        if self.player_y < 120:
            scroll_amount = (120 - self.player_y) * 0.2
            self.scroll_y += scroll_amount
            self.player_y += scroll_amount
            for plat in self.platforms:
                plat[1] += scroll_amount
            self.highest_platform_y += scroll_amount

        # 新しい足場生成
        if self.highest_platform_y > -900 and self.highest_platform_y < 1080:
            new_x = random.randint(0, 128)
            new_y = self.highest_platform_y - 50
            new_vx = random.choice([1, -1])  # ランダムな初期速度
            self.platforms.append([new_x, new_y, 32, 4, new_vx])
            self.highest_platform_y = new_y

        # 古い足場の削除
        self.platforms = [plat for plat in self.platforms if plat[1] < SCREEN_HEIGHT + self.scroll_y]

        # ゲームオーバー判定
        if self.player_y > 350:
            self.game_state = "GAME_OVER"

        # ゴール判定
        if self.scroll_y >= 1000:
            self.game_state = "CLEARED"

    def draw(self):
        pyxel.cls(0)

        if self.game_state == "GAME_OVER":
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "Game Over\nPress SPACE", 7)
            return
        elif self.game_state == "CLEARED":
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "Goal!\nPress SPACE", 7)
            return

        # 足場描画
        for plat in self.platforms:
            screen_y = plat[1]
            if 0 <= screen_y <= SCREEN_HEIGHT:
                pyxel.rect(plat[0], plat[1], plat[2], plat[3], 8)

        # 主人公描画
        if self.player_direction == 1:
            pyxel.blt(self.player_x, self.player_y, 1, 0, 0, 64, 64, pyxel.COLOR_BLACK)
        elif self.player_direction == 0:
            pyxel.blt(self.player_x, self.player_y, 1, 0, 64, 64, 64, pyxel.COLOR_BLACK)
        #pyxel.rect(self.player_x, self.player_y, 16, 16, 9)

        # 操作説明とデバッグ情報
        pyxel.text(10, 10, f"Arrow: Move, SPACE: Jump\nY: {self.player_y:.1f}\nScrollY: {self.scroll_y:.1f}", 7)

if __name__ == "__main__":
    Platformer()