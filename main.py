from kivy.app import App
from kivy.uix.button import Button
from jnius import autoclass

class MyApp(App):
    def build(self):
        return Button(text="Свайп вверх", on_press=self.swipe_up)

    def swipe_up(self, *args):
        try:
            # Отправляем Intent сервису
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent("MY_ACCESSIBILITY_ACTION")
            activity = PythonActivity.mActivity
            activity.sendBroadcast(intent)  # или startService, если так удобнее
        except Exception as e:
            print("Ошибка отправки команды сервису:", e)

if __name__ == "__main__":
    MyApp().run()
