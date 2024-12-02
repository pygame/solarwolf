import pygame
from pygame.locals import *
import game, gfx, snd
import random
import time

class GalagaGame:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = False
        self.first = True
        self.player_pos = [gfx.rect.centerx, gfx.rect.bottom - 50]
        self.player_dx = 0
        self.player_lives = 3
        self.score = 0
        self.player_bullets = []
        self.alien_bullets = []
        self.player_rect = None

        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.time_remaining = 15
        self.last_time = pygame.time.get_ticks()
        self.last_alien_shot_time = pygame.time.get_ticks()
        self.hud_width = 100  # HUD 가로 영역 크기
        self.game_width = gfx.rect.width - self.hud_width

        # 외계인 우주선 여러 개 생성 (랜덤화)
        self.alien_number = 10
        self.alien_x, self.alien_y, self.alien_dx, self.alien_dy = [], [], [], []
        self.alien_images = [gfx.load('enemy1.png'), gfx.load('enemy2.png'), gfx.load('enemy3.png')]
        self.alien_current_image = []

        # 외계인 초기 설정 (랜덤 위치, 속도, 이미지 선택)
        for _ in range(self.alien_number):
            self.alien_x.append(random.randint(50, gfx.rect.width - 50))  # 랜덤한 X 위치
            self.alien_y.append(random.randint(50, 150))  # 랜덤한 Y 위치
            self.alien_dx.append(random.uniform(0.05, 0.2))  # 랜덤한 속도
            self.alien_dy.append(0.0)  # Y 방향 속도
        self.alien_current_image = [random.choice(self.alien_images) for _ in range(self.alien_number)]

    def draw_hud(self):
        hud_x = self.game_width
        hud_rect = pygame.Rect(hud_x, 0, self.hud_width, gfx.rect.height)
        pygame.draw.rect(gfx.surface, (30, 30, 30), hud_rect)  # HUD 배경

        # 남은 시간 바 (세로 출력)
        bar_width = 20
        bar_height = gfx.rect.height - 100  # 최하단 요소를 위해 공간 확보
        bar_x = hud_x + 40
        bar_y = 10
        progress = max(0, self.time_remaining /15)
        pygame.draw.rect(gfx.surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(
            gfx.surface, 
            (0, 200, 0), 
            (bar_x, bar_y + (1 - progress) * bar_height, bar_width, progress * bar_height)
        )

        # 목숨 아이콘 (하단에 센터 정렬)
        ship_image = gfx.load('ship-mini-boost2.png')
        icon_width = ship_image.get_width()
        icon_spacing = 10
        total_width = self.player_lives * icon_width + (self.player_lives - 1) * icon_spacing
        start_x = hud_x + (self.hud_width - total_width) // 2
        for i in range(self.player_lives):
            gfx.surface.blit(ship_image, (start_x + i * (icon_width + icon_spacing), gfx.rect.height - 80))

        # 점수 (최하단 중앙)
        font_size = 16
        score_font = pygame.font.Font(None, font_size)
        score_text = score_font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(hud_x + self.hud_width // 2, gfx.rect.height - 40))
        gfx.surface.blit(score_text, score_rect)


    def update_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:  # 1초마다 감소
            self.time_remaining -= 1
            self.last_time = current_time
            if self.time_remaining <= 0:
                self.abort()

    def draw_player(self):
        ship_image = gfx.load('ship-up.png')
        self.player_rect = ship_image.get_rect(center=self.player_pos)
        gfx.surface.blit(ship_image, self.player_rect)
        gfx.dirty(self.player_rect)

    def draw_aliens(self):
        for i in range(self.alien_number):
            alien_image = self.alien_current_image[i]
            alien_rect = alien_image.get_rect(center=(self.alien_x[i], self.alien_y[i]))
            gfx.surface.blit(alien_image, alien_rect)
            gfx.dirty(alien_rect)

    def draw_status_bar(self):
        status_x = gfx.rect.width - 150  # 상태 표시줄의 X 위치
        y_spacing = 30  # 세로 간격
        gfx.surface.fill((30, 30, 30), (status_x, 0, 150, gfx.rect.height))  # 배경색

        # 상태 요소 렌더링
        elements = [
            f"Lives: {self.player_lives}",
            f"Score: {self.score}",
        ]
        for i, text in enumerate(elements):
            rendered_text = self.myfont.render(text, True, (255, 255, 255))
            gfx.surface.blit(rendered_text, (status_x + 10, i * y_spacing + 10))

    def update_player_position(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player_dx = -1
            elif event.key == pygame.K_RIGHT:
                self.player_dx = 1
            elif event.key == pygame.K_SPACE:
                self.fire_player_bullet()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.player_dx = 0

    def move_player(self):
        self.player_pos[0] += self.player_dx
        self.player_pos[0] = max(0, min(self.player_pos[0], gfx.rect.width))

    def fire_player_bullet(self):
        snd.play('shoot')
        bullet_frames = gfx.animstrip(gfx.load('fire.png'))
        bullet_x = self.player_pos[0]
        bullet_y = self.player_pos[1] - 20
        self.player_bullets.append({
            "frames": bullet_frames,
            "current_frame": 0,
            "x": bullet_x,
            "y": bullet_y,
            "dy": -1
        })

    def fire_alien_bullet(self, alien_index):
        bullet_x = self.alien_x[alien_index]
        bullet_y = self.alien_y[alien_index] + 20
        self.alien_bullets.append({
            "x": bullet_x,
            "y": bullet_y,
            "dy": 0.3,  # 느린 속도
            "image": gfx.animstrip(gfx.load('fire.png'))
        })

    def draw_bullets(self):
        for bullet in self.player_bullets:
            current_frame = bullet["frames"][bullet["current_frame"]]
            bullet_rect = current_frame.get_rect(center=(bullet["x"], bullet["y"]))
            gfx.surface.blit(current_frame, bullet_rect)
            gfx.dirty(bullet_rect)

    def draw_alien_bullets(self):
        for bullet in self.alien_bullets:
            current_frame = bullet["image"][0]  # 첫 번째 프레임을 가져옴
            bullet_rect = current_frame.get_rect(center=(bullet["x"], bullet["y"]))
            gfx.surface.blit(current_frame, bullet_rect)
            gfx.dirty(bullet_rect)

    def update_bullets(self):
        for bullet in self.player_bullets:
            bullet["y"] += bullet["dy"]
            bullet["current_frame"] = (bullet["current_frame"] + 1) % len(bullet["frames"])
            if bullet["y"] < 0:
                self.player_bullets.remove(bullet)
    
    def update_alien_bullets(self):
        for bullet in self.alien_bullets[:]:
            bullet["y"] += bullet["dy"]
            current_frame = bullet["image"][0]  # 첫 번째 프레임을 가져옴
            bullet_rect = current_frame.get_rect(center=(bullet["x"], bullet["y"]))

            # 플레이어와 충돌 체크
            if self.player_rect and bullet_rect.colliderect(self.player_rect):
                self.alien_bullets.remove(bullet)
                self.player_lives -= 1
                snd.play('explode')  # 충돌 효과음
                if self.player_lives <= 0:
                    self.abort()

            # 화면 밖으로 나간 총알 제거
            if bullet["y"] > gfx.rect.height:
                self.alien_bullets.remove(bullet)

    def check_collisions(self):
        for bullet in self.player_bullets:
            bullet_rect = pygame.Rect(bullet["frames"][bullet["current_frame"]].get_rect(center=(bullet["x"], bullet["y"])))
            for i in range(self.alien_number):
                alien_rect = pygame.Rect(self.alien_current_image[i].get_rect(center=(self.alien_x[i], self.alien_y[i])))
                if bullet_rect.colliderect(alien_rect):
                    self.player_bullets.remove(bullet)
                    self.score += 50
                    snd.play('chimein')
                    self.alien_x[i], self.alien_y[i] = random.randint(50, gfx.rect.width - 50), random.randint(50, 150)
                    self.alien_dx[i] *= random.choice([-1, 1])
                    self.alien_current_image[i] = random.choice(self.alien_images)  # 외계인 이미지 랜덤 변경
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.player_rect = None
                gfx.surface.fill((0, 0, 0))
                pygame.display.update()
                self.abort()
            self.update_player_position(event)

    def abort(self):
        snd.play('delete')
        self.done = True
        game.handler = self.prevhandler

    def move_aliens(self):
        for i in range(self.alien_number):
            self.alien_x[i] += self.alien_dx[i]
            if self.alien_x[i] <= 0 or self.alien_x[i] >= gfx.rect.width - self.alien_current_image[0].get_width():
                self.alien_dx[i] *= -1
                self.alien_y[i] += 30

    def handle_alien_bullets(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_alien_shot_time > 200:  # 0.2초마다 총알 발사
            self.last_alien_shot_time = current_time
            for i in range(self.alien_number):
                if random.random() < 0.8:  # 80% 확률로 외계인 총알 발사
                    alien_bullet_image = gfx.load('alien_bullet.png')
                    bullet_x = self.alien_x[i]
                    bullet_y = self.alien_y[i] + 20
                    bullet_rect = alien_bullet_image.get_rect(center=(bullet_x, bullet_y))
                    self.alien_bullets.append({
                        "image": alien_bullet_image,
                        "x": bullet_x,
                        "y": bullet_y,
                        "dy": 1
                    })
    
    def update_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:
            self.time_remaining -= 1
            self.last_time = current_time
            if self.time_remaining <= 0:
                self.abort()

        # 적의 총알 발사 타이밍 제어
        if current_time - self.last_alien_shot_time >= 200:  # 0.2초 간격
            alien_index = random.randint(0, self.alien_number - 1)
            self.fire_alien_bullet(alien_index)
            self.last_alien_shot_time = current_time

    def move_alien_bullets(self):
        for bullet in self.alien_bullets:
            bullet["y"] += bullet["dy"]
            if bullet["y"] > gfx.rect.height:
                self.alien_bullets.remove(bullet)

    def run(self):
        while not self.done:
            self.handle_events()
            self.move_player()
            self.move_aliens()
            self.update_bullets()
            self.update_alien_bullets()
            self.check_collisions()
            self.update_timer()

            gfx.surface.fill((0, 0, 0))
            self.draw_player()
            self.draw_aliens()
            self.draw_bullets()
            self.draw_alien_bullets()
            self.draw_hud()

            pygame.display.update()

        return game.handler
