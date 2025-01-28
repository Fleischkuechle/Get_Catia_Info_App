from kivy.app import App
from kivy.uix.label import Label

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import win32com.client

class Get_Catia_Info_label(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_text_size)
        self.bind(pos=self._update_text_size)

    def _update_text_size(self, *args):
        self.font_size = self.height * 0.5  # Adjust this multiplier for different text sizes

    # # Retrieving specific properties
    # operating_system = system_config.OperatingSystem
    # version = system_config.Version
    # release = system_config.Release
    # service_pack = system_config.ServicePack
    # product_count = system_config.ProductCount
    # name = system_config.Name
    def get_catia_system_info(self):
        catia=None
        try:
            catia = win32com.client.Dispatch("CATIA.Application")
            system_config = catia.SystemConfiguration

            operating_system = getattr(system_config, "OperatingSystem", None)
            version = getattr(system_config, "Version", None)
            release = getattr(system_config, "Release", None)
            service_pack = getattr(system_config, "ServicePack", None)
            product_count = getattr(system_config, "ProductCount", None)
            name = getattr(system_config, "Name", None)
            product_count
            return operating_system, version, release, service_pack,product_count,name
        except Exception as e:
            return None, None, None, None

    def update_info(self, )->str:
        operating_system, version, release, service_pack,product_count,name = self.get_catia_system_info()
        if None not in (operating_system, version, release, service_pack,product_count,name):
            info_text:str = (
                f"Operating System: {operating_system}\n"
                f"CATIA Version: {version}\n"
                f"CATIA Release: {release}\n"
                f"Service Pack: {service_pack}\n"
                f"Product Count: {product_count}\n"
                f"Name: {name}\n"
            )
        else:
            info_text = "Could not retrieve CATIA system information."
        self.text = info_text
        #self.info_label.text = info_text
        return info_text




class Get_Catia_Info_App(App):
    def build(self):
        self.layout=FloatLayout()
        self.label = Get_Catia_Info_label(text="Hello, World!", halign='left', valign='center')
        #self.label.update_info()
        self.label.text=self.label.update_info()
        self.label.bind(size=self._update_font_size)
        Window.bind(on_resize=self._on_window_resize)
        self.size_factor:float=0.05
        self.layout.add_widget(self.label)
        self.button = Button(text="Get CATIA Info\n(result depends on running Catia)", size_hint=(1, 0.2))
        self.button.bind(on_press=self._update_info)
        self.layout.add_widget(self.button)
        return self.layout#self.label
    	
    def _update_info(self, instance):
        self.label.update_info()

        
    def _on_window_resize(self, *args):
        self.label.size = Window.size

    def _update_font_size(self, *args):
        
        #self.label.font_size =self.size_factor * min(self.label.width, self.label.height)
        self.label.font_size =self.size_factor * max(self.label.width, self.label.height)
if __name__ == '__main__':
    Get_Catia_Info_App().run()
