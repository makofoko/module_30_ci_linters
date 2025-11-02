import logging
import string

class AsciiFilter(logging.Filter):
    """Пропускает только ASCII-сообщения."""
    def filter(self, record: logging.LogRecord) -> bool:
        msg = str(record.getMessage())
        return msg.isascii()

class AsciiReplaceFilter(logging.Filter):
    """Заменяет сообщение, если оно содержит не-ASCII символы."""
    def __init__(self, replacement="ÎŒØ∏‡°⁄·°€йцукен"):
        super().__init__()
        self.replacement = replacement

    def filter(self, record: logging.LogRecord) -> bool:
        msg = str(record.getMessage())
        if not msg.isascii():
            record.msg = self.replacement
            record.args = ()
        return True
