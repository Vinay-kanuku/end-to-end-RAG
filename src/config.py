from constants import DATA_DIR_NAME, YOUTUBE_DATA_DIR_NAME, ARTICLE_DATA_DIR_NAME
import os 

class ConfigManager:
    def __init__(self):
        self.data_dir = DATA_DIR_NAME
        self.youtube_data_dir = YOUTUBE_DATA_DIR_NAME
        self.article_data_dir = ARTICLE_DATA_DIR_NAME

class YoutubeConfig(ConfigManager):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.data_dir = os.path.join(self.config_manager.data_dir, self.config_manager.youtube_data_dir)
         
class ArticleConfig(ConfigManager):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.data_dir = os.path.join(self.config_manager.data_dir, self.config_manager.article_data_dir)



