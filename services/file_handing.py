import logging 
import os

logger = logging.getLogger(__name__)

def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    end_signs = ",.!:;?"
    max_end = min(len(text), start + page_size)
    chunk = text[start:max_end]
    
    last_good = -1
    i = 0
    
    while i < len(chunk):
        if chunk[i] in end_signs:
            seq_end = i
            while seq_end + 1 < len(chunk) and chunk[seq_end + 1] in end_signs:
                seq_end += 1
            
            if seq_end < len(chunk):
                if start + seq_end + 1 >= len(text):
                    last_good = seq_end
                else:
                    next_char = text[start + seq_end + 1]
                    if next_char not in end_signs:
                        last_good = seq_end
            i = seq_end + 1
        else:
            i += 1
    
    if last_good != -1:
        page_text = text[start:start + last_good + 1]
        page_len = last_good + 1
    else:
        page_text = chunk
        page_len = len(chunk)
    
    return page_text, page_len

def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    try:
        with open(file=os.path.normpath(path), mode="r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        logger.error("Error reading a book: %s", e)
        raise e

    book = {}
    start, page_number = 0, 1

    while start < len(text):
        page_text, actual_page_size = _get_part_text(text, start, page_size)
        start += actual_page_size
        book[page_number] = page_text.strip()
        page_number += 1

    return book 
