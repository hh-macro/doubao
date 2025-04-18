import cv2

# 加载图片
image_path = r"D:\aresult\2025-4-17\timu\file_aliyun@1bb2e6e8-c183-4ff8-b215-aa646c6d918f-8158.jpg"
image = cv2.imread(image_path)

# 确保图片已成功加载
if image is None:
    print(f"Error: Could not load image from {image_path}")
    exit()

# 获取图片的宽度和高度
height, width = image.shape[:2]

# 定义坐标点
coordinates = [
    (50002, 984188),
    (50002, 914527),
    (50002, 246931),
    (50002, 975823)
]

# 遍历每个坐标点并裁剪保存
for i, (x, y) in enumerate(coordinates):
    # 确保坐标点在图片范围内
    x = max(0, min(x, width - 1))
    y = max(0, min(y, height - 1))

    # 定义裁剪区域（例如，以坐标点为中心的 100x100 区域）
    crop_width = 100
    crop_height = 100
    x_start = max(0, x - crop_width // 2)
    y_start = max(0, y - crop_height // 2)
    x_end = min(width, x + crop_width // 2)
    y_end = min(height, y + crop_height // 2)

    # 确保裁剪区域的宽度和高度至少为1像素
    if x_end <= x_start or y_end <= y_start:
        print(f"Warning: Cropped area for coordinate ({x}, {y}) is invalid.")
        continue

    # 裁剪区域
    cropped_image = image[y_start:y_end, x_start:x_end]

    # 保存裁剪后的图片
    filename = f"cropped_area_{i + 1}.jpg"
    cv2.imwrite(filename, cropped_image)
    print(f"裁剪后的图片已保存为 {filename}")

print("所有裁剪操作完成")