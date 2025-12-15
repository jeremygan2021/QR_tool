import qrcode
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os
import io
import base64

def generate_svg_qr_code(data, output_file=None, color="#000000", bg_color="#FFFFFF", 
                         style="classic", border=4, box_size=12, logo_obj=None, logo_path=None):
    """
    Generate SVG QR code with basic styling and logo support
    """
    # Create QR matrix
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    matrix = qr.get_matrix()
    matrix_size = len(matrix)
    
    # Calculate dimensions
    module_size = box_size
    total_size = (matrix_size + 2 * border) * module_size
    offset = border * module_size
    
    # Start SVG
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{total_size}" height="{total_size}" viewBox="0 0 {total_size} {total_size}">']
    
    # Background
    if bg_color != "transparent":
        svg.append(f'<rect x="0" y="0" width="{total_size}" height="{total_size}" fill="{bg_color}"/>')
        
    # Draw modules
    for y in range(matrix_size):
        for x in range(matrix_size):
            if matrix[y][x]:
                pos_x = offset + x * module_size
                pos_y = offset + y * module_size
                
                if style == "circle":
                    # Circle style
                    cx = pos_x + module_size / 2
                    cy = pos_y + module_size / 2
                    r = module_size / 2 * 0.9  # Slight padding
                    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')
                elif style == "rounded":
                    # Rounded rect style
                    padding = module_size * 0.05
                    size = module_size * 0.9
                    rx = size * 0.3
                    svg.append(f'<rect x="{pos_x + padding}" y="{pos_y + padding}" width="{size}" height="{size}" rx="{rx}" fill="{color}"/>')
                else:
                    # Classic square
                    # Optimize by drawing only if needed? No, just draw all.
                    # Add small padding to avoid gaps? Or exact.
                    # Usually exact is better for crispness, but slight overlap helps anti-aliasing.
                    # Let's do exact.
                    svg.append(f'<rect x="{pos_x}" y="{pos_y}" width="{module_size}" height="{module_size}" fill="{color}"/>')

    # Add Logo
    logo = None
    if logo_obj:
        logo = logo_obj
    elif logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        
    if logo:
        # Convert logo to base64
        buffered = io.BytesIO()
        logo.save(buffered, format="PNG")
        logo_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Calculate position and size (20% of QR size)
        logo_display_size = total_size * 0.2
        logo_x = (total_size - logo_display_size) / 2
        logo_y = (total_size - logo_display_size) / 2
        
        svg.append(f'<image href="data:image/png;base64,{logo_b64}" x="{logo_x}" y="{logo_y}" width="{logo_display_size}" height="{logo_display_size}" />')

    svg.append('</svg>')
    svg_content = '\n'.join(svg)
    
    if output_file:
        if hasattr(output_file, 'write'):
            output_file.write(svg_content.encode('utf-8'))
        else:
            with open(output_file, 'w') as f:
                f.write(svg_content)
    
    return svg_content

