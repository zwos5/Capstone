import pyautogui
import time

buttons = ['samplepage_home.png', 'about.png', 'purpose.png']
for button in buttons:
    print(f'click on {button}')
    while pyautogui.locateOnScreen(button) is None:
        pyautogui.PAUSE = 2.5
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(button)))
    print('click back')
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('back.png')))
    time.sleep(2)
pyautogui.hotkey('alt','f4') 
print("Test Complete")