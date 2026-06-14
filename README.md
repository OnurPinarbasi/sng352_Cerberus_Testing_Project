# Cerberus Software Testing Project

Bu proje, **Cerberus** doğrulama kütüphanesi üzerine yazılmış MUMCUT tabanlı ünite testlerini ve mantıksal mutasyon (hata) testlerini içerir.

---

## 1. Proje Çalıştırma Komutları

Terminalde projenin ana dizinindeyken aşağıdaki komutları kullanabilirsiniz:

### 1.1. Ünite Testlerini Çalıştırmak İçin
Yazılan tüm temiz testleri koşturmak için:
```bash
pytest tests/ -v
```

### 1.2. Mutasyon (Hata) Testlerini Çalıştırmak İçin
Yazılan mantıksal hataların testler tarafından yakalanıp yakalanmadığını (öldürülüp öldürülmediğini) görmek için:
```bash
python faults/run_mutants.py
```

---

## 2. Klasör Yapısı

* **`cerberus/`**: Test edilen orijinal kütüphane kodları.
* **`tests/`**: Grup üyeleri tarafından yazılan ünite testleri (`member1`, `member2`, `member3`, `member4`).
* **`faults/`**: Manuel olarak enjekte edilen mantıksal hatalar (mutantlar) ve otomatik çalıştırıcı betik (`run_mutants.py`).
* **`report/`**: Matematiksel türetimlerin ve detayların olduğu proje raporu.
