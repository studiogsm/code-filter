"""
Code / Password Filter v2.1
Laboratorium Elektroniki | laboratoriumelektroniki.pl
Author: Krystian Zarzecki
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, re, threading, sys

# ── ICON HELPER ───────────────────────────────────────────────────────────────
def set_icon(root):
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    ico = os.path.join(base, "icon.ico")
    if os.path.exists(ico):
        try:
            root.iconbitmap(ico)
        except Exception:
            pass

# ── TRANSLATIONS ──────────────────────────────────────────────────────────────
LANGUAGES = {
    "EN": "English", "PL": "Polski", "ES": "Español", "FR": "Français",
    "IT": "Italiano", "DE": "Deutsch", "PT": "Português", "NL": "Nederlands",
    "RU": "Русский", "UA": "Українська",
}

T = {
    "title":        {"EN":"CODE / PASSWORD FILTER","PL":"FILTR KODÓW / HASEŁ","ES":"FILTRO DE CÓDIGOS","FR":"FILTRE DE CODES","IT":"FILTRO CODICI","DE":"CODE-FILTER","PT":"FILTRO DE CÓDIGOS","NL":"CODE FILTER","RU":"ФИЛЬТР КОДОВ","UA":"ФІЛЬТР КОДІВ"},
    "subtitle":     {"EN":"Filter wordlist lines by rules  |  Laboratorium Elektroniki","PL":"Filtruj linie słownika według reguł  |  Laboratorium Elektroniki","ES":"Filtra líneas del diccionario  |  Laboratorium Elektroniki","FR":"Filtrer les lignes du dictionnaire  |  Laboratorium Elektroniki","IT":"Filtra righe del dizionario  |  Laboratorium Elektroniki","DE":"Wörterbuch-Zeilen filtern  |  Laboratorium Elektroniki","PT":"Filtrar linhas do dicionário  |  Laboratorium Elektroniki","NL":"Woordenboekregels filteren  |  Laboratorium Elektroniki","RU":"Фильтр строк словаря  |  Laboratorium Elektroniki","UA":"Фільтр рядків словника  |  Laboratorium Elektroniki"},
    "input_frame":  {"EN":"Input File","PL":"Plik wejściowy","ES":"Archivo de entrada","FR":"Fichier d'entrée","IT":"File di input","DE":"Eingabedatei","PT":"Arquivo de entrada","NL":"Invoerbestand","RU":"Входной файл","UA":"Вхідний файл"},
    "browse":       {"EN":"Browse…","PL":"Wybierz…","ES":"Examinar…","FR":"Parcourir…","IT":"Sfoglia…","DE":"Durchsuchen…","PT":"Procurar…","NL":"Bladeren…","RU":"Обзор…","UA":"Огляд…"},
    "lines_found":  {"EN":"Lines in file:","PL":"Linii w pliku:","ES":"Líneas en archivo:","FR":"Lignes dans fichier:","IT":"Righe nel file:","DE":"Zeilen in Datei:","PT":"Linhas no arquivo:","NL":"Regels in bestand:","RU":"Строк в файле:","UA":"Рядків у файлі:"},
    "output_frame": {"EN":"Output File","PL":"Plik wynikowy","ES":"Archivo de salida","FR":"Fichier de sortie","IT":"File di output","DE":"Ausgabedatei","PT":"Arquivo de saída","NL":"Uitvoerbestand","RU":"Выходной файл","UA":"Вихідний файл"},
    "save_as":      {"EN":"Save as…","PL":"Zapisz jako…","ES":"Guardar como…","FR":"Enregistrer sous…","IT":"Salva come…","DE":"Speichern als…","PT":"Salvar como…","NL":"Opslaan als…","RU":"Сохранить как…","UA":"Зберегти як…"},
    "filter_frame": {"EN":"Filter Rules","PL":"Reguły filtrowania","ES":"Reglas de filtrado","FR":"Règles de filtrage","IT":"Regole di filtro","DE":"Filterregeln","PT":"Regras de filtragem","NL":"Filterregels","RU":"Правила фильтрации","UA":"Правила фільтрації"},
    "len_label":    {"EN":"Length:","PL":"Długość:","ES":"Longitud:","FR":"Longueur:","IT":"Lunghezza:","DE":"Länge:","PT":"Comprimento:","NL":"Lengte:","RU":"Длина:","UA":"Довжина:"},
    "len_any":      {"EN":"Any","PL":"Dowolna","ES":"Cualquiera","FR":"N'importe","IT":"Qualsiasi","DE":"Beliebig","PT":"Qualquer","NL":"Willekeurig","RU":"Любая","UA":"Будь-яка"},
    "len_exact":    {"EN":"Exact:","PL":"Dokładnie:","ES":"Exacto:","FR":"Exactement:","IT":"Esatto:","DE":"Genau:","PT":"Exato:","NL":"Exact:","RU":"Точно:","UA":"Точно:"},
    "len_range":    {"EN":"Range:","PL":"Zakres:","ES":"Rango:","FR":"Plage:","IT":"Intervallo:","DE":"Bereich:","PT":"Faixa:","NL":"Bereik:","RU":"Диапазон:","UA":"Діапазон:"},
    "len_to":       {"EN":"to","PL":"do","ES":"a","FR":"à","IT":"a","DE":"bis","PT":"a","NL":"tot","RU":"до","UA":"до"},
    "char_label":   {"EN":"Characters:","PL":"Znaki:","ES":"Caracteres:","FR":"Caractères:","IT":"Caratteri:","DE":"Zeichen:","PT":"Caracteres:","NL":"Tekens:","RU":"Символы:","UA":"Символи:"},
    "char_any":     {"EN":"Any","PL":"Dowolne","ES":"Cualquiera","FR":"N'importe","IT":"Qualsiasi","DE":"Beliebig","PT":"Qualquer","NL":"Willekeurig","RU":"Любые","UA":"Будь-які"},
    "char_digits":  {"EN":"Digits only","PL":"Tylko cyfry","ES":"Solo dígitos","FR":"Chiffres seul.","IT":"Solo cifre","DE":"Nur Ziffern","PT":"Só dígitos","NL":"Alleen cijfers","RU":"Только цифры","UA":"Тільки цифри"},
    "char_alpha":   {"EN":"Letters only","PL":"Tylko litery","ES":"Solo letras","FR":"Lettres seul.","IT":"Solo lettere","DE":"Nur Buchstaben","PT":"Só letras","NL":"Alleen letters","RU":"Только буквы","UA":"Тільки букви"},
    "char_alnum":   {"EN":"Alphanumeric","PL":"Alfanumeryczne","ES":"Alfanumérico","FR":"Alphanumérique","IT":"Alfanumerico","DE":"Alphanumerisch","PT":"Alfanumérico","NL":"Alfanumeriek","RU":"Буквенно-цифр.","UA":"Буквено-цифр."},
    "char_lower":   {"EN":"Lowercase only","PL":"Tylko małe","ES":"Solo minúsc.","FR":"Minuscules seul.","IT":"Solo minusc.","DE":"Nur Klein","PT":"Só minúsc.","NL":"Alleen klein","RU":"Только строчн.","UA":"Тільки малі"},
    "char_upper":   {"EN":"Uppercase only","PL":"Tylko wielkie","ES":"Solo mayúsc.","FR":"Majuscules seul.","IT":"Solo maiusc.","DE":"Nur Groß","PT":"Só maiúsc.","NL":"Alleen groot","RU":"Только заглавн.","UA":"Тільки великі"},
    "cond_frame":   {"EN":"Additional Conditions","PL":"Warunki dodatkowe","ES":"Condiciones adicionales","FR":"Conditions supplémentaires","IT":"Condizioni aggiuntive","DE":"Zusatzbedingungen","PT":"Condições adicionais","NL":"Extra voorwaarden","RU":"Доп. условия","UA":"Дод. умови"},
    "has_digit":    {"EN":"Must contain digit","PL":"Musi zawierać cyfrę","ES":"Debe tener dígito","FR":"Doit avoir chiffre","IT":"Deve avere cifra","DE":"Muss Ziffer haben","PT":"Deve ter dígito","NL":"Moet cijfer hebben","RU":"Должно быть число","UA":"Мусить мати цифру"},
    "has_upper":    {"EN":"Must contain uppercase","PL":"Musi zawierać wielką","ES":"Debe tener mayúsc.","FR":"Doit avoir majusc.","IT":"Deve avere maiusc.","DE":"Muss Großbuchst.","PT":"Deve ter maiúsc.","NL":"Moet hoofdletter","RU":"Должна заглавная","UA":"Мусить мати велику"},
    "has_special":  {"EN":"Must contain special char","PL":"Musi zawierać znak spec.","ES":"Debe tener carácter esp.","FR":"Doit avoir spécial","IT":"Deve avere speciale","DE":"Muss Sonderzeichen","PT":"Deve ter especial","NL":"Moet speciaal teken","RU":"Должен спецсимвол","UA":"Мусить мати спец."},
    "no_special":   {"EN":"No special characters","PL":"Brak znaków specjalnych","ES":"Sin caracteres esp.","FR":"Sans caractères spéc.","IT":"Nessun carattere spec.","DE":"Keine Sonderzeichen","PT":"Sem caracteres esp.","NL":"Geen speciale tekens","RU":"Без спецсимволов","UA":"Без спец. символів"},
    "adv_frame":    {"EN":"Advanced Options","PL":"Opcje zaawansowane","ES":"Opciones avanzadas","FR":"Options avancées","IT":"Opzioni avanzate","DE":"Erweiterte Optionen","PT":"Opções avançadas","NL":"Geavanceerde opties","RU":"Расширенные настройки","UA":"Розширені параметри"},
    "dedup":        {"EN":"Remove duplicates","PL":"Usuń duplikaty","ES":"Eliminar duplicados","FR":"Supprimer doublons","IT":"Rimuovi duplicati","DE":"Duplikate entfernen","PT":"Remover duplicatas","NL":"Duplicaten verwijderen","RU":"Удалить дубликаты","UA":"Видалити дублікати"},
    "case_label":   {"EN":"Case:","PL":"Wielkość liter:","ES":"Mayúsculas:","FR":"Casse:","IT":"Maiuscole:","DE":"Groß/Klein:","PT":"Maiúsculas:","NL":"Hoofd/kleine letters:","RU":"Регистр:","UA":"Регістр:"},
    "case_none":    {"EN":"Unchanged","PL":"Bez zmian","ES":"Sin cambios","FR":"Sans changement","IT":"Invariato","DE":"Unverändert","PT":"Sem mudanças","NL":"Ongewijzigd","RU":"Без изменений","UA":"Без змін"},
    "case_lower":   {"EN":"→ lowercase","PL":"→ małe litery","ES":"→ minúsculas","FR":"→ minuscules","IT":"→ minuscolo","DE":"→ kleinschreibung","PT":"→ minúsculas","NL":"→ kleine letters","RU":"→ строчные","UA":"→ малі"},
    "case_upper":   {"EN":"→ UPPERCASE","PL":"→ WIELKIE LITERY","ES":"→ MAYÚSCULAS","FR":"→ MAJUSCULES","IT":"→ MAIUSCOLO","DE":"→ GROSSSCHREIBUNG","PT":"→ MAIÚSCULAS","NL":"→ HOOFDLETTERS","RU":"→ ЗАГЛАВНЫЕ","UA":"→ ВЕЛИКІ"},
    "prefix_label": {"EN":"Prefix:","PL":"Prefiks:","ES":"Prefijo:","FR":"Préfixe:","IT":"Prefisso:","DE":"Präfix:","PT":"Prefixo:","NL":"Prefix:","RU":"Префикс:","UA":"Префікс:"},
    "suffix_label": {"EN":"Suffix:","PL":"Sufiks:","ES":"Sufijo:","FR":"Suffixe:","IT":"Suffisso:","DE":"Suffix:","PT":"Sufixo:","NL":"Suffix:","RU":"Суффикс:","UA":"Суфікс:"},
    "regex_label":  {"EN":"Regex filter:","PL":"Filtr Regex:","ES":"Filtro Regex:","FR":"Filtre Regex:","IT":"Filtro Regex:","DE":"Regex-Filter:","PT":"Filtro Regex:","NL":"Regex-filter:","RU":"Фильтр Regex:","UA":"Фільтр Regex:"},
    "filter_btn":   {"EN":"▶  FILTER","PL":"▶  FILTRUJ","ES":"▶  FILTRAR","FR":"▶  FILTRER","IT":"▶  FILTRA","DE":"▶  FILTERN","PT":"▶  FILTRAR","NL":"▶  FILTEREN","RU":"▶  ФИЛЬТР","UA":"▶  ФІЛЬТР"},
    "preview_btn":  {"EN":"👁  Preview (50 lines)","PL":"👁  Podgląd (50 linii)","ES":"👁  Vista previa","FR":"👁  Aperçu","IT":"👁  Anteprima","DE":"👁  Vorschau","PT":"👁  Visualizar","NL":"👁  Voorbeeld","RU":"👁  Предпросмотр","UA":"👁  Перегляд"},
    "preview_title":{"EN":"Preview — first 50 matches","PL":"Podgląd — pierwsze 50 pasujących","ES":"Vista previa — primeras 50","FR":"Aperçu — 50 premières","IT":"Anteprima — prime 50","DE":"Vorschau — erste 50","PT":"Visualizar — primeiras 50","NL":"Voorbeeld — eerste 50","RU":"Предпросмотр — первые 50","UA":"Перегляд — перші 50"},
    "no_match":     {"EN":"No matching lines found.","PL":"Brak pasujących linii.","ES":"No se encontraron líneas.","FR":"Aucune ligne trouvée.","IT":"Nessuna riga trovata.","DE":"Keine Zeilen gefunden.","PT":"Nenhuma linha encontrada.","NL":"Geen overeenkomsten.","RU":"Совпадений не найдено.","UA":"Збігів не знайдено."},
    "success":      {"EN":"Done","PL":"Gotowe","ES":"Listo","FR":"Terminé","IT":"Fatto","DE":"Fertig","PT":"Concluído","NL":"Klaar","RU":"Готово","UA":"Готово"},
    "success_msg":  {"EN":"Saved {count:,} lines (of {total:,}) to:\n{path}","PL":"Zapisano {count:,} linii (z {total:,}) do:\n{path}","ES":"Guardadas {count:,} líneas de {total:,}:\n{path}","FR":"{count:,} lignes sauvegardées sur {total:,}:\n{path}","IT":"Salvate {count:,} righe su {total:,}:\n{path}","DE":"{count:,} Zeilen (von {total:,}) gespeichert:\n{path}","PT":"{count:,} linhas de {total:,} salvas:\n{path}","NL":"{count:,} regels (van {total:,}) opgeslagen:\n{path}","RU":"Сохранено {count:,} строк из {total:,}:\n{path}","UA":"Збережено {count:,} рядків із {total:,}:\n{path}"},
    "err_title":    {"EN":"Error","PL":"Błąd","ES":"Error","FR":"Erreur","IT":"Errore","DE":"Fehler","PT":"Erro","NL":"Fout","RU":"Ошибка","UA":"Помилка"},
    "err_no_input": {"EN":"Please select an input file first.","PL":"Najpierw wybierz plik wejściowy.","ES":"Seleccione primero un archivo.","FR":"Sélectionnez d'abord un fichier.","IT":"Prima seleziona un file.","DE":"Bitte Eingabedatei auswählen.","PT":"Selecione um arquivo primeiro.","NL":"Selecteer eerst een invoerbestand.","RU":"Сначала выберите файл.","UA":"Спочатку виберіть файл."},
    "err_no_output":{"EN":"Please set an output file path.","PL":"Ustaw ścieżkę pliku wynikowego.","ES":"Establezca la ruta del archivo.","FR":"Définissez le chemin de sortie.","IT":"Imposta il percorso di output.","DE":"Bitte Ausgabepfad festlegen.","PT":"Defina o caminho de saída.","NL":"Stel het uitvoerpad in.","RU":"Укажите путь к выходному файлу.","UA":"Вкажіть шлях вихідного файлу."},
    "err_bad_regex":{"EN":"Invalid regex: {msg}","PL":"Nieprawidłowy regex: {msg}","ES":"Regex inválido: {msg}","FR":"Regex invalide: {msg}","IT":"Regex non valido: {msg}","DE":"Ungültiger Regex: {msg}","PT":"Regex inválido: {msg}","NL":"Ongeldige regex: {msg}","RU":"Неверный regex: {msg}","UA":"Невірний regex: {msg}"},
    "status_ready": {"EN":"Ready","PL":"Gotowy","ES":"Listo","FR":"Prêt","IT":"Pronto","DE":"Bereit","PT":"Pronto","NL":"Klaar","RU":"Готов","UA":"Готовий"},
    "status_done":  {"EN":"Done: {count:,} lines saved ({pct:.1f}%)","PL":"Gotowe: zapisano {count:,} linii ({pct:.1f}%)","ES":"Listo: {count:,} líneas ({pct:.1f}%)","FR":"Terminé: {count:,} lignes ({pct:.1f}%)","IT":"Fatto: {count:,} righe ({pct:.1f}%)","DE":"Fertig: {count:,} Zeilen ({pct:.1f}%)","PT":"Concluído: {count:,} linhas ({pct:.1f}%)","NL":"Klaar: {count:,} regels ({pct:.1f}%)","RU":"Готово: {count:,} строк ({pct:.1f}%)","UA":"Готово: {count:,} рядків ({pct:.1f}%)"},
    "status_proc":  {"EN":"Processing: {count:,} matched so far...","PL":"Przetwarzanie: {count:,} pasujących...","ES":"Procesando: {count:,} encontradas...","FR":"Traitement: {count:,} trouvées...","IT":"Elaborazione: {count:,} trovate...","DE":"Verarbeitung: {count:,} gefunden...","PT":"Processando: {count:,} encontradas...","NL":"Verwerken: {count:,} gevonden...","RU":"Обработка: {count:,} найдено...","UA":"Обробка: {count:,} знайдено..."},
}

def tr(key, lang, **kw):
    v = T.get(key, {}).get(lang, T.get(key, {}).get("EN", key))
    return v.format(**kw) if kw else v

# ── LIGHT THEME ───────────────────────────────────────────────────────────────
BG   = "#F5F7FA"
CARD = "#FFFFFF"
BORD = "#D0D7E2"
ACC  = "#1E50A0"
ACC2 = "#E8EEF8"
TX   = "#1A2540"
TX2  = "#5A6480"
OK   = "#1A8A4A"
WARN = "#C07000"
ERR  = "#C02020"
BTN  = "#FFFFFF"

def card(parent, **kw):
    return tk.Frame(parent, bg=CARD, relief="flat", bd=0,
                    highlightbackground=BORD, highlightthickness=1, **kw)

def section(parent, text):
    f = tk.Frame(parent, bg=ACC)
    tk.Label(f, text=text, font=("Segoe UI", 9, "bold"),
             bg=ACC, fg=BTN).pack(anchor="w", padx=8, pady=3)
    return f

def lbl(parent, key, lang_var, **kw):
    v = tk.StringVar()
    w = tk.Label(parent, textvariable=v, bg=kw.pop("bg", CARD),
                 fg=kw.pop("fg", TX), font=("Segoe UI", 9), **kw)
    def upd(*_): v.set(tr(key, lang_var.get()))
    lang_var.trace_add("write", upd); upd()
    return w

def btn(parent, text_key, lang_var, cmd, bg=ACC, fg=BTN, **kw):
    sv = tk.StringVar()
    def upd(*_): sv.set(tr(text_key, lang_var.get()))
    lang_var.trace_add("write", upd); upd()
    return tk.Button(parent, textvariable=sv, command=cmd,
                     bg=bg, fg=fg, font=("Segoe UI", 9, "bold"),
                     relief="flat", cursor="hand2",
                     activebackground="#163a80", activeforeground=BTN, **kw)


class CodeFilter:
    def __init__(self, root):
        self.root = root
        self.lang = tk.StringVar(value="EN")
        self.input_file = ""
        self.total_lines = 0
        self._w = {}

        self.len_mode    = tk.StringVar(value="any")
        self.len_exact   = tk.IntVar(value=8)
        self.len_min     = tk.IntVar(value=4)
        self.len_max     = tk.IntVar(value=10)
        self.char_type   = tk.StringVar(value="any")
        self.has_digit   = tk.BooleanVar(value=False)
        self.has_upper   = tk.BooleanVar(value=False)
        self.has_special = tk.BooleanVar(value=False)
        self.no_special  = tk.BooleanVar(value=False)
        self.dedup       = tk.BooleanVar(value=False)
        self.case_mode   = tk.StringVar(value="none")
        self.prefix_var  = tk.StringVar(value="")
        self.suffix_var  = tk.StringVar(value="")
        self.regex_var   = tk.StringVar(value="")
        self.output_path = tk.StringVar(value="")

        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.geometry("630x830")
        set_icon(root)

        style = ttk.Style()
        style.theme_use("clam")
        for w in ("TRadiobutton","TCheckbutton"):
            style.configure(w, background=CARD, foreground=TX, font=("Segoe UI",9))
            style.map(w, background=[("active", CARD)])
        style.configure("TCombobox", fieldbackground=ACC2, background=CARD, foreground=TX)
        style.configure("TProgressbar", troughcolor=BORD, background=ACC)

        self.build_ui()
        self.update_title()
        self.lang.trace_add("write", lambda *_: self.update_title())

    def t(self, key, **kw): return tr(key, self.lang.get(), **kw)

    def update_title(self):
        self.root.title(f"CodeFilter v2.1  |  Laboratorium Elektroniki")

    def build_ui(self):
        root = self.root
        # ── Header ──
        hdr = tk.Frame(root, bg=ACC)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔍  CodeFilter", font=("Segoe UI",15,"bold"),
                 bg=ACC, fg=BTN).pack(side="left", padx=14, pady=8)
        # language selector
        lang_frame = tk.Frame(hdr, bg=ACC)
        lang_frame.pack(side="right", padx=10)
        tk.Label(lang_frame, text="🌐", bg=ACC, fg=BTN,
                 font=("Segoe UI",11)).pack(side="left")
        cb = ttk.Combobox(lang_frame, textvariable=self.lang,
                          values=list(LANGUAGES.keys()), width=4,
                          state="readonly", font=("Segoe UI",9))
        cb.pack(side="left", padx=4)
        # subtitle
        sv = tk.StringVar()
        def upd_sub(*_): sv.set(tr("subtitle", self.lang.get()))
        self.lang.trace_add("write", upd_sub); upd_sub()
        tk.Label(root, textvariable=sv, font=("Segoe UI",8),
                 bg=BG, fg=TX2).pack(fill="x", padx=10, pady=(4,0))

        scroll_canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(scroll_canvas, bg=BG)
        win_id = scroll_canvas.create_window((0,0), window=inner, anchor="nw")
        def on_configure(e):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
            scroll_canvas.itemconfig(win_id, width=scroll_canvas.winfo_width())
        inner.bind("<Configure>", on_configure)
        scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(win_id, width=e.width))
        scroll_canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas.yview_scroll(-1*(e.delta//120), "units"))

        P = inner  # shorthand

        # ── Input File ──
        c1 = card(P); c1.pack(fill="x", padx=10, pady=(6,2))
        section(c1, self._tstr("input_frame")).pack(fill="x")
        row = tk.Frame(c1, bg=CARD); row.pack(fill="x", padx=8, pady=6)
        self._path_var = tk.StringVar(value="")
        e = tk.Entry(row, textvariable=self._path_var, font=("Segoe UI",9),
                     bg=ACC2, fg=TX, relief="flat", bd=4)
        e.pack(side="left", fill="x", expand=True)
        btn(row, "browse", self.lang, self.browse_input,
            width=10).pack(side="left", padx=(6,0))
        row2 = tk.Frame(c1, bg=CARD); row2.pack(fill="x", padx=8, pady=(0,6))
        lbl(row2, "lines_found", self.lang).pack(side="left")
        self._lines_lbl = tk.Label(row2, text="—", font=("Segoe UI",9,"bold"),
                                   bg=CARD, fg=ACC)
        self._lines_lbl.pack(side="left", padx=4)

        # ── Output File ──
        c2 = card(P); c2.pack(fill="x", padx=10, pady=2)
        section(c2, self._tstr("output_frame")).pack(fill="x")
        row = tk.Frame(c2, bg=CARD); row.pack(fill="x", padx=8, pady=6)
        e2 = tk.Entry(row, textvariable=self.output_path, font=("Segoe UI",9),
                      bg=ACC2, fg=TX, relief="flat", bd=4)
        e2.pack(side="left", fill="x", expand=True)
        btn(row, "save_as", self.lang, self.browse_output,
            width=12).pack(side="left", padx=(6,0))

        # ── Filter Rules ──
        c3 = card(P); c3.pack(fill="x", padx=10, pady=2)
        section(c3, self._tstr("filter_frame")).pack(fill="x")
        inner3 = tk.Frame(c3, bg=CARD); inner3.pack(fill="x", padx=8, pady=6)

        # Length
        lf = tk.Frame(inner3, bg=CARD); lf.pack(fill="x", pady=2)
        lbl(lf, "len_label", self.lang, font=("Segoe UI",9,"bold")).pack(side="left")
        for val, key in [("any","len_any"),("exact","len_exact"),("range","len_range")]:
            sv2 = tk.StringVar()
            def _upd(sv=sv2, k=key, *_): sv.set(tr(k, self.lang.get()))
            self.lang.trace_add("write", _upd); _upd()
            ttk.Radiobutton(lf, textvariable=sv2, variable=self.len_mode,
                            value=val).pack(side="left", padx=4)
        tk.Spinbox(inner3, textvariable=self.len_exact, from_=1, to=100, width=5,
                   font=("Segoe UI",9), bg=ACC2).pack(anchor="w", padx=4, pady=1)
        rf = tk.Frame(inner3, bg=CARD); rf.pack(anchor="w", pady=1)
        lbl(rf, "len_range", self.lang).pack(side="left", padx=4)
        tk.Spinbox(rf, textvariable=self.len_min, from_=1, to=100, width=5,
                   font=("Segoe UI",9), bg=ACC2).pack(side="left", padx=2)
        lbl(rf, "len_to", self.lang).pack(side="left", padx=2)
        tk.Spinbox(rf, textvariable=self.len_max, from_=1, to=200, width=5,
                   font=("Segoe UI",9), bg=ACC2).pack(side="left", padx=2)

        # Character type
        cf2 = tk.Frame(inner3, bg=CARD); cf2.pack(fill="x", pady=(6,2))
        lbl(cf2, "char_label", self.lang, font=("Segoe UI",9,"bold")).pack(side="left")
        for val, key in [("any","char_any"),("digits","char_digits"),
                         ("alpha","char_alpha"),("alnum","char_alnum"),
                         ("lower","char_lower"),("upper","char_upper")]:
            sv3 = tk.StringVar()
            def _u(sv=sv3, k=key, *_): sv.set(tr(k, self.lang.get()))
            self.lang.trace_add("write", _u); _u()
            ttk.Radiobutton(cf2, textvariable=sv3, variable=self.char_type,
                            value=val).pack(side="left", padx=3)

        # ── Additional Conditions ──
        c4 = card(P); c4.pack(fill="x", padx=10, pady=2)
        section(c4, self._tstr("cond_frame")).pack(fill="x")
        cond = tk.Frame(c4, bg=CARD); cond.pack(fill="x", padx=8, pady=4)
        for var, key in [(self.has_digit,"has_digit"),(self.has_upper,"has_upper"),
                         (self.has_special,"has_special"),(self.no_special,"no_special")]:
            sv4 = tk.StringVar()
            def _u4(sv=sv4, k=key, *_): sv.set(tr(k, self.lang.get()))
            self.lang.trace_add("write", _u4); _u4()
            ttk.Checkbutton(cond, textvariable=sv4, variable=var).pack(anchor="w")

        # ── Advanced Options ──
        c5 = card(P); c5.pack(fill="x", padx=10, pady=2)
        section(c5, self._tstr("adv_frame")).pack(fill="x")
        adv = tk.Frame(c5, bg=CARD); adv.pack(fill="x", padx=8, pady=4)

        sv5 = tk.StringVar()
        def _u5(*_): sv5.set(tr("dedup", self.lang.get()))
        self.lang.trace_add("write", _u5); _u5()
        ttk.Checkbutton(adv, textvariable=sv5, variable=self.dedup).pack(anchor="w")

        case_row = tk.Frame(adv, bg=CARD); case_row.pack(anchor="w", pady=2)
        lbl(case_row, "case_label", self.lang).pack(side="left")
        for val, key in [("none","case_none"),("lower","case_lower"),("upper","case_upper")]:
            sv6 = tk.StringVar()
            def _u6(sv=sv6, k=key, *_): sv.set(tr(k, self.lang.get()))
            self.lang.trace_add("write", _u6); _u6()
            ttk.Radiobutton(case_row, textvariable=sv6, variable=self.case_mode,
                            value=val).pack(side="left", padx=3)

        for var, key in [(self.prefix_var,"prefix_label"),(self.suffix_var,"suffix_label")]:
            row_ps = tk.Frame(adv, bg=CARD); row_ps.pack(anchor="w", fill="x", pady=1)
            lbl(row_ps, key, self.lang, width=8).pack(side="left")
            tk.Entry(row_ps, textvariable=var, width=20, font=("Segoe UI",9),
                     bg=ACC2, fg=TX, relief="flat", bd=4).pack(side="left", padx=4)

        regex_row = tk.Frame(adv, bg=CARD); regex_row.pack(anchor="w", fill="x", pady=1)
        lbl(regex_row, "regex_label", self.lang, width=10).pack(side="left")
        tk.Entry(regex_row, textvariable=self.regex_var, width=28, font=("Segoe UI",9),
                 bg=ACC2, fg=TX, relief="flat", bd=4).pack(side="left", padx=4)

        # ── Buttons + Progress ──
        c6 = card(P); c6.pack(fill="x", padx=10, pady=(4,8))
        bf = tk.Frame(c6, bg=CARD); bf.pack(fill="x", padx=8, pady=6)
        fb = btn(bf, "filter_btn", self.lang, self.run_filter,
                 font=("Segoe UI",10,"bold"), height=2)
        fb.pack(side="left", fill="x", expand=True, padx=(0,6))
        self._w["filter_btn"] = fb
        pb_btn = btn(bf, "preview_btn", self.lang, self.run_preview,
                     bg="#4A7CC0", width=20)
        pb_btn.pack(side="left")
        self._w["preview_btn"] = pb_btn

        self.progress = ttk.Progressbar(c6, mode="indeterminate")
        self.progress.pack(fill="x", padx=8, pady=(0,4))

        self._w["status_lbl"] = tk.Label(c6, text="", font=("Segoe UI",9),
                                          bg=CARD, fg=TX2)
        self._w["status_lbl"].pack(pady=(0,4))

        # footer
        tk.Label(P, text="Laboratorium Elektroniki  |  CodeFilter v2.1  |  laboratoriumelektroniki.pl",
                 font=("Segoe UI",7), bg=BG, fg=TX2).pack(pady=4)

    def _tstr(self, key):
        sv = tk.StringVar()
        def upd(*_): sv.set(tr(key, self.lang.get()))
        self.lang.trace_add("write", upd); upd()
        return sv.get()

    def browse_input(self):
        path = filedialog.askopenfilename(
            title="Select wordlist TXT file",
            filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        self.input_file = path
        self._path_var.set(path)
        # Count lines fast (binary)
        try:
            with open(path, "rb") as f:
                self.total_lines = f.read().count(b"\n")
            self._lines_lbl.config(text=f"{self.total_lines:,}")
        except Exception:
            self._lines_lbl.config(text="?")
        # Auto output path
        base, ext = os.path.splitext(path)
        self.output_path.set(base + "_filtered" + (ext or ".txt"))

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save filtered output as",
            defaultextension=".txt",
            filetypes=[("Text files","*.txt"),("All files","*.*")])
        if path:
            self.output_path.set(path)

    def _build_filter(self):
        """Build and return filter function + compiled regex (or None)."""
        len_mode  = self.len_mode.get()
        len_exact = self.len_exact.get()
        len_min   = self.len_min.get()
        len_max   = self.len_max.get()
        char_type = self.char_type.get()
        has_digit = self.has_digit.get()
        has_upper = self.has_upper.get()
        has_spec  = self.has_special.get()
        no_spec   = self.no_special.get()
        dedup     = self.dedup.get()
        case_mode = self.case_mode.get()
        prefix    = self.prefix_var.get()
        suffix    = self.suffix_var.get()
        regex_str = self.regex_var.get().strip()

        rx = None
        if regex_str:
            try:
                rx = re.compile(regex_str)
            except re.error as e:
                raise ValueError(self.t("err_bad_regex", msg=str(e)))

        SPEC = set('!@#$%^&*()_+-=[]{}|;\':",.<>?/`~\\')

        def match(word):
            n = len(word)
            # length
            if len_mode == "exact" and n != len_exact: return False
            if len_mode == "range" and not (len_min <= n <= len_max): return False
            # char type (fastest checks first)
            if char_type == "digits" and not word.isdigit(): return False
            if char_type == "alpha"  and not word.isalpha(): return False
            if char_type == "alnum"  and not word.isalnum(): return False
            if char_type == "lower"  and not (word.isalpha() and word.islower()): return False
            if char_type == "upper"  and not (word.isalpha() and word.isupper()): return False
            # additional conditions
            if has_digit and not any(c.isdigit() for c in word): return False
            if has_upper and not any(c.isupper() for c in word): return False
            if has_spec  and not any(c in SPEC for c in word):   return False
            if no_spec   and any(c in SPEC for c in word):       return False
            # regex (slowest — last)
            if rx and not rx.search(word): return False
            return True

        def transform(word):
            if case_mode == "lower": word = word.lower()
            elif case_mode == "upper": word = word.upper()
            return prefix + word + suffix

        return match, transform, dedup

    def run_filter(self, preview=False):
        if not self.input_file:
            messagebox.showerror(self.t("err_title"), self.t("err_no_input"))
            return
        if not preview and not self.output_path.get():
            messagebox.showerror(self.t("err_title"), self.t("err_no_output"))
            return
        try:
            match, transform, dedup = self._build_filter()
        except ValueError as e:
            messagebox.showerror(self.t("err_title"), str(e)); return

        self._w["filter_btn"].config(state="disabled")
        self._w["preview_btn"].config(state="disabled")
        self._w["status_lbl"].config(text="⏳ …", fg=WARN)
        self.progress.start(12)

        def worker():
            results = []
            count = 0
            seen = set() if dedup else None
            BUFSIZE = 1 << 20  # 1 MB
            try:
                with open(self.input_file, "r", encoding="utf-8",
                          errors="replace", buffering=BUFSIZE) as fin:
                    if preview:
                        for raw in fin:
                            word = raw.rstrip("\n\r")
                            if match(word):
                                if dedup:
                                    if word in seen: continue
                                    seen.add(word)
                                results.append(transform(word))
                                if len(results) >= 50: break
                    else:
                        with open(self.output_path.get(), "w", encoding="utf-8",
                                  buffering=BUFSIZE) as fout:
                            buf = []
                            for raw in fin:
                                word = raw.rstrip("\n\r")
                                if match(word):
                                    if dedup:
                                        if word in seen: continue
                                        seen.add(word)
                                    buf.append(transform(word))
                                    count += 1
                                    if len(buf) >= 50_000:
                                        fout.write("\n".join(buf) + "\n")
                                        buf.clear()
                                        self.root.after(0, lambda c=count:
                                            self._w["status_lbl"].config(
                                                text=tr("status_proc", self.lang.get(), count=c),
                                                fg=WARN))
                            if buf:
                                fout.write("\n".join(buf) + "\n")
            except Exception as e:
                self.root.after(0, lambda: self.reset_ui())
                self.root.after(0, lambda: messagebox.showerror(
                    self.t("err_title"), str(e)))
                return

            if preview:
                self.root.after(0, lambda: self.show_preview(results))
                self.root.after(0, lambda: self.finish_preview())
            else:
                self.root.after(0, lambda: self.finish(count, self.output_path.get()))

        threading.Thread(target=worker, daemon=True).start()

    def run_preview(self):
        self.run_filter(preview=True)

    def show_preview(self, results):
        lang = self.lang.get()
        win = tk.Toplevel(self.root)
        win.title(tr("preview_title", lang))
        win.configure(bg=BG)
        win.geometry("500x520")
        tk.Label(win, text=tr("preview_title", lang),
                 font=("Segoe UI",10,"bold"), bg=ACC, fg=BTN).pack(fill="x", pady=0)
        frame = tk.Frame(win, bg=BG); frame.pack(fill="both", expand=True, padx=10, pady=8)
        sb = ttk.Scrollbar(frame); sb.pack(side="right", fill="y")
        txt = tk.Text(frame, bg=CARD, fg=TX, font=("Courier New",10),
                      yscrollcommand=sb.set, relief="flat", bd=6)
        txt.pack(fill="both", expand=True)
        sb.config(command=txt.yview)
        txt.insert("end", "\n".join(results) if results else tr("no_match", lang))
        txt.config(state="disabled")
        tk.Label(win, text="Laboratorium Elektroniki",
                 font=("Segoe UI",7), bg=BG, fg=TX2).pack(side="bottom", pady=2)

    def finish(self, count, path):
        self.progress.stop()
        self._w["filter_btn"].config(state="normal")
        self._w["preview_btn"].config(state="normal")
        pct = (count / self.total_lines * 100) if self.total_lines else 0
        self._w["status_lbl"].config(
            text=tr("status_done", self.lang.get(), count=count, pct=pct), fg=OK)
        messagebox.showinfo(self.t("success"),
            self.t("success_msg", count=count, total=self.total_lines, path=path))

    def finish_preview(self):
        self.progress.stop()
        self._w["filter_btn"].config(state="normal")
        self._w["preview_btn"].config(state="normal")
        self._w["status_lbl"].config(text=tr("status_ready", self.lang.get()), fg=TX2)

    def reset_ui(self):
        self.progress.stop()
        self._w["filter_btn"].config(state="normal")
        self._w["preview_btn"].config(state="normal")
        self._w["status_lbl"].config(text=f"❌ {self.t('err_title')}", fg=ERR)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeFilter(root)
    root.mainloop()
