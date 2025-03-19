from PIL import Image, ImageDraw, ImageFont
import os

# Pastas de entrada e saída
input_folder = r"C:\python\imagens"  # Pasta onde estão as imagens originais
output_folder = r"C:\python\imagens_marcadas"  # Pasta onde serão salvas as imagens editadas
watermark_path = r"C:\python\marca_dagua.png\test-watermark-on-a-transparent-background-free-png.webp"  # Caminho para a imagem da marca d'água

# Criar pasta de saída se não existir
os.makedirs(output_folder, exist_ok=True)

try:
    # Carregar a marca d'água
    watermark = Image.open(watermark_path).convert("RGBA")
except PermissionError as e:
    print(f"Erro de permissão ao acessar o arquivo de marca d'água: {e}")
    exit(1)

# Loop pelas imagens da pasta de entrada
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGBA")

        # Redimensiona a marca d'água para x.x% do tamanho da imagem original
        wm_width = int(image.width * 1.0)
        wm_height = int((wm_width / watermark.width) * watermark.height)
        watermark_resized = watermark.resize((wm_width, wm_height), Image.LANCZOS)

        # Define posição da marca d'água (centro da imagem)
        pos_x = (image.width - wm_width) // 2
        pos_y = (image.height - wm_height) // 2

        # Adiciona a marca d'água na imagem
        image.paste(watermark_resized, (pos_x, pos_y), watermark_resized)

        # Salva a imagem editada
        output_path = os.path.join(output_folder, filename)
        image.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Marca d'água adicionada em: {filename}")

print("Processo concluído!")
