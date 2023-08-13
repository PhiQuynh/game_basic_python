# thêm thư viện
import pygame
from pygame.locals import *
import pickle
from os import path
from pygame import mixer
#tần số = 44100, kích thước = -16, các kênh = 2, bộ đệm = 512,
pygame.mixer.pre_init(44100, -16, 2, 512)
#chạy nhạc
mixer.init()
# chạy chương trình
pygame.init()

# phông chữ và kích thước mặc định
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# thời gian nếu ko hoạt động sẽ tự thoát
clock = pygame.time.Clock()
fps = 60
# Chiều dài ,rộng màn hình game mặc định là 600 x 600
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
# tiêu đề game là NHÓM Ế
pygame.display.set_caption('NHÓM 6')

# Giá trị mặc định của mỗi ô trên màn hình
tile_size = 30
# Hàm chia hàng ,cột

# thêm ảnh mặt trời và mây
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')

# thêm ảnh nút restart
restart_img = pygame.image.load('img/restart_btn.png')

# thêm ảnh nút start,exit
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# nếu khác 0 thì nhân vật sống,-1 là nhân vật chết
game_over = 0

# cấp độ hiện tại và cấp độ tối đa
level = 1
max_levels = 7
# điểm
score = 0


# màu mặc định
white = (255, 255, 255)
blue = (0, 0, 255)

# menu ở trạng thái mở
main_menu = True

#thêm các bài nhạc âm lượng 0.5 khi bắt đầu ,nhặt vàng,nhảy,thua
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)


# Hàm hiện thị chữ


def draw_text(text, font, text_col, x, y):
    # hiện thị ra chữ ,màu chữ ,vị trí
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Hàm chơi lại cấp độ hiện tại


def reset_level(level):
    # cập nhật lại cấp độ 
    player.reset(50, screen_height - 100)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()

    # tải dữ liệu cấp và tạo màn hình dựa trên dữ liệu
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


# Lớp nút
class Button():
    # hình ảnh ,vị trí nút,trạng thái hoạt động có kích thước bằng ảnh
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        action = False

        # Lấy vị trí của chuột
        pos = pygame.mouse.get_pos()

        # kiểm tra điều kiện di chuột và ấn chuột
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # hiện nút ấn
        screen.blit(self.image, self.rect)

        return action

# lớp người dùng


