import pyautogui
import time
import random
import PIL
from fuzzy_match import fuzzy_images_match

time.sleep(2)

SYSTEM_STATE = {
    -1: "已掉线",
    0: "已暂停",
    1: "游戏运行中，准备排本",
    2: "副本队列中，等待确认",
    3: "已确认进入副本，等待赛鸟开始",
    4: "赛鸟进行中...",
    5: "赛鸟已结束，记录获得的金蝶币和经验",
    6: "已退出副本，准备下一轮赛鸟\n",
    7: "超时异常，重新判定状态",
}

state = 1
turn = 0
mingci_list = []
exp_list = []
jbd_list = []
img_list = [PIL.Image.open('digit%d.png' % i) for i in range(10)]


def my_click(x, y):
    pyautogui.moveTo(x, y, 0.5)
    pyautogui.mouseDown()
    pyautogui.mouseUp()


def recognize_digit(region):
    return fuzzy_images_match(pyautogui.screenshot(region=region), img_list)


def recognize_number(thousand_number_position):
    dx = thousand_number_position[0]
    dy = thousand_number_position[1]
    thousand_number = recognize_digit((dx, dy, 6, 18))
    hundred_number = recognize_digit((dx + 12, dy, 6, 18))
    tens_number = recognize_digit((dx + 20, dy, 6, 18))
    ones_number = recognize_digit((dx + 28, dy, 6, 18))
    return thousand_number * 1000 + hundred_number * 100 + tens_number * 10 + ones_number


def recognize_exp(landmark_position):
    # reward 801 475
    # [*1000 digit]exp 765 498
    dx = landmark_position[0] - 36
    dy = landmark_position[1] + 23
    return recognize_number((dx, dy))


def recognize_jdb(landmark_position):
    # reward 801 475
    # [*1000 digit]jdb 847 498
    dx = landmark_position[0] + 46
    dy = landmark_position[1] + 23
    return recognize_number((dx, dy))


def recognize_mingci(landmark_position):
    # bisaijieguo 1442 475
    # dibaming 1304 859
    # 228 203 55
    # di k ming 1304 859 - 32 * (8 - k) = 1304 603 + 32 k
    # diff = (-138, +128+32k)

    for i in range(1, 9):
        x = landmark_position[0] - 138
        y = landmark_position[1] + 128 + 32 * i
        if pyautogui.pixelMatchesColor(x, y, (228, 203, 55), tolerance=10):
            return i
    return None


def ready_to_queue():
    global state
    # 按U排本
    # 779 248 任务搜索器检测框左上角
    # 1107 377 金蝶游乐场按钮
    # 799 508 选中任务名称
    # 1140 830 选中参加
    offset_jindie = (1107-779, 377-248)
    offset_renwu = (799-779, 508-248)
    offset_canjia = (1140-779, 830-248)

    pyautogui.keyDown('u')
    time.sleep(random.random() / 10)
    pyautogui.keyUp('u')
    time.sleep(2)
    res = pyautogui.locateOnScreen("search3.png")
    if res is None:
        print("open searcher failed!")
        state = 1
        return
    else:
        x, y = res[0], res[1]
        my_click(x + offset_jindie[0], y + offset_jindie[1])
        if not pyautogui.pixelMatchesColor(x + offset_renwu[0], y + offset_renwu[1], (244, 206, 120)):
            my_click(x + offset_renwu[0], y + offset_renwu[1])
        my_click(x + offset_canjia[0], y + offset_canjia[1])
        state = 2
    # print(pyautogui.position())


def waiting_for_queue(timeout=100, interval=1):
    global state
    state_start_time = time.time()
    while True:
        res = pyautogui.locateOnScreen("search6.png")
        if res is not None:
            # 单击出发
            my_click(res[0], res[1])
            state = 3
            break
        elif time.time()-state_start_time > timeout:
            # 超时
            state = 7
            break
        else:
            time.sleep(interval)