def generate_styled_qr_code(data, output_file="styled_qrcode.png", logo_path=None, logo_obj=None,
                           color="#000000", bg_color="#FFFFFF", box_size=12, 
                           border=4, style="rounded", img_size=(350, 350), auto_adjust=True):
    """
    生成美化的二维码
    
    参数:
        data: 要编码的数据
        output_file: 输出文件名
        logo_path: 可选的居中logo图片路径
        color: 二维码颜色
        bg_color: 背景颜色
        box_size: 二维码方块大小
        border: 边界大小
        style: 样式 ("rounded", "circle", "classic")
        img_size: 最终输出图片的大小 (宽, 高)
        auto_adjust: 是否根据数据长度自动调整参数
    """
    # 根据数据长度自动调整参数
    if auto_adjust:
        # 长链接需要更多空间
        data_length = len(data)
        
        # 根据链接长度调整二维码版本和边框大小
        qr_version = 1
        if data_length > 50:
            qr_version = 2
        if data_length > 100:
            qr_version = 3
        if data_length > 150:
            qr_version = 4
        
        # 确保边框足够大但不太大
        min_border = max(4, 4 + (data_length // 300))  # 进一步减小边框增长率
        border = max(border, min_border)
        
        # 修正：保持盒子大小不太小，确保二维码点足够明显
        # 即使对于长链接也保持较大的box_size
        box_size = max(10, box_size - (data_length // 300))  # 提高最小值和减小减小率
    else:
        qr_version = 1
    
    # 生成QR码
    qr = qrcode.QRCode(
        version=qr_version,  # 根据数据长度自动选择版本
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高纠错率以支持Logo
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # 获取二维码矩阵和大小信息
    qr_matrix = qr.get_matrix()
    matrix_size = len(qr_matrix)
    
    # 计算实际需要的图像大小
    module_size = box_size
    qr_actual_size = matrix_size * module_size
    border_size = border * module_size
    total_qr_size = qr_actual_size + 2 * border_size
    
    # 自动调整输出图像大小，确保足够大以容纳二维码
    if auto_adjust:
        min_img_size = total_qr_size + 40  # 添加额外的40像素作为边距
        if img_size[0] < min_img_size or img_size[1] < min_img_size:
            img_size = (min_img_size, min_img_size)
    
    # 创建原始图像
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_width, qr_height = qr_img.size
    
    # 应用样式
    if style == "rounded" or style == "circle":
        # 创建一个空白画布，设置为指定大小
        final_img_size = img_size
        styled_img = Image.new("RGBA", final_img_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(styled_img)
        
        # 计算居中位置的起始坐标
        start_x = (final_img_size[0] - total_qr_size) // 2 + border_size
        start_y = (final_img_size[1] - total_qr_size) // 2 + border_size
        
        # 转换颜色格式
        if color.startswith('#'):
            rgb_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            rgba_color = rgb_color + (255,)
        else:
            rgba_color = color
        
        # 定义定位点位置（左上角、右上角、左下角）
        finder_patterns = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
            (1, 0), (1, 6),
            (2, 0), (2, 2), (2, 3), (2, 4), (2, 6),
            (3, 0), (3, 2), (3, 3), (3, 4), (3, 6),
            (4, 0), (4, 2), (4, 3), (4, 4), (4, 6),
            (5, 0), (5, 6),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            
            (0, matrix_size-7), (0, matrix_size-6), (0, matrix_size-5), (0, matrix_size-4), (0, matrix_size-3), (0, matrix_size-2), (0, matrix_size-1),
            (1, matrix_size-7), (1, matrix_size-1),
            (2, matrix_size-7), (2, matrix_size-5), (2, matrix_size-4), (2, matrix_size-3), (2, matrix_size-1),
            (3, matrix_size-7), (3, matrix_size-5), (3, matrix_size-4), (3, matrix_size-3), (3, matrix_size-1),
            (4, matrix_size-7), (4, matrix_size-5), (4, matrix_size-4), (4, matrix_size-3), (4, matrix_size-1),
            (5, matrix_size-7), (5, matrix_size-1),
            (6, matrix_size-7), (6, matrix_size-6), (6, matrix_size-5), (6, matrix_size-4), (6, matrix_size-3), (6, matrix_size-2), (6, matrix_size-1),
            
            (matrix_size-7, 0), (matrix_size-7, 1), (matrix_size-7, 2), (matrix_size-7, 3), (matrix_size-7, 4), (matrix_size-7, 5), (matrix_size-7, 6),
            (matrix_size-6, 0), (matrix_size-6, 6),
            (matrix_size-5, 0), (matrix_size-5, 2), (matrix_size-5, 3), (matrix_size-5, 4), (matrix_size-5, 6),
            (matrix_size-4, 0), (matrix_size-4, 2), (matrix_size-4, 3), (matrix_size-4, 4), (matrix_size-4, 6),
            (matrix_size-3, 0), (matrix_size-3, 2), (matrix_size-3, 3), (matrix_size-3, 4), (matrix_size-3, 6),
            (matrix_size-2, 0), (matrix_size-2, 6),
            (matrix_size-1, 0), (matrix_size-1, 1), (matrix_size-1, 2), (matrix_size-1, 3), (matrix_size-1, 4), (matrix_size-1, 5), (matrix_size-1, 6),
        ]
        
        # 调整大小因子，确保点的大小足够明显
        # 修正：增加最小尺寸因子，确保二维码点始终足够大
        rect_size_factor = max(0.9, min(1.0, 18.0 / matrix_size))  # 增加系数和最小值
        circle_radius_factor = max(0.85, min(1.0, 16.0 / matrix_size))  # 增加系数和最小值
        
        # 添加一个小的间距调整，减少模块间的空白
        spacing_factor = 0.95  # 减小间距，值越小模块间距越小
        
        # 遍历二维码矩阵，绘制每个模块
        for y in range(matrix_size):
            for x in range(matrix_size):
                if qr_matrix[y][x]:  # 如果是填充点
                    # 计算模块的中心坐标，调整间距
                    center_x = start_x + x * (module_size * spacing_factor) + module_size // 2
                    center_y = start_y + y * (module_size * spacing_factor) + module_size // 2
                    
                    # 确定是否是定位点的一部分
                    is_finder = (x, y) in finder_patterns
                    
                    if style == "rounded":
                        # 对于定位点，使用较小的圆角半径，但保证大小
                        radius = 1 if is_finder else max(2, int(3 * rect_size_factor))
                        # 修正：增加最小矩形大小，确保即使在大型二维码中也清晰可见
                        rect_size = max(module_size // 1.2, int((module_size - 1) * rect_size_factor))
                        
                        # 绘制圆角矩形
                        draw.rounded_rectangle(
                            [center_x - rect_size//2, center_y - rect_size//2,
                             center_x + rect_size//2, center_y + rect_size//2],
                            radius=radius, fill=rgba_color
                        )
                    else:  # circle
                        # 修正：增加圆的最小半径，确保在大型二维码中也足够明显
                        if is_finder:
                            radius = module_size//2
                        else:
                            # 确保圆的大小不会太小
                            radius = max(module_size//2.5, int((module_size//2) * circle_radius_factor))
                        
                        # 绘制圆形
                        draw.ellipse(
                            [center_x - radius, center_y - radius,
                             center_x + radius, center_y + radius],
                            fill=rgba_color
                        )
        
            # 创建最终图像
        if bg_color == "transparent":
            final_qr = Image.new("RGBA", final_img_size, (0, 0, 0, 0))
        elif bg_color.upper() == "#FFFFFF":
            final_qr = Image.new("RGBA", final_img_size, (255, 255, 255, 255))
        else:
            bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
            final_qr = Image.new("RGBA", final_img_size, bg_rgb + (255,))
            
        final_qr.paste(styled_img, (0, 0), styled_img)
        qr_img = final_qr
    else:
        # 经典样式 - 直接使用指定颜色
        final_img_size = img_size
        
        if bg_color == "transparent":
            classic_img = Image.new("RGBA", final_img_size, (0, 0, 0, 0))
        else:
            classic_img = Image.new("RGBA", final_img_size, bg_color)
            
        draw = ImageDraw.Draw(classic_img)
        
        # 计算居中位置的起始坐标
        start_x = (final_img_size[0] - total_qr_size) // 2 + border_size
        start_y = (final_img_size[1] - total_qr_size) // 2 + border_size
        
        # 转换颜色格式
        if color.startswith('#'):
            rgb_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            rgba_color = rgb_color + (255,)
        else:
            rgba_color = color
            
        # 添加一个小的间距调整，减少模块间的空白
        spacing_factor = 0.95  # 减小间距，值越小模块间距越小
        
        # 遍历二维码矩阵，绘制每个模块
        for y in range(matrix_size):
            for x in range(matrix_size):
                if qr_matrix[y][x]:  # 如果是填充点
                    # 计算模块的中心坐标，调整间距
                    center_x = start_x + x * (module_size * spacing_factor) + module_size // 2
                    center_y = start_y + y * (module_size * spacing_factor) + module_size // 2
                    
                    # 修正：绘制矩形而不是点，确保在任何尺寸下都可见
                    rect_size = max(module_size // 1.2, module_size - 1)
                    draw.rectangle(
                        [center_x - rect_size//2, center_y - rect_size//2,
                         center_x + rect_size//2, center_y + rect_size//2],
                        fill=rgba_color
                    )
                    
        qr_img = classic_img
    
    # 添加Logo（如果提供）
    logo = None
    if logo_obj:
        logo = logo_obj.convert("RGBA")
    elif logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

    if logo:
        try:
            # 调整Logo大小，不超过二维码的20%（较大数据时需要更小Logo）
            logo_scale = 5 if data_length < 100 else 6
            logo_max_size = qr_img.size[0] // logo_scale
            logo_size = min(logo.size[0], logo.size[1], logo_max_size)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            
            # 计算位置使Logo居中
            pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
            
            # 创建圆形蒙版
            mask = Image.new("L", logo.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(1))
            
            # 将Logo粘贴到二维码上
            qr_img.paste(logo, pos, mask)
        except Exception as e:
            print(f"添加Logo时出错: {e}")
    
    if isinstance(output_file, str):
        qr_img.save(output_file)
    else:
        qr_img.save(output_file, format='PNG')
    return output_file

def generate_gradient_qr(data, output_file="gradient_qrcode.png", start_color="#1E88E5", 
                         end_color="#8BC34A", bg_color="#FFFFFF", box_size=12, 
                         border=4, img_size=(350, 350), auto_adjust=True, logo_obj=None, logo_path=None):
    """
    生成渐变色二维码
    
    参数:
        data: 要编码的数据
        output_file: 输出文件名
        start_color: 渐变起始颜色
        end_color: 渐变结束颜色
        bg_color: 背景颜色
        box_size: 二维码方块大小
        border: 边界大小
        img_size: 最终输出图片的大小 (宽, 高)
        auto_adjust: 是否根据数据长度自动调整参数
    """
    # 根据数据长度自动调整参数
    if auto_adjust:
        # 长链接需要更多空间
        data_length = len(data)
        
        # 根据链接长度调整二维码版本和边框大小
        qr_version = 1
        if data_length > 50:
            qr_version = 2
        if data_length > 100:
            qr_version = 3
        if data_length > 150:
            qr_version = 4
        
        # 确保边框足够大
        min_border = max(4, 4 + (data_length // 300))  # 减小边框增长率
        border = max(border, min_border)
        
        # 修正：保持盒子大小不太小
        box_size = max(10, box_size - (data_length // 300))
    else:
        qr_version = 1
    
    # 生成QR码
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # 将十六进制颜色转为RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    if bg_color == "transparent":
        bg_rgb = (0, 0, 0, 0)
    else:
        bg_rgb = hex_to_rgb(bg_color)
    
    # 获取二维码矩阵和大小信息
    qr_matrix = qr.get_matrix()
    matrix_size = len(qr_matrix)
    
    # 计算实际需要的图像大小
    module_size = box_size
    qr_actual_size = matrix_size * module_size
    border_size = border * module_size
    total_qr_size = qr_actual_size + 2 * border_size
    
    # 自动调整输出图像大小，确保足够大以容纳二维码
    if auto_adjust:
        min_img_size = total_qr_size + 40  # 添加额外的40像素作为边距
        if img_size[0] < min_img_size or img_size[1] < min_img_size:
            img_size = (min_img_size, min_img_size)
    
    # 创建渐变映射
    final_img_size = img_size
    if len(bg_rgb) == 4:
        gradient_img = Image.new("RGBA", final_img_size, bg_rgb)
    else:
        gradient_img = Image.new("RGBA", final_img_size, bg_rgb + (255,))
    
    # 计算居中位置的起始坐标
    start_x = (final_img_size[0] - total_qr_size) // 2 + border_size
    start_y = (final_img_size[1] - total_qr_size) // 2 + border_size
    
    # 创建渐变效果
    draw = ImageDraw.Draw(gradient_img)
    
    # 修正：调整矩形大小，确保在大型二维码中不会过小
    rect_size_factor = max(0.9, min(1.0, 18.0 / matrix_size))
    
    # 添加一个小的间距调整，减少模块间的空白
    spacing_factor = 0.95  # 减小间距，值越小模块间距越小
    
    # 遍历二维码矩阵，绘制每个模块
    for y in range(matrix_size):
        for x in range(matrix_size):
            if qr_matrix[y][x]:  # 如果是填充点
                # 计算模块的中心坐标，调整间距
                center_x = start_x + x * (module_size * spacing_factor) + module_size // 2
                center_y = start_y + y * (module_size * spacing_factor) + module_size // 2
                
                # 根据y坐标计算渐变
                ratio = y / matrix_size
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                
                # 修正：确保矩形大小足够大，即使在大型二维码中也清晰可见
                rect_size = max(module_size // 1.2, int((module_size - 1) * rect_size_factor))
                draw.rectangle(
                    [center_x - rect_size//2, center_y - rect_size//2,
                     center_x + rect_size//2, center_y + rect_size//2],
                    fill=(r, g, b)
                )
    
    # 添加Logo（如果提供）
    logo = None
    if logo_obj:
        logo = logo_obj.convert("RGBA")
    elif logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

    if logo:
        try:
            # 调整Logo大小，不超过二维码的20%（较大数据时需要更小Logo）
            logo_scale = 5 if data_length < 100 else 6
            logo_max_size = gradient_img.size[0] // logo_scale
            logo_size = min(logo.size[0], logo.size[1], logo_max_size)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            
            # 计算位置使Logo居中
            pos = ((gradient_img.size[0] - logo.size[0]) // 2, (gradient_img.size[1] - logo.size[1]) // 2)
            
            # 创建圆形蒙版
            mask = Image.new("L", logo.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(1))
            
            # 将Logo粘贴到二维码上
            gradient_img.paste(logo, pos, mask)
        except Exception as e:
            print(f"添加Logo时出错: {e}")

    # 保存图像
    if isinstance(output_file, str):
        gradient_img.save(output_file)
    else:
        gradient_img.save(output_file, format='PNG')
    return output_file

# 使用示例
if __name__ == "__main__":
    print("正在生成美化二维码...")
    
    # 测试链接，包括短链接和长链接
    short_url = "https://bzgcaishui.com/"
    long_url = "https://bzgcaishui.com/"
    
    # 使用长链接生成二维码
    url_to_use = long_url
    
    # 标准美化二维码示例
    generate_styled_qr_code(
        url_to_use, 
        output_file="styled_qrcode.png",
        color="#1E88E5",  # 蓝色
        style="rounded",
        img_size=(350, 350),
        auto_adjust=True
    )
    print("圆角二维码已生成: styled_qrcode.png")
    
    # 圆形二维码示例
    generate_styled_qr_code(
        url_to_use, 
        output_file="circle_qrcode.png",
        color="#8BC34A",  # 绿色
        style="circle",
        img_size=(350, 350),
        auto_adjust=True
    )
    print("圆形二维码已生成: circle_qrcode.png")
    
    # 渐变二维码示例
    generate_gradient_qr(
        url_to_use,
        output_file="gradient_qrcode.png", 
        start_color="#FF5722",  # 橙色
        end_color="#9C27B0",  # 紫色
        img_size=(350, 350),
        auto_adjust=True
    )
    print("渐变二维码已生成: gradient_qrcode.png")
    
    # 橙色圆形点二维码
    generate_styled_qr_code(
        url_to_use, 
        output_file="orange_circle_qrcode.png",
        color="#FF5722",  # 橙色
        style="circle",
        img_size=(350, 350),
        auto_adjust=True
    )
    print("橙色圆形二维码已生成: orange_circle_qrcode.png")
    
    print("所有二维码生成完成!") 