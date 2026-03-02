from paddleocr import PaddleOCR
import re

# ① 创建数字字典（只运行一次）
digit_dict_path = 'digit_dict.txt'
with open(digit_dict_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join([str(i) for i in range(10)]))

# ② 初始化OCR —— 极简数字模式
# ocr = PaddleOCR(
#     lang='en',                  # 使用英文轻量模型
#     rec_char_dict_path=digit_dict_path,  # 限定识别字符集
#     use_angle_cls=False,        # 关闭方向分类，加速
#     det_db_box_thresh=0.5,      # 保守框阈值
#     rec_image_height=32,        # 降低识别输入尺寸，加速
#     use_gpu=False               # 如果有GPU可改成 True
# )

ocr = PaddleOCR( 
                det_db_thresh=0.3, 
                det_db_box_thresh=0.5, 
                rec_image_height=10,  
                use_angle_cls=False,
                rec_model_dir='models/ch_number_mobile_v2.0_rec_infer',
                det_model_dir='models/ch_number_mobile_v2.0_det_infer',
                rec_char_dict_path='number_dict.txt'
                )

# ③ 识别图片
result = ocr.ocr('1.png', cls=False)

# ④ 提取识别结果
for line in result:
    text = line[1][0]
    print("识别文本:", text)
