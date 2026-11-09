import json
from pathlib import Path
from wer import calculate_wer


def main():
  ref_path = Path("reference.txt")
  hyp_path = Path("hypothesis.txt")

  if not ref_path.exists() or not hyp_path.exists():
    print("Помилка: Файли текстів не знайдено!")
    return

  ref_text = ref_path.read_text(encoding="utf-8")
  hyp_text = hyp_path.read_text(encoding="utf-8")

  metrics = calculate_wer(ref_text, hyp_text)

  output_path = Path("wer_results.json")
  output_path.write_text(
      json.dumps(metrics, ensure_ascii=False, indent=4), encoding="utf-8"
  )

  print("=== Результати обчислення WER ===")
  for key, value in metrics.items():
    print(f"  {key}: {value}")
  print(f"\n[успішно] Результати збережено у файл '{output_path.name}'")


if __name__ == "__main__":
  main()