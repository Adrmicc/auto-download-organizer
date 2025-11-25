# Krok po kroku: Jak uruchomić projekt

## 1. Instalacja środowiska

### Krok 1.1: Sprawdź Python
```powershell
python --version
```
Upewnij się, że masz Python 3.8 lub nowszy.

### Krok 1.2: Utwórz środowisko wirtualne
```powershell
cd auto-download-organizer
python -m venv venv
```

### Krok 1.3: Aktywuj środowisko
```powershell
.\venv\Scripts\Activate.ps1
```

### Krok 1.4: Zainstaluj zależności
```powershell
pip install -r requirements.txt
```

## 2. Pierwsze uruchomienie

### Krok 2.1: Test w trybie dry-run
```powershell
python -m src.cli organize --dry-run
```

To pokaże, co zostałoby zrobione bez faktycznej zmiany plików.

### Krok 2.2: Sprawdź wyniki
Program powinien wyświetlić listę plików i gdzie by zostały przeniesione.

## 3. Organizacja plików

### Krok 3.1: Organizuj folder Downloads
```powershell
python -m src.cli organize
```

### Krok 3.2: Sprawdź folder Downloads
Otwórz folder Downloads i zobacz, że pliki są teraz w kategoriach (Documents, Images, etc.).

### Krok 3.3: Sprawdź log
```powershell
python -m src.cli show-log
```

## 4. Czyszczenie duplikatów

### Krok 4.1: Zobacz raport duplikatów
```powershell
python -m src.cli clean-duplicates --report-only
```

### Krok 4.2: Usuń duplikaty
```powershell
python -m src.cli clean-duplicates
```

## 5. Uruchomienie testów

### Krok 5.1: Uruchom wszystkie testy
```powershell
pytest
```

### Krok 5.2: Testy z pokryciem kodu
```powershell
pytest --cov=src tests/
```

## 6. Użycie zaawansowane

### Krok 6.1: Tworzenie własnej konfiguracji
```powershell
python -m src.cli create-config moja_konfiguracja.yaml
```

Edytuj plik i dodaj własne kategorie.

### Krok 6.2: Użyj własnej konfiguracji
```powershell
python -m src.cli organize -c moja_konfiguracja.yaml
```

### Krok 6.3: Organizacja z folderami dat
```powershell
python -m src.cli organize --date-folders
```

### Krok 6.4: Pełna organizacja
```powershell
python -m src.cli full -d "C:\Users\YourName\Downloads" --clean-duplicates
```

## 7. Rozwiązywanie problemów

### Problem: Błąd importu modułu Click
**Rozwiązanie:**
```powershell
pip install click
```

### Problem: Testy się nie uruchamiają
**Rozwiązanie:**
```powershell
pip install pytest
pytest
```

### Problem: Błąd "Cannot find module"
**Rozwiązanie:**
Upewnij się, że środowisko wirtualne jest aktywne:
```powershell
.\venv\Scripts\Activate.ps1
```

## 8. Kolejne kroki

1. **Przetestuj na prawdziwych plikach** - ale najpierw zrób backup!
2. **Dostosuj konfigurację** - dodaj własne kategorie
3. **Stwórz harmonogram** - użyj Windows Task Scheduler do automatycznego uruchamiania
4. **Eksperymentuj z opcjami** - wypróbuj różne strategie dla duplikatów
5. **Rozwijaj projekt** - dodaj własne kategorie i funkcje

## Gratulacje!

Masz teraz w pełni funkcjonalny, profesjonalny projekt automatyzacji! 🎉
