import cv2
import numpy as np

def findcentroid(image):
    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用阈值法将图像二值化
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 计算图像的质心
    M = cv2.moments(binary_image)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        # 如果图像没有前景，则使用图像中心
        cX, cY = image.shape[1] // 2, image.shape[0] // 2

    return (cX, cY)

def crop_square(image, center, side_length):
    cX, cY = center
    half_side = side_length // 2

    start_x = max(cX - half_side, 0)
    start_y = max(cY - half_side, 0)
    end_x = min(cX + half_side, image.shape[1])
    end_y = min(cY + half_side, image.shape[0])

    # 调整截图区域为正方形
    crop_width = end_x - start_x
    crop_height = end_y - start_y
    if crop_width != crop_height:
        diff = abs(crop_width - crop_height)
        if crop_width > crop_height:
            end_y = min(end_y + diff, image.shape[0])
        else:
            end_x = min(end_x + diff, image.shape[1])

    return image[start_y:end_y, start_x:end_x]

# 加载图片
image = cv2.imread('./images/makeup/frame_0030.jpg')

# 找到图像的质心
center = findcentroid(image)

# 设置正方形的边长
side_length = 200  # 根据需要调整边长

# 截图
cropped_image = crop_square(image, center, side_length)

# 显示截图结果
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
