from app import process_map_dir
from app import process_res_ocr_dir
from app import process_res_unrepeated_dir


if __name__ == '__main__':
    process_map_dir()
    process_res_ocr_dir()
    process_res_unrepeated_dir()