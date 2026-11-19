import os
from PIL import Image

dest_dir = r"C:\googleebook\website\public\images\covers"

mapping = [
    # Afrikaans Die Swart Luiperd Reeks
    ("AF 1", "GEMASKERDE MOORDENAARS", "cover_125.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\DIE SWART LUIPERD REEKS - AFRIKAANS\1. GEMASKERDE MOORDENAARS\SQRIBBLE\1. Thumbnail.jpg"),
    ("AF 2", "DIE MENSVRETERS VAN TSAWO", "cover_99.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\DIE SWART LUIPERD REEKS - AFRIKAANS\2. DIE MENSVRETERS VAN TSAWO\SQRIBBLE\2. Thumbnail.jpg"),
    ("AF 3", "DIE BLOEDBOODSKAP", "cover_98.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\DIE SWART LUIPERD REEKS - AFRIKAANS\3. DIE BLOEDBOODSKAP\SQRIBBLE\3. Thumbnail.jpg"),
    ("AF 4", "KAMERADE VAN DIE DRAAK", "cover_97.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\DIE SWART LUIPERD REEKS - AFRIKAANS\4. KAMERADE VAN DIE DRAAK\SQRIBBLE\4. Thumbnail.jpg"),
    ("AF 5", "DIE KRUIPENDE DOOD", "cover_96.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\DIE SWART LUIPERD REEKS - AFRIKAANS\5. DIE KRUIPENDE DOOD\SQRIBBLE\5. Thumbnail.jpg"),
    ("AF 6", "DIE GALG IN DIE OERWOUD", "cover_95.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\DIE SWART LUIPERD REEKS - AFRIKAANS\6. DIE GALG IN DIE OERWOUD\SQRIBBLE\6. Thumbnail.jpg"),

    # English The Black Leopard Series
    ("EN 1", "MASKED MURDERERS", "cover_13.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\THE BLACK LEOPARD SERIES - ENGLISH\1. MASKED MURDERERS\SQRIBBLE\1. Thumbnail.jpg"),
    ("EN 2", "THE MANEATERS OF TSAVO", "cover_12.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\THE BLACK LEOPARD SERIES - ENGLISH\2. THE MANEATERS OF TSAVO\SQRIBBLE\2. Thumbnail.jpg"),
    ("EN 3", "THE BLOOD MESSAGE", "cover_11.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\THE BLACK LEOPARD SERIES - ENGLISH\3. THE BLOOD MESSAGE\SQRIBBLE\3. Thumbnail.jpg"),
    ("EN 4", "COMRADES OF THE DRAGON", "cover_10.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\THE BLACK LEOPARD SERIES - ENGLISH\4. COMRADES OF THE DRAGON\SQRIBBLE\4. Thumbnail.jpg"),
    ("EN 5", "THE CREEPING DEATH", "cover_9.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\THE BLACK LEOPARD SERIES - ENGLISH\5. THE CREEPING DEATH\SQRIBBLE\5. Thumbnail.jpg"),
    ("EN 6", "THE GALLOWS IN THE JUNGLE", "cover_8.jpg",
     r"C:\YOUTUBE - BOOKS WITH HOOKS\SWART LUIPERD REEKS\THE BLACK LEOPARD SERIES - ENGLISH\6. THE GALLOWS IN THE JUNGLE\SQRIBBLE\6. Thumbnail.jpg"),
]

print("Updating 12 book covers in c:\\googleebook\\website\\public\\images\\covers...")
for tag, title, filename, src_path in mapping:
    assert os.path.exists(src_path), f"Source missing: {src_path}"
    
    out_path = os.path.join(dest_dir, filename)
    old_size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    
    im = Image.open(src_path)
    # Convert to RGB if needed
    if im.mode != 'RGB':
        im = im.convert('RGB')
        
    # Resize to (600, 960) with Lanczos high quality resampling
    # 600x960 gives excellent crispness on high-DPI displays and remains well-optimized
    im_resized = im.resize((600, 960), Image.Resampling.LANCZOS)
    im_resized.save(out_path, "JPEG", quality=82, optimize=True)
    
    new_size = os.path.getsize(out_path)
    print(f"[{tag}] {title} -> {filename} | Old: {old_size} bytes -> New: {new_size} bytes (600x960, Q82)")

print("\nAll 12 covers updated successfully!")
