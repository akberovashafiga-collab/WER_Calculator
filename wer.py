from pathlib import Path
import re


def tokenize(text: str) -> list[str]:
  """Токенізація тексту: вилучає слова з урахуванням української та англійської мов."""
  return re.findall(r"[a-zA-Zа-щьюяєіїґА-ЩЬЮЯЄІЇҐ'’]+", text.lower())


def calculate_wer(reference_text: str, hypothesis_text: str) -> dict:
  """Обчислює Word Error Rate (WER) та метрики N, S, D, I за формулою:

  WER = (S + D + I) / N
  """
  ref_words = tokenize(reference_text)
  hyp_words = tokenize(hypothesis_text)

  n = len(ref_words)
  m = len(hyp_words)

  # Створення матриці для динамічного програмування
  d = [[0] * (m + 1) for _ in range(n + 1)]
  for i in range(n + 1):
    d[i][0] = i
  for j in range(m + 1):
    d[0][j] = j

  for i in range(1, n + 1):
    for j in range(1, m + 1):
      if ref_words[i - 1] == hyp_words[j - 1]:
        d[i][j] = d[i - 1][j - 1]
      else:
        substitution = d[i - 1][j - 1] + 1
        deletion = d[i - 1][j] + 1
        insertion = d[i][j - 1] + 1
        d[i][j] = min(substitution, deletion, insertion)

  # Зворотний прохід (Backtracking) для підрахунку S, D, I
  i, n_idx = n, m
  s, dele, ins = 0, 0, 0

  while i > 0 or n_idx > 0:
    if i > 0 and n_idx > 0 and ref_words[i - 1] == hyp_words[n_idx - 1]:
      i -= 1
      n_idx -= 1
    else:
      sub_val = d[i - 1][n_idx - 1] if i > 0 and n_idx > 0 else float("inf")
      del_val = d[i - 1][n_idx] if i > 0 else float("inf")
      ins_val = d[i][n_idx - 1] if n_idx > 0 else float("inf")

      min_val = min(sub_val, del_val, ins_val)

      if min_val == sub_val:
        s += 1
        i -= 1
        n_idx -= 1
      elif min_val == del_val:
        dele += 1
        i -= 1
      else:
        ins += 1
        n_idx -= 1

  wer_value = (s + dele + ins) / n if n > 0 else 0.0

  return {
      "N": n,
      "S": s,
      "D": dele,
      "I": ins,
      "WER": round(wer_value, 4),
  }