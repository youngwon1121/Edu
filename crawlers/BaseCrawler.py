from abc import ABCMeta, abstractmethod


class BaseCrawler(metaclass=ABCMeta):
    @abstractmethod
    def get_post(self, url=None):
        pass

    @abstractmethod
    def get_target_site_ids(self):
        pass
