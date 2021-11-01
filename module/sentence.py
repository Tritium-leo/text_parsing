from typing import *


class Sentence(object):
    source: str
    sentence_text: str
    sentence_start_index: int
    token_positions: Dict[str, List]
    time_token_positions: Dict[str, List]
    sentence_time: str

    def __init__(self, param):
        self.source = param.get('source', '')
        self.sentence_text = param.get('sentence_text', '')
        self.token_positions = param.get('token_positions', {})
        self.sentence_start_index = param.get('sentence_start_index', 0)

        self.sentence_time = param.get('sentence_time', 'UNKNOWN')
        self.time_token_positions = param.get('time_token_positions', {})
