import os
import tkinter

import requests

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if GOOGLE_API_KEY is None:
    raise ValueError('GOOGLE_API_KEY should not be None')


def translate(text, lang_source='fr', lang_target='en'):
    response = requests.post(
        url='https://translation.googleapis.com/language/translate/v2',
        params={
            'q': text,
            'source': lang_source,
            'target': lang_target,
            'format': 'text',
            'key': GOOGLE_API_KEY,
        }
    )
    print(response.json())
    result = response.json()['data']['translations'][0]['translatedText']
    result.replace(r'\n', '')

    return result


class App:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Traduction')

        self.frame = tkinter.Frame(self.window, padx=10, pady=10)
        self.frame_bottom = tkinter.Frame(self.window, padx=10, pady=10)

        self.text = tkinter.StringVar('')

        self.widget_text = tkinter.Text(self.frame, height=10, width=40)
        self.widget_result = tkinter.Label(
            self.frame,
            textvariable=self.text,
            height=10, width=40
        )
        self.widget_button = tkinter.Button(
            self.frame_bottom,
            text='Traduire',
            pady=10,
            command=self._translate
        )
        self._make_layout()

    def _make_layout(self):
        self.frame.pack()
        self.frame_bottom.pack(side=tkinter.BOTTOM)
        self.widget_text.pack(side=tkinter.LEFT)
        self.widget_result.pack(side=tkinter.RIGHT)
        self.widget_button.pack()

    def run(self):
        self.window.mainloop()

    def _translate(self):
        text_to_translate = self.widget_text.get('1.0', tkinter.END)
        translated_text = translate(text_to_translate, 'fr', 'en')
        self.text.set(translated_text)


if __name__ == '__main__':
    app = App()
    app.run()
