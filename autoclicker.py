import threading
import time
from pynput import keyboard
from pynput import mouse

auto_click_count = 0
mouse_controller = mouse.Controller()
ac_enable = True
pressing = False


class AutoClickTask:
    running = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        global mouse_controller
        global auto_click_count
        global ac_enable
        while self.running and ac_enable:
            print("clicking")
            auto_click_count += 1
            print("[Debug] p " + str(auto_click_count))
            mouse_controller.click(mouse.Button.left)
            time.sleep(0.06)


task = AutoClickTask()


def on_click(x, y, button, pressed):
    global pressing
    global auto_click_count
    global task
    global ac_enable

    if button == mouse.Button.left:
        if pressed:
            pressing = True
            if not ac_enable:
                return
            if not task.running:
                print("start ac")
                threading.Thread(target=task.run).start()
        else:
            auto_click_count -= 1
            print("[Debug] r " + str(auto_click_count))
            if auto_click_count < 0:
                print("end ac")
                auto_click_count = 0
                task.stop()
                task = AutoClickTask()
                pressing = False


def switch_ac(key):
    global ac_enable
    global pressing
    if key == keyboard.Key.tab:
        ac_enable = not ac_enable
        print("[Switch] " + str(ac_enable))
        if ac_enable and pressing:
            print("[Switch] Auto Start AC")
            threading.Thread(target=task.run).start()


mouse_listener = mouse.Listener(on_click=on_click)

key_listener = keyboard.Listener(on_press=switch_ac)

mouse_listener.start()
key_listener.start()

key_listener.join()