class Player():
    # x,y là vị trí người dùng
    def __init__(self, x, y):
        self.reset(x, y)
    #     # hoạt ảnh đi sang trái,phải
    #     self.images_right = []
    #     self.images_left = []
    #     # vị trí ảnh hiện tại
    #     self.index = 0
    #     self.counter = 0
    #     for num in range(1, 5):
    #         # chèn các ảnh guy1,guy2,guy3,guy4 có kích thước 30 x 60
    #         img_right = pygame.image.load(f'img/guy{num}.png')
    #         img_right = pygame.transform.scale(img_right, (30, 60))

    #         # sang trái thực hiện ngược lại so với sang phải
    #         img_left = pygame.transform.flip(img_right, True, False)
    #         self.images_right.append(img_right)
    #         self.images_left.append(img_left)
    #     self.image = self.images_right[self.index]
    #     # hướng di chuyển 0 :đứng im hoặc nhảy ,1 sang phải,-1 sang trái
    #     self.direction = 0
    #     # hình ảnh nhân vật có kích thước là 30 x 80 (rộng 30 ,dài 60)
    #     # ở vị trị x,y (được truyền từ ngoài vào),mặc định là không nhảy
    #     img = pygame.image.load('img/guy1.png')
    #     self.image = pygame.transform.scale(img, (30, 60))
    #     self.rect = self.image.get_rect()
    #     self.rect.x = x
    #     self.rect.y = y
    #     # chiều dài,rộng của nhân vật
    #     self.width = self.image.get_width()
    #     self.height = self.image.get_height()

    #     self.vel_y = 0
    #     self.jumped = False
    #     # ảnh nhân vật khi chết
    #     self.dead_image = pygame.image.load('img/ghost.png')
    # # khi người dùng di chuyển nhân vật(nhảy ,sang trái ,sang phải)
    # hàm reset lại trạng thái ban đầu của nhân vật

    def reset(self, x, y):
        # hoạt ảnh đi sang trái,phải
        self.images_right = []
        self.images_left = []
        # vị trí ảnh hiện tại
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            # chèn các ảnh guy1,guy2,guy3,guy4 có kích thước 30 x 60
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 60))

            # sang trái thực hiện ngược lại so với sang phải
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        # hướng di chuyển 0 :đứng im hoặc nhảy ,1 sang phải,-1 sang trái
        self.direction = 0
        # hình ảnh nhân vật có kích thước là 30 x 80 (rộng 30 ,dài 60)
        # ở vị trị x,y (được truyền từ ngoài vào),mặc định là không nhảy
        img = pygame.image.load('img/guy1.png')
        self.image = pygame.transform.scale(img, (30, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # chiều dài,rộng của nhân vật
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.vel_y = 0
        self.jumped = False
        # ảnh nhân vật khi chết
        self.dead_image = pygame.image.load('img/ghost.png')
        # không cho nhảy 2 lần
        self.in_air = True

    def update(self, game_over):
        dx = 0
        dy = 0
        # thời gian hồi chiêu đi bộ(chuyển trang thái)
        walk_cooldown = 5
        # Khi ấn phím
        key = pygame.key.get_pressed()
        # nếu nhân vật còn sống
        if game_over == 0:
            # nếu ấn phím cách và nhân vật không trong trạng thái nhảu thì sẽ thực hiện nhảy ,và chuyển về trạng thái nhảy
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                #bật nhạc nhảy
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            # nếu người dùng bỏ tay khỏi phím cách thì sẽ chuyển về trạng thái chưa nhảy
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            # nếu người dùng ấn nút sang bên trái thì nhân vật sẽ di chuyển sang trái
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            # nếu người dùng ấn nút sang bên phải thì nhân vật sẽ di chuyển sang phải
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            # nếu người chơi ko ấn nút trái và phải thì nhân vật đứng im
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                # nếu người chơi ấn sang trái sẽ chuyển direction về 1 sẽ thực hiện các hoạt ảnh bên trái
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                # nếu người chơi ấn sang trái sẽ chuyển direction về -1 sẽ thực hiện các hoạt ảnh bên trái
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            # xử lý hoạt ảnh

            # nếu counter quá 5 thì sẽ bắt ảnh quay trở lại ảnh 1 và thực hiện tiếp việc di chuyển
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                # nếu người dùng vẫn hướng sang phải thì lặp lại chuyển động sang phải
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                # nếu người dùng vẫn hướng sang trái thì lặp lại chuyển động sang trái
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Thêm trong lực khi nhảy
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            self.in_air = True
            # Kiểm tra xem nhân vật có va chạm không
            for tile in world.tile_list:
                # Kiểm tra xem va chạm theo hướng x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Kiểm tra xem va chạm theo hướng y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # kiểm tra xem bên dưới mặt đất, tức là có nhảy không
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # kiểm tra xem trên mặt đất có rơi xuống không
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = -555
                        self.in_air = False
            # kiểm tra va chạm với quái không
            if pygame.sprite.spritecollide(self, blob_group, False):
                #bật nhạc thua
                game_over_fx.play()
                game_over = -1

            # kiểm tra va chạm với dung nham không
            if pygame.sprite.spritecollide(self, lava_group, False):
                #bật nhạc thua
                game_over_fx.play()
                game_over = -1
            # kiểm tra có qua màn không
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # cập nhật vị trí của nhân vật
            self.rect.x += dx
            self.rect.y += dy
            # không cho nhân vật vượt quá màn hình dưới
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0
        # nếu nhân vật chết
        elif game_over == -1:
            # Thì sẽ hiện thị ra chữ GAME OVER! kiểu Bauhaus 93 kích thước 70 ở vị trí 100 ,270
            draw_text('GAME OVER!', font, blue, 100, 270)
            # thì vẽ hiện chết ở vị trú hiện tại ở màn hình vị trí y= 200
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # in nhân vật lên màn hình
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over


def draw_grid():
    # chia thành 20 * 20 ô
    for line in range(0, 20):
        # chèn lên màn hình đường kẻ có màu (255, 255, 255)
        pygame.draw.line(screen, (255, 255, 255), (0, line *
                         tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line *
                         tile_size, 0), (line * tile_size, screen_height))


class World():
    def __init__(self, data):
        self.tile_list = []

        # Thêm ảnh đất và ảnh cỏ
        dirt_img = pygame.image.load('img/dirt.png')  # đất
        grass_img = pygame.image.load('img/grass.png')  # cỏ
        # chạy qua từng hàng và cột
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # nếu trong data là 1 thì hiện thị ảnh đất kích thước là 1 ô (30 x 30) và thêm vào danh sách để in ra màn hình
                if tile == 1:
                    img = pygame.transform.scale(
                        dirt_img, (tile_size , tile_size ))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # nếu trong data là 2 thì hiện thị ảnh cỏ có kích thước là 1 ô (30 x 30) và thêm vào danh sách để in ra màn hình
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (tile_size , tile_size ))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # nếu trong data là 3 thì sẽ hiện ra kẻ thù(quái) có chiều rộng là 45 ,cao 30
                if tile == 3:
                    blob = Enemy(col_count * tile_size,
                                 row_count * tile_size + 15)
                    blob_group.add(blob)
                # nếu trong data là 4 thì sẽ hiện ra dung nham có chiều cao là 30 ,rộng là 30+30//2
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count *
                                tile_size + (tile_size // 2))
                    lava_group.add(lava)
                   # nếu trong data là 5 thì sẽ hiện ra =tiền có chiều cao là 30 ,rộng là 30+30//2
                if tile == 5:
                    coin = Coin(col_count * tile_size + (tile_size // 2),
                                row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                 # nếu trong data là 6 thì sẽ hiện ra ô cửa qua màn có chiều cao là 30 ,rộng là 30+30//2
                if tile == 6:
                    exit = Exit(col_count * tile_size, row_count *
                                tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1
    # hàm cập nhật giá trị mặc định

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # ảnh quái ,vị trí ,tự động thay đổi di chuyển,tự động thực hiện lặp lại
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    # cập nhật lại hướng di chuyển ,tự động tăng giảm

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 0.5
        if abs(self.move_counter) > 5:
            self.move_direction *= -1
            self.move_counter *= -1
        # pygame.draw.rect(screen, (255,255,255), self.rect)

class Lava(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Hình ảnh ,kích thước ,vị trí dung nham
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Hình ảnh ,kích thước ,vị trí qua màn
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(
            img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Hình ảnh ,kích thước ,vị trí qua tiền vàng
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(
            img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# 1 là đất ,2 là cỏ ,còn lại là ô trống(do chưa code xong)
# sau khi code xong thì 1 là đất ,2 là cỏ ,0 là ô trống ,3 là quái 
# 4 là dung nham,5 là vàng ,6 là qua màn
# world_data = [
# [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1],
# [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 2, 2, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 5, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
# [1, 5, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 1],
# [1, 0, 2, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 2, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
# [1, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]
# quái
blob_group = pygame.sprite.Group()
# dung nham
lava_group = pygame.sprite.Group()
# qua màn
exit_group = pygame.sprite.Group()
# vàng
coin_group = pygame.sprite.Group()

# create dummy coin for showing the score
#tạo đồng xu giả để hiển thị điểm số
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# world = World(world_data)

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# người chơi ở vị trí x=50 ,y=600-100
player = Player(50, screen_height - 100)
# tạo nút chơi lại ở vị trí 225,200
restart_button = Button(225, 200, restart_img)
# tạo nút bắt đầu và nút thoát ở vị
start_button = Button(30, screen_height // 2, start_img)
exit_button = Button(330, screen_height // 2, exit_img)


# Lặp cho đến khi run =False
run = True
while run:
    # mỗi giây có nhiều nhất 60 khung hình sẽ trôi qua.
    clock.tick(fps)
    # chèn ảnh nền vào vị trí 0,0 và ảnh nền vào vị trí 100,100
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))
    # bắt đầu mở bảng menu
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        # chạy hàm dữ liệu
        world.draw()
        # chạy hàm chia bảng
        # draw_grid()
        # nếu nhân vật còn sống thì quái tự động chạy
        if game_over == 0:
            blob_group.update()
            # cập nhật số vàng
            # kiểm tra xem một đồng xu đã được thu thập
            if pygame.sprite.spritecollide(player, coin_group, True):
                #bật nhạc nhặt được tiền
                coin_fx.play()
                score += 5
            # hiện thị ra màn hình
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 5)
        # chạy hàm quái
        blob_group.draw(screen)
        # chạy hàm dung nham
        lava_group.draw(screen)
        # chạy hàm qua màn
        exit_group.draw(screen)
        # chạy hàm vàng
        coin_group.draw(screen)
        # chạy nhân vật
        game_over = player.update(game_over)
        # nếu thua sẽ hiện ra nút chơi lại
        if game_over == -1:
            # nếu ấn chơi lại thì nhân vật sẽ trở về trạng thái sống
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        # nếu người chơi đã hoàn thành cấp độ hiện tại
        if game_over == 1:
            # đặt lại trò chơi và chuyển sang cấp độ tiếp theo
            level += 1
            if level <= max_levels:
                # đạt lại cấp độ
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                # hiện thị ra chữ YOU WIN!
                draw_text('YOU WIN!', font, blue, 150, 270)

                if restart_button.draw():
                    level = 1
                    # đạt lại cấp độ
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
    # các phim ấn
    for event in pygame.event.get():
        # nếu ấn nút X sẽ dừng chương trình
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# hủy chương trình
pygame.quit()
