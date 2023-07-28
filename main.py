import mouse
import time
import ctypes
import pyautogui
import keyboard
import math

# TODO: make a stop button for the program | thread might be the answer
# DONE:
# instead of making a timer count make sure that it will know where the needle is and how long its going to take
# make sure it's in the right location.
# instead of needing to receive a character it should receive a keystrokes
# solving the problem with the refresh button that sometimes moves

# screen boundaries
TopLeftSecondScreen = (-1920, 418)
BottomRightSecondScreen = (-1, 1497)

# tapping the web so the program will be able to do the functions in the web page
FirstTapToStartMakingActions = (-72, round((TopLeftSecondScreen[1] + BottomRightSecondScreen[1]) / 2))

# favorites bar location
FavoritesBar = (-55, 505)
# favorites bar color
FavoritesBarColor = (125, 126, 130)


# if the search bar moved we need to add this amount to the x-axis
IfMoved = 42


# the location of the start button (green)
GreenButtonColor = (149, 204, 0)
# the location of the starting point for the checker
TopStart = (-725, 876)
# the location of the ending point for the checker
BottomEnd = (TopStart[0], 1100)

# the biggest diff I allow to colors to have
ColorsDiff = 1000

# the circle locations
TopCircle = (-868, 1060)
BottomCircle = (-868, 1246)

CenterCircle = (-868, TopCircle[1] + round((BottomCircle[1] - TopCircle[1]) / 2))

RightSideCircle = (-960, round((BottomCircle[1] + TopCircle[1]) / 2))
LeftSideCircle = (-775, round((BottomCircle[1] + TopCircle[1]) / 2))

Radius = CenterCircle[1] - TopCircle[1]

Timer = 30

# circle full color
FullCircleColor = (149, 204, 0)
# circle hollow color
HollowCircleColor = (122, 122, 122)

# the locations of the button that asks if you want to continue from the place you left off
ContinueButton = (-1081, 671)

# the color of the button that continues from the place left off
ContinueButtonColor = (149, 204, 0)

# the color of the show before it starts
BlackColor = (0, 0, 0)


def get_pos():
    return mouse.get_position()


def move_mouse(pos):
    # move
    mouse.move(pos[0], pos[1], absolute=True, duration=0.0)


def mouse_click():
    mouse.click('left')


def double_click():
    mouse_click()
    time.sleep(0.1)
    mouse_click()


def mouse_click_with_position(pos):
    move_mouse(pos)
    mouse_click()


def get_pixel_rgb(pos):
    gdi32 = ctypes.windll.gdi32
    user32 = ctypes.windll.user32
    hdc = user32.GetDC(None)
    pixel = gdi32.GetPixel(hdc, pos[0], pos[1])
    r = pixel & 0xFF
    g = (pixel >> 8) & 0xFF
    b = (pixel >> 16) & 0xFF
    user32.ReleaseDC(None, hdc)
    return r, g, b


def color_dist(c1, c2):
    return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2


def check_for_favorites():
    if not get_pixel_rgb(FavoritesBar) == FavoritesBarColor:
        keyboard.press_and_release('ctrl + shift + b')


def screen_right_location():
    mouse_click_with_position(FirstTapToStartMakingActions)
    pyautogui.press('home')
    mouse.wheel(-7)


def check_key_pressed():
    if keyboard.is_pressed('s') or keyboard.is_pressed('S'):
        return True
    elif keyboard.is_pressed('e') or keyboard.is_pressed('E'):
        return None
    return False


def time_checker():
    # angle = 1
    # while angle < 360:
    #     start_from_y_axis = 90
    #     angle_radians = math.radians(angle + start_from_y_axis)
    #
    #     point = (round(CenterCircle[0] + Radius * math.cos(angle_radians)),
    #              round(CenterCircle[1] - Radius * math.sin(angle_radians)))
    #     move_mouse(point)
    #     if get_pixel_rgb(point) == FullCircleColor:
    #         print(angle)
    #         chase_me(angle)
    #         return 0
    #         # return angle * Timer / 360
    #     angle += 1

    while True:
        cut_degree_counter = 0

        just_one_before = True
        angle = 180
        start_from_y_axis = 90

        angle_radians = math.radians(angle + start_from_y_axis)
        point = (round(CenterCircle[0] + Radius * math.cos(angle_radians)),
                 round(CenterCircle[1] - Radius * math.sin(angle_radians)))
        color = get_pixel_rgb(point)

        if color == FullCircleColor and not just_one_before:
            return angle * Timer / 360

        elif color == FullCircleColor:
            angle /= 2

        else:
            angle *= 1.5
            just_one_before = False

        cut_degree_counter += 1
        just_one_before = True
        print(just_one_before)


def chase_me(angle):
    start_from_y_axis = 90

    while angle > 1:
        angle_radians = math.radians(angle + start_from_y_axis)

        point = (round(CenterCircle[0] + Radius * math.cos(angle_radians)),
                 round(CenterCircle[1] - Radius * math.sin(angle_radians)))
        move_mouse(point)
        angle -= 1
        time.sleep(0.0824)


# while 1:
#     if mouse.is_pressed("left"):
#         print(get_pos())
#         print(get_pixel_rgb(get_pos()))
#         time.sleep(0.2)
#


Question = "Proceed (Y/n)?"

equal_color = False

refreshed = False
emergency = False

while True:
    if check_key_pressed():
        screen_right_location()
        check_for_favorites()

        while not equal_color:
            if emergency:
                emergency = False
                break

            # time.sleep(2)
            move_mouse(TopCircle)

            if not refreshed:
                if get_pixel_rgb(TopCircle) == FullCircleColor:
                    wait_time = time_checker()
                    print(f"Time to wait: {wait_time is None}")
                    time.sleep(wait_time)

            for i in range(BottomEnd[1] - TopStart[1]):
                browser_color = get_pixel_rgb((TopStart[0], TopStart[1] + i))
                # move_mouse((TopStart[0], TopStart[1] + i))

                if color_dist(browser_color, GreenButtonColor) < ColorsDiff:
                    mouse_click()
                    current_position = get_pos()

                    time.sleep(1)
                    if get_pixel_rgb(ContinueButton) == ContinueButtonColor:
                        mouse_click_with_position(ContinueButton)

                    while not color_dist(get_pixel_rgb(current_position), BlackColor) < ColorsDiff:
                        current_position = (current_position[0], current_position[1] + 1)
                    move_mouse((current_position[0], current_position[1] + 20))
                    time.sleep(2)
                    double_click()
                    time.sleep(1)
                    # mouse_click()
                    exit()

            if not equal_color:
                keyboard.press_and_release('ctrl + r')
                i = 30
                while i:
                    i -= 1
                    time.sleep(1)
                    result = check_key_pressed()
                    if result is None:
                        emergency = True
                        break
