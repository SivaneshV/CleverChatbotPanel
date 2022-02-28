#region packages
import configparser, os, sys
#endregion

#region declarations
config = configparser.ConfigParser()
#endregion

class Config:
    #region declarations
    configFilePath = 'app.cfg'
    #endregion

    def get_app_configs(self):
        self.cfgDict = {}

        try:
            config.read(self.configFilePath)

            chat_clear_buffer_min = str(config.get('AppConfigs', 'chat_clear_buffer_min'))

            self.cfgDict.update({'chat_clear_buffer_min': chat_clear_buffer_min})
            
        except Exception as e:
            pass

        return self.cfgDict

    def get_ui_configs(self):
        self.cfgDict = {}

        try:
            config.read(self.configFilePath)

            chat_timeout_sec = str(config.get('UIConfigs', 'chat_timeout_sec'))
            chat_anythingelse_sec = str(config.get('UIConfigs', 'chat_anythingelse_sec'))

            self.cfgDict.update({'chat_timeout_sec': chat_timeout_sec})
            self.cfgDict.update({'chat_anythingelse_sec': chat_anythingelse_sec})
            
        except Exception as e:
            pass

        return self.cfgDict
