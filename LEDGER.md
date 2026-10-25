# LEDGER.md - G*Power t-test (Independent Means) Kanıt Defteri

## 1. Arama Döngüsü (A priori)
* **Başlangıç ve Adım:** [REA] Başlangıç aralığı `[3.0, 100.0]`. Eğer güç yetmezse üst sınır `x 1.6` katlanarak büyür. Adım adım arama yerine Brent kök bulucu algoritması kullanılır (Tolerans: 1e-10, Maksimum İterasyon: 300).
  * *Kanıt Adresi:* `0x4ac4c0` -> `FUN_004962d0(0, 0x40080000, 0, 0x40590000)` ve `0x4962d0` (büyütme döngüsü).

## 2. Eşit Olmayan Oran (Allocation Ratio) ve Yuvarlama
* **Bölüşüm Kuralı:** [REA] Toplam N bulunduktan sonra `n1` yakına yuvarlanır (`round`), `n2` ise yukarı yuvarlanır (`ceil`).
  * *Formül:* `n1 = round(N / (r + 1))` ve `n2 = ceil(N - n1)`.
  * *Kanıt Adresi:* `0x4d9d88` (ceil çağrısı) ve `0x5727d0` (round-half-up).

## 3. Toplam N'nin Çift Sayı Zorlaması (Nihai Yuvarlama)
* **Çift Sayı Kancası:** [REA] Toplam örneklem boyutu `N`, oran ne olursa olsun arayüze aktarılmadan önce daima çift sayıya (veya 4'e) tamamlanır.
  * *Formül:* `N_int = 2 * ceil(round10(N/2))`.
  * *Kanıt Adresi:* `0x4d64c0` -> `return fVar1 + fVar1;`

## 4. Minimum Allocation Ratio
* **Sınır Kontrolü:** [REA] Oran (ratio) geçerlilik aralığı `[0.01, 100]` olarak belirlenmiştir.
  * *Kanıt Adresi:* `0x487300` -> `FUN_00487300` ("The allocation ratio falls outside" hata referansı) ve `0x5c3b50` adresindeki `0.01` sabiti.