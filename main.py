from kivy.app import App
from jnius import autoclass, cast, PythonJavaClass, java_method

# Android классы
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
Gravity = autoclass('android.view.Gravity')
ButtonAndroid = autoclass('android.widget.Button')
Intent = autoclass('android.content.Intent')
Settings = autoclass('android.provider.Settings')
Uri = autoclass('android.net.Uri')
Build_VERSION = autoclass('android.os.Build$VERSION')
ComponentName = autoclass('android.content.ComponentName')
Runnable = autoclass('java.lang.Runnable')
Secure = autoclass('android.provider.Settings$Secure')

class AddViewRunnable(PythonJavaClass):
    __javainterfaces__ = ['java/lang/Runnable']
    def __init__(self, wm, view, params):
        super().__init__()
        self.wm = wm
        self.view = view
        self.params = params
    @java_method('()V')
    def run(self):
        self.wm.addView(self.view, self.params)

class OverlayApp(App):
    def build(self):
        self.check_permissions()
        return None

    def check_permissions(self):
        activity = PythonActivity.mActivity

        # 1. Проверяем overlay-разрешение
        if not Settings.canDrawOverlays(activity):
            intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                            Uri.parse("package:" + activity.getPackageName()))
            activity.startActivity(intent)
            return

        # 2. Проверяем AccessibilityService
        if not self.is_accessibility_enabled(activity):
            intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
            activity.startActivity(intent)
            return

        # Всё включено → создаём плавающую кнопку
        self.create_overlay_button()

def is_accessibility_enabled(self, activity):
    service_id = activity.getPackageName() + "/.MyAccessibilityService"
    enabled_services = Secure.getString(
        activity.getContentResolver(),
        Secure.ENABLED_ACCESSIBILITY_SERVICES
    )
    return enabled_services and service_id in enabled_services

    def create_overlay_button(self):
        activity = PythonActivity.mActivity
        wm = cast('android.view.WindowManager',
                  activity.getSystemService(Context.WINDOW_SERVICE))

        # Android-кнопка поверх всех приложений
        button = ButtonAndroid(activity)
        button.setText("Свайп ↑")

        # При клике → отправляем Intent в AccessibilityService
        def on_click(v):
            intent = Intent("MY_ACCESSIBILITY_ACTION")
            activity.sendBroadcast(intent)

        button.setOnClickListener(on_click)

        # Тип окна
        if Build_VERSION.SDK_INT >= 26:
            wtype = LayoutParams.TYPE_APPLICATION_OVERLAY
        else:
            wtype = LayoutParams.TYPE_PHONE

        params = LayoutParams(
            LayoutParams.WRAP_CONTENT,
            LayoutParams.WRAP_CONTENT,
            wtype,
            LayoutParams.FLAG_NOT_FOCUSABLE,
            -3
        )
        params.gravity = Gravity.TOP | Gravity.LEFT
        params.x = 200
        params.y = 600

        activity.runOnUiThread(AddViewRunnable(wm, button, params))

if __name__ == "__main__":
    OverlayApp().run()


