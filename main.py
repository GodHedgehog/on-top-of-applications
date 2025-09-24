from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from jnius import autoclass

class BlackScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0, 0, 0, 1)  # чёрный фон

class TestApp(App):
    def build(self):
        # через 3 секунды показать toast и закрыть приложение
        Clock.schedule_once(lambda dt: self.show_toast_and_exit(
            "Внимание! Система безопасности Android обнаружила шпионское ПО, это приложение скоро будет удалено!"
        ), 1)
        return BlackScreen()

    def show_toast_and_exit(self, text):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Toast = autoclass('android.widget.Toast')
        TextView = autoclass('android.widget.TextView')
        Color = autoclass('android.graphics.Color')
        String = autoclass('java.lang.String')
        GradientDrawable = autoclass("android.graphics.drawable.GradientDrawable")
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")

        activity = PythonActivity.mActivity

        # Получаем ID системного фона Toast
        Resources = activity.getResources()
        toast_frame_id = Resources.getIdentifier("toast_frame", "drawable", "android")

        def make_toast():
            tv = TextView(activity)
            tv.setText(String(text))
            tv.setTextColor(Color.BLACK)
            tv.setTextSize(16)
            tv.setPadding(40, 25, 40, 25)
            tv.setLineSpacing(1.2, 1.2)  # добавляем немного межстрочного интервала
            tv.setSingleLine(False)      # многострочный текст
            tv.setMaxLines(10)           # ограничение по высоте
            tv.setLayoutParams(LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT))

            # 🔹 Создаем фон с закругленными углами и обводкой
            bg = GradientDrawable()
            bg.setShape(GradientDrawable.RECTANGLE)
            bg.setColor(Color.WHITE)  # фон
            bg.setCornerRadius(25)  # скругление углов (px)
            bg.setStroke(4, Color.GRAY)  # толщина и цвет рамки
            tv.setBackground(bg)

            toast = Toast(activity)
            toast.setDuration(6000)
            toast.setView(tv)
            toast.show()

            def suggest_uninstall(dt):
                package_name = activity.getPackageName()
                intent = Intent(Intent.ACTION_DELETE)
                intent.setData(Uri.parse("package:" + package_name))
                activity.startActivity(intent)

            # закрыть приложение через LENGTH_LONG (~3.5 сек)
            Clock.schedule_once(suggest_uninstall, 1)
            Clock.schedule_once(lambda dt: activity.finish(), 3)


        # запускаем в UI-потоке
        activity.runOnUiThread(make_toast)

TestApp().run()



