from abc import ABC, abstractmethod
from typing import List, Dict

class NewsSource(ABC):

    @abstractmethod
    def fetch(self) -> List[Dict]:
        """
        Returns:
        [
          {
            url,
            title,
            content,
            published_at
          }
        ]
        """
        pass
