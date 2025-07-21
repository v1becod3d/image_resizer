import os
from PIL import Image

# Size templates
PRESETS = {
    '1': (1920, 1080),  # Full HD
    '2': (1000, 1000),  # Square
    '3': "custom"       # Custom size
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
        print(f"✓ Image saved: {output_path}")
    except Exception as e:
        print(f"✗ Error: {e}")

def get_target_size():
    print("\nChoose a template or enter size manually:")
    print("1: 1920×1080 (Full HD)")
    print("2: 1000×1000 (Square)")
    print("3: Enter custom size")
    
    choice = input("Your choice (1/2/3): ").strip()
    if choice not in PRESETS:
        print("✗ Invalid choice. Using 1920×1080.")
        return PRESETS['1']
    
    if PRESETS[choice] == "custom":
        while True:
            try:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                return (width, height)
            except ValueError:
                print("✗ Error: please enter numbers!")
    else:
        return PRESETS[choice]

def get_unique_filename(path):
    """Generates a unique filename with a numeric suffix (e.g., _1, _2)."""
    base, ext = os.path.splitext(path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def main():
    print("=== Resize Image Tool ===")
    print("Enter the full path to the image:")
    input_path = input().strip('"')
    
    if not os.path.exists(input_path):
        print("✗ File not found!")
        return
    
    target_size = get_target_size()
    stretch = input("Stretch without maintaining proportions? (y/n, default y): ").strip().lower()
    stretch = stretch != 'n'
    
    dir_path = os.path.dirname(input_path)
    filename, ext = os.path.splitext(os.path.basename(input_path))
    output_path = os.path.join(dir_path, f"{filename}_resized{ext}")
    
    if os.path.exists(output_path):
        print("\n⚠ File already exists. Choose an action:")
        print("1: Overwrite existing file")
        print("2: Save with a new name (e.g., _resized_1)")
        print("3: Do not save")
        
        choice = input("Your choice (1/2/3): ").strip()
        if choice == '1':
            pass  # Overwrite
        elif choice == '2':
            output_path = get_unique_filename(output_path)
        elif choice == '3':
            print("Cancelled.")
            return
        else:
            print("✗ Invalid choice. Cancelled.")
            return
    
    resize_image(input_path, output_path, target_size, stretch)

if __name__ == "__main__":
    main()