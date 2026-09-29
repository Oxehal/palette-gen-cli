# palette-gen-cli
Lightweight CLI tool for generating harmonious UI color palettes and CSS gradients from any base HEX.

Markdown
# 🎨 PaletteGen CLI

Легковесная консольная утилита для генерации гармоничных цветовых палитр и CSS-градиентов по базовому HEX-коду.

Построена на базе цветового пространства **HLS** (`colorsys`), без сторонних зависимостей.

---

## ⚡ Особенности
- **4 схемы гармонии**: комплементарная, аналоговая, триада и монохромный спектр.
- **Готовые CSS-переменные**: генерация блока `:root` с переменными и градиентами через флаг `--css`.
- **Zero Dependencies**: работает на чистом Python 3.

---

## 🚀 Использование

### 1. Быстрый просмотр HEX-палитры
```bash
python main.py
Или передай свой цвет:

Bash
python main.py "#3B82F6"
Вывод:

Plaintext
🎨 Base Color: #3B82F6
────────────────────────────────────
Complementary : #3B82F6 → #F6AF3B
Analogous     : #3B5CF6 → #3B82F6 → #3BD5F6
Triadic       : #3B82F6 → #F63B82 → #82F63B
Monochrome    : #D7E6FD → #96BEFA → #3B82F6 → #104AB3 → #08255A
CSS Gradient  : linear-gradient(135deg, #3B82F6, #F6AF3B)
────────────────────────────────────
2. Экспорт готового CSS
Bash
python main.py "#6366F1" --css
Результат:

CSS
:root {
  --color-primary: #6366F1;
  --color-mono-100: #E6E7FD;
  --color-mono-200: #AEB2FA;
  --color-mono-300: #6366F1;
  --color-mono-400: #2226B2;
  --color-mono-500: #111359;
  --color-analogous-1: #8C63F1;
  --color-analogous-2: #6366F1;
  --color-analogous-3: #63A3F1;
  --color-triadic-1: #6366F1;
  --color-triadic-2: #F16366;
  --color-triadic-3: #66F163;
  --gradient-accent: linear-gradient(135deg, #6366F1 0%, #F1EE63 100%);
  --gradient-soft: linear-gradient(180deg, #AEB2FA 0%, #6366F1 100%);
}
