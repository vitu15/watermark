import os
watermark_path = r"C:\python\marca_dagua.png"

if os.path.exists(watermark_path):
    print("Arquivo encontrado!")
else:
    print("Arquivo NÃO encontrado!")
