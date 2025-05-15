import os
import zipfile
import shutil
from PIL import Image
from pathlib import Path
import fitz  # PyMuPDF
import io

# ----------------------------
# Funções auxiliares
# ----------------------------

def limpar_pasta(pasta):
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(caminho):
                os.remove(caminho)
            elif os.path.isdir(caminho):
                shutil.rmtree(caminho)
        except Exception as e:
            print(f"Erro ao limpar {caminho}: {e}")

def tem_zips(pasta):
    return any(arquivo.lower().endswith('.zip') for arquivo in os.listdir(pasta))

def tem_imagens(pasta):
    return any(arquivo.lower().endswith(('.png', '.jpg', '.jpeg')) for arquivo in os.listdir(pasta))

def obter_arquivo_mais_recente(pasta):
    arquivos = list(Path(pasta).glob("*.pdf"))
    if not arquivos:
        return None
    return max(arquivos, key=lambda f: f.stat().st_mtime)

def extract_images_from_pdf(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    imagem_extraida = False

    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_ext = base_image["ext"]

            img_path = os.path.join(output_folder, f"page_{i+1}_img_{img_index+1}.jpg")

            if img_ext.lower() != "jpg":
                image = Image.open(io.BytesIO(image_bytes))
                image.convert("RGB").save(img_path, "JPEG")
            else:
                with open(img_path, "wb") as f:
                    f.write(image_bytes)

            print(f"Imagem extraída do PDF: {img_path}")
            imagem_extraida = True

    return imagem_extraida

# ----------------------------
# Pastas
# ----------------------------

zip_folder = r"C:\pythonnew\python\zips"
input_folder = r"C:\pythonnew\python\imagens"
output_folder = r"C:\pythonnew\python\imagens_marcadas"
watermark_path = r"C:\pythonnew\python\marca_dagua.png\Exho preto.png"
pasta_pdfs = r"C:\pythonnew\python\pdf_file"

os.makedirs(zip_folder, exist_ok=True)
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# ----------------------------
# 1. Processar PDF (se existir)
# ----------------------------

pdf_file = obter_arquivo_mais_recente(pasta_pdfs)
if pdf_file:
    print(f"Processando arquivo PDF: {pdf_file}")
    sucesso = extract_images_from_pdf(str(pdf_file), input_folder)
    if not sucesso:
        print("Nenhuma imagem foi extraída do PDF.")
else:
    print("Nenhum arquivo PDF encontrado na pasta.")

# ----------------------------
# 2. Extrair imagens dos ZIPs
# ----------------------------

if tem_zips(zip_folder):
    for nome_arquivo in os.listdir(zip_folder):
        if nome_arquivo.lower().endswith('.zip'):
            caminho_zip = os.path.join(zip_folder, nome_arquivo)
            try:
                with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                    zip_ref.extractall(input_folder)
                    print(f"Extraído do ZIP: {nome_arquivo}")
            except Exception as e:
                print(f"Erro ao extrair {nome_arquivo}: {e}")

# ----------------------------
# 3. Verifica se há imagens na pasta input_folder
# ----------------------------

if not tem_imagens(input_folder):
    print("A pasta de imagens está vazia. Limpando imagens_marcadas...")
    limpar_pasta(output_folder)
    print("Pasta imagens_marcadas foi limpa.")
else:
    # Adicione esta linha para regular a transparência da marca d'água
    watermark_transparency = 128  # Valor entre 0 (transparente) e 255 (opaco)

    # Tenta abrir a marca d'água
    try:
        watermark = Image.open(watermark_path).convert("RGBA")
        # Ajusta a transparência da marca d'água
        alpha = watermark.split()[3]  # Obtém o canal alpha
        alpha = alpha.point(lambda p: p * (watermark_transparency / 255))
        watermark.putalpha(alpha)
    except PermissionError as e:
        print(f"Erro de permissão ao acessar o arquivo de marca d'água: {e}")
        exit(1)

    # Processa imagens
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            try:
                image = Image.open(image_path).convert("RGBA")

                wm_width = int(image.width * 0.4)
                wm_height = int((wm_width / watermark.width) * watermark.height)
                watermark_resized = watermark.resize((wm_width, wm_height), Image.LANCZOS)

                pos_x = (image.width - wm_width) // 2
                pos_y = (image.height - wm_height) // 2

                image.paste(watermark_resized, (pos_x, pos_y), watermark_resized)

                output_path = os.path.join(output_folder, filename)
                image.convert("RGB").save(output_path, "JPEG", quality=95)
                print(f"Marca d'água adicionada em: {filename}")
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

    print("Processo de marca d’água concluído!")

# ----------------------------
# Parte final: Menu de limpeza
# ----------------------------

def menu_limpeza():
    print("\n--- MENU DE LIMPEZA ---")
    print("1 - Limpar: pdf_file, imagens, imagens_marcadas")
    print("2 - Limpar: imagens, imagens_marcadas, zips")
    print("0 - Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        print("\nLimpando pdf_file, imagens e imagens_marcadas...")
        limpar_pasta(r"C:\pythonnew\python\pdf_file")
        limpar_pasta(r"C:\pythonnew\python\imagens")
        limpar_pasta(r"C:\pythonnew\python\imagens_marcadas")
        print("Limpeza concluída.")
    elif escolha == "2":
        print("\nLimpando imagens, imagens_marcadas e zips...")
        limpar_pasta(r"C:\pythonnew\python\imagens")
        limpar_pasta(r"C:\pythonnew\python\imagens_marcadas")
        limpar_pasta(r"C:\pythonnew\python\zips")
        print("Limpeza concluída.")
    elif escolha == "0":
        print("Encerrando menu.")
    else:
        print("Opção inválida.")

# Chamada do menu somente após execução principal
menu_limpeza()