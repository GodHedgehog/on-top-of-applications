from kivy.app import App
from kivy.uix.button import Button
from jnius import autoclass, cast

# Классы Android
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
Gravity = autoclass('android.view.Gravity')
Color = autoclass('android.graphics.Color')
TextView = autoclass('android.widget.TextView')

class OverlayDemo(App):
    def build(self):
        return Button(text="Показать плавающее окно", on_press=self.show_overlay)

    def show_overlay(self, *args):
        activity = PythonActivity.mActivity
        window_service = activity.getSystemService(Context.WINDOW_SERVICE)
        window_manager = cast('android.view.WindowManager', window_service)

        # Создаём текстовое поле
        textview = TextView(activity)
        textview.setText("Привет с оверлея!")
        textview.setBackgroundColor(Color.argb(200, 0, 0, 0))
        textview.setTextColor(Color.WHITE)
        textview.setPadding(50, 50, 50, 50)

        # Настройки окна
        params = LayoutParams(
            LayoutParams.WRAP_CONTENT,
            LayoutParams.WRAP_CONTENT,
            LayoutParams.TYPE_APPLICATION_OVERLAY,  # для Android 8+
            LayoutParams.FLAG_NOT_FOCUSABLE,
            -3  # PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.TOP | Gravity.LEFT
        params.x = 100
        params.y = 300

        # Добавляем окно
        window_manager.addView(textview, params)

if __name__ == "__main__":
    OverlayDemo().run()
