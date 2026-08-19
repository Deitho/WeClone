import json
import os
import re

input_file = "data.txt"
output_dir = "./dataset/res_csv/sft"
os.makedirs(output_dir, exist_ok=True)


def clean_letter_text(text: str) -> str:
    """Metin içindeki gereksiz boşluk ve hatalı new-line'ları temizler."""
    if not text:
        return ""

    # 1. Her satırın sağındaki gereksiz boşlukları temizle
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = "\n".join(lines)

    # 2. 3 veya daha fazla üst üste gelen satır başını standart 2 satır başına (\n\n) indir
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # 3. Metnin başındaki ve sonundaki tüm boşluk/satır başlarını temizle
    return cleaned.strip()


dataset = []

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"GELEN:\s*(.*?)\s*---+\s*MEKTUP\s*---+\s*CEVAP:\s*(.*?)\s*---+\s*MEKTUP\s*---+"
matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

for gelen_raw, cevap_raw in matches:
    gelen_clean = clean_letter_text(gelen_raw)
    cevap_clean = clean_letter_text(cevap_raw)

    if gelen_clean and cevap_clean:
        dataset.append(
            {
                "messages": [
                    {"from": "user", "value": gelen_clean},
                    {"from": "assistant", "value": cevap_clean},
                ]
            }
        )

output_path = os.path.join(output_dir, "chat-sft.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(
    f"Toplam {len(dataset)} adet mektup çifti temizlenerek 'chat-sft.json' dosyasına aktarıldı."
)