# Cerberus Software Testing Project

Bu proje, Python veri doğrulama kütüphanesi **Cerberus**'un güvenlik ve doğruluğunu sınamak amacıyla geliştirilmiş bir yazılım test projesidir. 

Projede formal test tasarımı yöntemlerinden **MUMCUT (Kriter 8.30)** analiz yöntemi ve **DNF Hata Sınıfları (Table 8.1)** kullanılmıştır.

---

## 1. Proje Hakkında Genel Bilgiler

* **Hedef Sistem:** Cerberus doğrulama kütüphanesinin `validator.py` dosyasındaki 20 kritik fonksiyon test edilmiştir.
* **Ekip Çalışması:** 4 takım üyesi, sistemden tamamen benzersiz 5'er fonksiyon (toplamda 20 fonksiyon) seçerek detaylı $\LaTeX$ analizleri ve doğruluk tabloları oluşturmuştur.
* **Test Süiti:** Her üye en az 20 adet ünite testi yazarak toplamda **105 testlik** güçlü bir test süiti oluşturmuştur.
* **Hata Emülasyonu (Mutation Testing):** Kod tabanına Table 8.1 hata sınıflarını (LIF, LNF, TOF vb.) simüle eden **45 mantıksal mutasyon** (yapay hata) yerleştirilmiştir. Bu sayede testlerin hataları yakalama (öldürme) yeteneği ölçülmüştür.

---

## 2. Çalıştırma Komutları

Terminalde projenin ana dizinindeyken aşağıdaki komutları kullanabilirsiniz:

### 2.1. Ünite Testlerini Çalıştırmak İçin
Yazılan tüm temiz testleri koşturmak ve testlerin geçtiğini doğrulamak için:
```bash
pytest tests/ -v
```

### 2.2. Mutasyon (Hata) Testlerini Çalıştırmak İçin
Yazılan mantıksal hataların (mutantların) testler tarafından yakalanıp yakalanmadığını (öldürülüp öldürülmediğini) otomatik olarak test etmek için:
```bash
python faults/run_mutants.py
```
*(Bu komut, 45 mutasyonu sırasıyla koda uygulayıp testleri koşacak ve en sonunda hangilerinin başarıyla yakalandığını terminalde tablo şeklinde gösterecektir).*

---

## 3. Klasör Yapısı

* **`cerberus/`**: Test edilen hedef kütüphanenin kaynak kodları.
* **`tests/`**: Grup üyeleri tarafından yazılan ünite testleri (`member1`, `member2`, `member3`, `member4`).
* **`faults/`**: Manuel oluşturulan mantıksal hata dosyaları (mutantlar) ve otomatik çalıştırıcı betik (`run_mutants.py`).
* **`report/`**: Matematiksel türetimlerin, doğruluk tablolarının ve analizlerin yer aldığı proje teslim raporu (`report.md`).