def waiting_for_race_begin(timeout=100, interval=1):
    global state
    state_start_time = time.time()
    while True:
        res = pyautogui.locateOnScreen("tili.png")
        if res is not None:
            state = 4
            break
        elif time.time()-state_start_time > timeout:
            # 超时
            state = 7
            break
        else:
            time.sleep(interval)


def chocobo_run(timeout=200, interval=1):
    global state
    state_start_time = time.time()
    pyautogui.keyDown('w')
    pyautogui.keyDown('a')
    item = True
    finished = False
    while True:
        if time.time() - state_start_time > 15 and not finished:
            pyautogui.keyUp('a')
            finished = True

        res = pyautogui.locateOnScreen("result.png")
        if res is not None:
            pyautogui.keyUp('w')
            # pyautogui.keyUp('a')
            state = 5
            break
        elif time.time() - state_start_time > timeout:
            # 超时
            pyautogui.keyUp('w')
            # pyautogui.keyUp('a')
            state = 7
            break
        elif item:
            # 使用道具
            pyautogui.keyDown('1')
            time.sleep(random.random()/10)
            pyautogui.keyUp('1')
            time.sleep(interval)
        else:
            time.sleep(interval)


def recording_the_results(timeout=90, interval=1):
    global state, turn
    state_start_time = time.time()

    mingci = None
    exp = None
    jdb = None

    turn += 1
    print("已经成功进行了%d轮赛鸟！" % turn)

    res = pyautogui.locateOnScreen("result.png")
    if res is not None:
        mingci = recognize_mingci(res)
        if mingci is None:
            print("获取比赛的名次失败！")
    else:
        print("获取比赛的名次失败！")
    res = pyautogui.locateOnScreen("reward.png")
    if res is not None:
        exp = recognize_exp(res)
    else:
        print("获取奖励的经验值失败！")
    res = pyautogui.locateOnScreen("reward.png")
    if res is not None:
        jdb = recognize_jdb(res)
    else:
        print("获取奖励的金蝶币失败！")

    if mingci is not None and exp is not None and jdb is not None:
        mingci_list.append(mingci)
        exp_list.append(exp)
        jbd_list.append(jdb)
        print("比赛结果：")
        print("名次：%d (平均：%.2f)" % (mingci, sum(mingci_list) / len(mingci_list) * 1.0))
        print("经验值：%d (共计：%d)" % (exp, sum(exp_list)))
        print("金蝶币：%d (共计：%d)" % (jdb, sum(jbd_list)))
        file = open('result.txt', 'a')
        file.write("%d,%d,%d\n" % (mingci, exp, jdb))
        file.close()
    else:
        pyautogui.screenshot().save("error.png")

    while True:
        res = pyautogui.locateOnScreen("game7.png")
        if res is not None:
            # 单击退出
            my_click(res[0], res[1])
            state = 6
            break
        elif time.time()-state_start_time > timeout:
            # 超时
            state = 7
            break
        else:
            time.sleep(interval)


def waiting_for_return(timeout=60, interval=1):
    global state
    state_start_time = time.time()
    while True:
        res = pyautogui.locateOnScreen("coin.png")
        if res is not None:
            state = 1
            break
        elif time.time()-state_start_time > timeout:
            # 超时
            state = 7
            break
        else:
            time.sleep(interval)


def timeout():
    global state
    pyautogui.alert(text='脚本运行时发生超时异常，即将重启脚本！', title='超时警告', button='OK')
    time.sleep(100)
    res = pyautogui.locateOnScreen("coin.png")
    if res is not None:
        state = 1
    else:
        state = -1


def loop():
    while True:
        print(SYSTEM_STATE[state])
        if state == 1:
            ready_to_queue()
        elif state == 2:
            waiting_for_queue()
        elif state == 3:
            waiting_for_race_begin()
        elif state == 4:
            chocobo_run()
        elif state == 5:
            recording_the_results()
        elif state == 6:
            waiting_for_return()
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        elif state == 7:
            timeout()
        else:
            time.sleep(1)


if __name__ == "__main__":
    loop()