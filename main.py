from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform

# Проверяем, что мы на Android, перед импортом jnius
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    # Импортируем необходимые классы Android
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Settings = autoclass('android.provider.Settings')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    String = autoclass('java.lang.String')

class OverlayButtonApp(App):
    
    def build(self):
        layout = FloatLayout()
        swipe_button = Button(
            text='Свайп',
            size_hint=(None, None),
            size=('100dp', '50dp'),
            pos_hint={'x': 0, 'center_y': 0.5}
        )
        swipe_button.bind(on_press=self.perform_swipe)
        layout.add_widget(swipe_button)
        return layout

    def on_start(self):
        """
        Этот метод вызывается при старте приложения.
        Идеальное место для проверки разрешений.
        """
        if platform == 'android':
            self.check_all_permissions()

    @run_on_ui_thread
    def check_all_permissions(self):
        """
        Проверяет оба разрешения и запрашивает их, если необходимо.
        """
        if not self.has_overlay_permission():
            self.request_overlay_permission()
            return # Выходим, чтобы пользователь сначала дал одно разрешение

        if not self.is_accessibility_service_enabled():
            self.request_accessibility_permission()

    # --- Методы для работы с разрешением OVERLAY ---
    
    def has_overlay_permission(self):
        """Проверяет, дано ли разрешение на отображение поверх других окон."""
        return Settings.canDrawOverlays(PythonActivity.mActivity)

    def request_overlay_permission(self):
        """Открывает системные настройки для выдачи разрешения OVERLAY."""
        package_name = PythonActivity.mActivity.getPackageName()
        intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse(String.format("package:%s", (package_name,))))
        PythonActivity.mActivity.startActivity(intent)

    # --- Методы для работы со службой специальных возможностей ---
    
    def is_accessibility_service_enabled(self):
        """Проверяет, включена ли наша служба в настройках."""
        activity = PythonActivity.mActivity
        package_name = activity.getPackageName()
        service_name = f'{package_name}/.ServiceSwipeService'
        
        try:
            enabled_services = Settings.Secure.getString(
                activity.getContentResolver(),
                Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
            )
            return enabled_services is not None and service_name in enabled_services
        except Exception:
            return False

    def request_accessibility_permission(self):
        """Открывает системные настройки для включения службы."""
        intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
        PythonActivity.mActivity.startActivity(intent)

    # --- Основное действие ---

    def perform_swipe(self, instance):
        """
        Выполняет свайп, предварительно проверив, что все разрешения на месте.
        """
        if platform != 'android':
            print("Не на Android, свайп невозможен.")
            return

        # Повторная проверка прямо перед действием
        if not self.has_overlay_permission() or not self.is_accessibility_service_enabled():
            print("Разрешения не предоставлены. Открываю настройки.")
            self.check_all_permissions()
            return
            
        # Ваш код для выполнения свайпа
        try:
            package_name = PythonActivity.mActivity.getPackageName()
            service_class_name = f'{package_name}.ServiceSwipeService'
            service = autoclass(service_class_name)
            
            if service and service.getInstance():
                service.getInstance().swipeUp()
                print("Свайп выполнен.")
            else:
                print("Не удалось получить экземпляр службы. Включена ли она?")
                self.request_accessibility_permission()
        except Exception as e:
            print(f"Ошибка при попытке свайпа: {e}")
            # Если мы все еще получаем ClassNotFoundException здесь,
            # значит проблема в сборке (buildozer.spec), а не в разрешениях.
            

if __name__ == '__main__':
    OverlayButtonApp().run()
