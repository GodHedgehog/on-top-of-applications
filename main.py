from kivy.app import App
from kivy.uix.button import Button
from jnius import autoclass, cast, PythonJavaClass, java_method

# Android-классы
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
Gravity = autoclass('android.view.Gravity')
TextView = autoclass('android.widget.TextView')
Color = autoclass('android.graphics.Color')
Settings = autoclass('android.provider.Settings')
Intent = autoclass('android.content.Intent')
MotionEvent = autoclass('android.view.MotionEvent')
View = autoclass('android.view.View')
String = autoclass('java.lang.String')
Build_VERSION = autoclass('android.os.Build$VERSION')
Runnable = autoclass('java.lang.Runnable')

# Runnable для UI-потока
class AddViewRunnable(PythonJavaClass):
    __javainterfaces__ = ['java/lang/Runnable']

    def __init__(self, window_manager, view, params):
        super().__init__()
        self.window_manager = window_manager
        self.view = view
        self.params = params

    @java_method('()V')
    def run(self):
        self.window_manager.addView(self.view, self.params)

# Listener для перетаскивания
class TouchListener(PythonJavaClass):
    __javainterfaces__ = ['android/view/View$OnTouchListener']

    def __init__(self, window_manager, view, params):
        super().__init__()
        self.window_manager = window_manager
        self.view = view
        self.params = params
        self.last_x = 0
        self.last_y = 0

    @java_method('(Landroid/view/View;Landroid/view/MotionEvent;)Z')
    def onTouch(self, v, event):
        action = event.getAction()
        if action == MotionEvent.ACTION_DOWN:
            self.last_x = int(event.getRawX())
            self.last_y = int(event.getRawY())
            return True
        elif action == MotionEvent.ACTION_MOVE:
            dx = int(event.getRawX()) - self.last_x
            dy = int(event.getRawY()) - self.last_y
            self.params.x += dx
            self.params.y += dy
            self.window_manager.updateViewLayout(self.view, self.params)
            self.last_x = int(event.getRawX())
            self.last_y = int(event.getRawY())
            return True
        return False

class OverlayDemo(App):
    def build(self):
        return Button(text="Показать плавающее окно", on_press=self.show_overlay)

    def show_overlay(self, *args):
        activity = PythonActivity.mActivity

        # Проверка разрешения на оверлей
        if not Settings.canDrawOverlays(activity):
            intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
            activity.startActivity(intent)
            return

        window_service = activity.getSystemService(Context.WINDOW_SERVICE)
        window_manager = cast('android.view.WindowManager', window_service)

        # Создаём текстовое поле
        textview = TextView(activity)
        textview.setText(String("Перетащи меня!"))
        textview.setBackgroundColor(Color.argb(200, 0, 0, 0))
        textview.setTextColor(Color.WHITE)
        textview.setPadding(50, 50, 50, 50)

        # Тип окна
        if Build_VERSION.SDK_INT >= 26:
            window_type = LayoutParams.TYPE_APPLICATION_OVERLAY
        else:
            window_type = LayoutParams.TYPE_PHONE

        # Параметры окна
        params = LayoutParams(
            LayoutParams.WRAP_CONTENT,
            LayoutParams.WRAP_CONTENT,
            window_type,
            LayoutParams.FLAG_NOT_FOCUSABLE,
            -3
        )
        params.gravity = Gravity.TOP | Gravity.LEFT
        params.x = 100
        params.y = 300

        # Добавляем обработчик перетаскивания
        listener = TouchListener(window_manager, textview, params)
        textview.setOnTouchListener(listener)

        # Добавляем view через UI-поток
        activity.runOnUiThread(AddViewRunnable(window_manager, textview, params))

if __name__ == "__main__":
    OverlayDemo().run()
