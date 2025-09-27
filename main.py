from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from jnius import autoclass

class OverlayButtonApp(App):
    def build(self):
        layout = FloatLayout()

        # Кнопка, располагающаяся слева
        swipe_button = Button(
            text='Свайп',
            size_hint=(None, None),
            size=('100dp', '50dp'),
            pos_hint={'x': 0, 'center_y': 0.5}
        )
        swipe_button.bind(on_press=self.perform_swipe)
        layout.add_widget(swipe_button)

        return layout

    def perform_swipe(self, instance):
        # Импортируем PythonActivity для доступа к контексту Android
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        mActivity = PythonActivity.mActivity

        # Динамически получаем имя пакета текущего приложения
        package_name = mActivity.getPackageName()

        # Формируем правильное и полное имя класса службы
        # "Service" + "SwipeService" (имя из buildozer.spec)
        service_class_name = f'{package_name}.ServiceSwipeService'
        
        try:
            # Получаем доступ к классу нашей службы
            service = autoclass(service_class_name)
            
            # Вызываем метод для выполнения свайпа
            if service.getInstance():
                service.getInstance().swipeUp()
            else:
                print("SwipeService: Service instance is not available.")
        except Exception as e:
            print(f"SwipeService: Could not find or access service class: {e}")

if __name__ == '__main__':
    OverlayButtonApp().run()

