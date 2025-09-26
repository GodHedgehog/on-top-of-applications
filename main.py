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
        # Получаем доступ к нашей службе
        service = autoclass('org.test.swipeservice.ServiceSwipeService')
        
        # Вызываем метод для выполнения свайпа
        if service.getInstance():
            service.getInstance().swipeUp()

if __name__ == '__main__':
    OverlayButtonApp().run()
