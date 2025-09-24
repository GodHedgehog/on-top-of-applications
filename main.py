from kivy.app import App
from kivy.uix.button import Button
from jnius import autoclass, cast

# Android-классы
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
Gravity = autoclass('android.view.Gravity')
TextView = autoclass('android.widget.TextView')
Color = autoclass('android.graphics.Color')
Settings = autoclass('android.provider.Settings')
Intent = autoclass('android.content.Intent')
String = autoclass('java.lang.String')
Build_VERSION = autoclass('android.os.Build$VERSION')

class OverlayDemo(App):
    def build(self):
        return Button(text="Показать плавающее окно", on_press=self.show_overlay)

    def show_overlay(self, *args):
        activity = PythonActivity.mActivity

        # Проверяем разрешение на оверлей
        if not Settings.canDrawOverlays(activity):
            intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
            activity.startActivity(intent)
            return

        window_service = activity.getSystemService(Context.WINDOW_SERVICE)
        window_manager = cast('android.view.WindowManager', window_service)

        # Создаём текстовое поле
        textview = TextView(activity)
        textview.setText(String("Привет с оверлея!"))
        textview.setBackgroundColor(Color.argb(200, 0, 0, 0))
        textview.setTextColor(Color.WHITE)
        textview.setPadding(50, 50, 50, 50)

        # Тип окна в зависимости от версии Android
        if Build_VERSION.SDK_INT >= 26:
            window_type = LayoutParams.TYPE_APPLICATION_OVERLAY
        else:
            window_type = LayoutParams.TYPE_PHONE

        # Настройки окна
        params = LayoutParams(
            LayoutParams.WRAP_CONTENT,
            LayoutParams.WRAP_CONTENT,
            window_type,
            LayoutParams.FLAG_NOT_FOCUSABLE,
            -3  # PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.TOP | Gravity.LEFT
        params.x = 100
        params.y = 300

        # Добавляем окно поверх других приложений
        window_manager.addView(textview, params)

if __name__ == "__main__":
    OverlayDemo().run()
