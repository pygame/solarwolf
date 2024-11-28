import pygame
from pygame.locals import *
import game, gfx, math, txt
from pygame.font import Font

def render(score):
    #0일땐 출력하지 않게 함
    if score <= 0:
        # 기존 코드와 동일한 크기의 빈 Surface 생성
        empty_surface = pygame.Surface((30, 36))  # 크기는 적절히 조정 가능
        empty_surface.set_colorkey(0, RLEACCEL)
        return empty_surface
    
    # 한글 폰트 사용
    font = Font(txt.font_path, 20)  #--- 단계 폰트를 36에서 20로 변경 ---
    

    # '[숫자]단계' 형식으로 텍스트 생성
    level_text = f"단계 {score}"
    
    # 흰색으로 텍스트 렌더링
    text_surface = font.render(level_text, True, (255, 255, 255))
    
    # 투명한 배경을 위한 설정
    text_surface.set_colorkey(0, RLEACCEL)
    
    return text_surface

# 게임 리소스 로드 함수는 더 이상 필요없으므로 비워둡니다
def load_game_resources():
    pass