#region packages
from datetime import datetime
import logging, os, sys
#endregion

class log_writter:
    #region declarations
    error_logger = ''
    activity_logger = ''
    #endregion

    def __init__(self):
        exceptions = ''
        configFilePath = 'app.cfg'
        err_log_file = ''
        sysDate = datetime.now()
        level=logging.INFO

        if not os.path.exists(configFilePath):
            err_log_file = 'other'
            configFilePath = 'app.cfg'

        if err_log_file == 'other':
            err_log_file = "Logs/Exception/Exception" + sysDate.strftime('%d_%b_%Y') + ".log"
            act_log_file = "Logs/Activity/Activity" + sysDate.strftime('%d_%b_%Y') + ".log"
        else:
            err_log_file = "Logs/Exception/Exception" + sysDate.strftime('%d_%b_%Y') + ".log"
            act_log_file = "Logs/Activity/Activity" + sysDate.strftime('%d_%b_%Y') + ".log"
        
        if not os.path.exists(os.path.dirname(err_log_file)):
            try:
                os.makedirs(os.path.dirname(err_log_file))
            except OSError as exception:
                pass
        
        if not os.path.exists(os.path.dirname(act_log_file)):
            try:
                os.makedirs(os.path.dirname(act_log_file))
            except OSError as exception:
                pass

        formatter = logging.Formatter(
            'Date : %(asctime)s, \nLevel : %(levelname)s, \nLine No :  %(lineno)d, \nFunction Name : %(funcName)s, \nMessage : %(message)s \n--------------------------------------------------------------------------------------',
            '%Y-%m-%d %H:%M')

        handler = logging.FileHandler(err_log_file)
        handler.setFormatter(formatter)

        self.error_logger = logging.getLogger("ExceptionLog")
        self.error_logger.setLevel(level)
        self.error_logger.addHandler(handler)
        
        handler = logging.FileHandler(act_log_file)
        handler.setFormatter(formatter)

        self.activity_logger = logging.getLogger("ActivityLog")
        self.activity_logger.setLevel(level)
        self.activity_logger.addHandler(handler)

    def write_exception(self, message, method_name):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fullMessage = str(method_name) + " | " + str(message) + " | Error line no : " + str(exc_tb.tb_lineno)
        self.error_logger.error(fullMessage)

    def write_activity(self, actvityMessage, stepNo):
        fullMessage = str(stepNo) + " | " + str(actvityMessage)
        self.activity_logger.info(fullMessage)
