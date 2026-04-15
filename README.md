<p align="center">
  <img src="https://img.shields.io/badge/version-2.1-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python-3.10+-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" />
</p>

<h1 align="center">🔍 CodeFilter — Code / Password Filter</h1>

<p align="center">
  Fast wordlist filter for digital forensics and password recovery workflows.<br>
  Filter large TXT wordlists by length, character type, regex and more.
</p>

---

## 🧑‍💼 Author

**Krystian Zarzecki**  
President of the Board — Wezafon Sp. z o.o. (brand: **Laboratorium Elektroniki**)  
Court-Appointed Expert in Digital Forensics & Teleinformatics  
District Court in Tarnobrzeg, Poland

🌐 [laboratorium-elektroniki.pl](https://laboratorium-elektroniki.pl)  
📘 [facebook.com/LaboratoriumElektroniki](https://facebook.com/LaboratoriumElektroniki)  
🐙 [github.com/studiogsm](https://github.com/studiogsm)

---

## ✨ Features

### 📐 Length Filter
- Any length
- Exact number of characters
- Range: min–max

### 🔤 Character Type
- Any
- Digits only
- Letters only
- Alphanumeric
- Lowercase only
- Uppercase only

### ✅ Additional Conditions (checkboxes)
- Must contain a digit
- Must contain an uppercase letter
- Must contain a special character
- No special characters

### ⚙️ Advanced Options
- Remove duplicates
- Case conversion: unchanged / lowercase / UPPERCASE
- Add prefix and/or suffix to every line
- Regex filter (for advanced patterns)

### 👁️ Preview
- Preview first 50 matching lines before saving

### 📁 Smart Output Path
- After loading `wordlist.txt`, the output path is automatically set to `wordlist_filtered.txt` in the same directory — no extra clicking needed

---

## 🌐 Languages

10 interface languages: **PL / EN / ES / FR / IT / DE / PT / NL / RU / UA**

---

## ⚡ Performance

Optimized for large files (>1 GB wordlists):
- File read with 1 MB buffer (not line-by-line)
- Binary line counting (instant even for huge files)
- GUI updates every 50,000 matches instead of every line
- Fastest filters (length, type) checked first — regex checked last

---

## 🖥️ Usage

### Workflow
1. **Generate** a large wordlist (e.g. with a wordlist generator)
2. **Load** the TXT file in CodeFilter
3. **Set** filter rules
4. **Click FILTER** → get a smaller, targeted output file
5. **Use** the output with Hashcat, BruteStorm, or other recovery tools

---

## 📦 Requirements

- **Python 3.10+**
- `tkinter` — included with standard Python on Windows
- No external packages required

---

## 🔨 Build (compile to Windows EXE)

Place all files in one folder and run:

```
build_filter.bat
```

The script installs PyInstaller automatically if not present.  
Output: `dist\CodeFilter.exe`

### Required files:
```
code_filter.py      ← application source
build_filter.bat    ← build script
icon.ico            ← application icon (place your own or use provided)
```

> If you have your own `icon.ico`, just place it in the same folder — the build script detects and uses it automatically.

---

## 📋 Version History

| Version | Changes |
|---|---|
| **v2.1** | Light theme (professional white/blue UI), Segoe UI font, improved layout |
| **v2.0** | Performance optimization (1 MB buffer), auto output path, branding, icon support |
| **v1.0** | Initial release — length, type, regex, prefix/suffix, dedup, 10 languages |

---

## ⚖️ License

MIT License — free to use, modify and distribute.

---

© 2025 Krystian Zarzecki / Laboratorium Elektroniki
