import matplotlib.font_manager as fm

# 检查特定字体是否在系统中
def check_font(font_name):
    font_list = fm.findSystemFonts()
    for font_path in font_list:
        if font_name in font_path:
            return True
    return False

# 检查字体
fonts_to_check = ['SimHei', 'Arial Unicode MS']
for font_name in fonts_to_check:
    if check_font(font_name):
        print(f"Font '{font_name}' is available.")
    else:
        print(f"Font '{font_name}' is not available.")
