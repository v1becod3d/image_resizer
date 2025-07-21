import os
from PIL import Image

# Size templates
PRESETS = {
    '1': (1920, 1080),  # Full HD
    '2': (1000, 1000),  # Square
    '3': "custom"       # custom
}

def resize_image(input_path, output_path, target_size, stretch=True):
    try:
        img = Image.open(input_path)
        
        if stretch:
            img_resized = img.resize(target_size, Image.LANCZOS)
        else:
            img.thumbnail((target_size[0], target_size[1] * 2), Image.LANCZOS)
            img_resized = Image.new("RGB", target_size, (0, 0, 0))
            img_resized.paste(img, (
                (target_size[0] - img.width) // 2,
                (target_size[1] - img.height) // 2
            ))
        
        img_resized.save(output_path)
        print(f"✓ Изображение сохранено: {output_path}")
    except Exception as e:
        print(f"✗ Ошибка: {e}")

def get_target_size():
    print("\nВыберите шаблон или введите размер вручную:")
    print("1: 1920×1080 (Full HD)")
    print("2: 1000×1000 (Квадрат)")
    print("3: Указать вручную")
    
    choice = input("Ваш выбор (1/2/3): ").strip()
    if choice not in PRESETS:
        print("✗ Неверный выбор. Используется 1920×1080.")
        return PRESETS['1']
    
    if PRESETS[choice] == "custom":
        while True:
            try:
                width = int(input("Введите ширину: "))
                height = int(input("Введите высоту: "))
                return (width, height)
            except ValueError:
                print("✗ Ошибка: введите числа!")
    else:
        return PRESETS[choice]

def get_unique_filename(path):
    """Генерирует уникальное имя файла с числовым суффиксом (например, _1, _2)."""
    base, ext = os.path.splitext(path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def main():
    print("=== Resize Image Tool ===")
    print("Введите полный путь к изображению:")
    input_path = input().strip('"')
    
    if not os.path.exists(input_path):
        print("✗ Файл не найден!")
        return
    
    target_size = get_target_size()
    stretch = input("Растянуть без сохранения пропорций? (y/n, по умолчанию y): ").strip().lower()
    stretch = stretch != 'n'
    
    dir_path = os.path.dirname(input_path)
    filename, ext = os.path.splitext(os.path.basename(input_path))
    output_path = os.path.join(dir_path, f"{filename}_resized{ext}")
    
    if os.path.exists(output_path):
        print("\n⚠ Файл уже существует. Выберите действие:")
        print("1: Перезаписать существующий файл")
        print("2: Сохранить с новым именем (например, _resized_1)")
        print("3: Не сохранять")
        
        choice = input("Ваш выбор (1/2/3): ").strip()
        if choice == '1':
            pass  # Перезаписываем
        elif choice == '2':
            output_path = get_unique_filename(output_path)
        elif choice == '3':
            print("Отменено.")
            return
        else:
            print("✗ Неверный выбор. Отменено.")
            return
    
    resize_image(input_path, output_path, target_size, stretch)

if __name__ == "__main__":
    main()