# HALLUCINATIONS.md

En az 2 gerçek kayıt gerekir: ajanın YANLIŞ çıkardığı şey, nasıl fark edildiği, hangi test yakaladı.
Bu dosya burada bilerek boş bırakıldı: kayıtlar REA oturumundan gelmeli, uydurulmamalı.

| # | Ajanın iddiası | Gerçek davranış | Nasıl fark edildi | Yakalayan test |
|---|----------------|-----------------|-------------------|----------------|
| 1 | | | | |
| 2 | | | | |

## Şimdiden bilinen (dürüst) not -- bu bir REA halüsinasyonu değil, bir motor hatası
- scipy `nct.cdf(-crit, df, ncp)` büyük n ve küçük alfa'da `nan` döndürüyordu; arama kuralı `nan >= hedef` yanlış olduğu için
  `n1` yanlış (ör. d=0.5, alpha=0.001, power=0.95 için 212 yerine 198 olması gerekirken) bulunuyordu.
  Yakalayan: tests/test_differential.py (statsmodels ölçek vektörleri). Düzeltme: alt kuyruk simetriyle `nct.sf(crit, df, -ncp)`.
