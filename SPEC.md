# SPEC.md -- t testi, iki bağımsız ortalama (t2-indep)

> DURUM: Taslak. `@hypothesis` etiketli senaryolar REA kanıtı gelince `@verified` yapılır veya düzeltilir.
> Temiz oda: Oturum 2 yalnızca bu dosyayı görür. Belirsiz bırakılan yer tahminle doldurulmaz.

```gherkin
Feature: İki bağımsız ortalama için örneklem büyüklüğü ve güç (t testi)

  Background:
    Given test ailesi "t2-indep"
    And etki büyüklüğü d Cohen'in d'sidir (standartlaştırılmış ortalama farkı)
    And ratio = n2 / n1

  @verified-by-contract
  Scenario: Yönergedeki örnek
    When mode "a-priori", tails 2, d 0.5, alpha 0.05, power 0.95, ratio 1
    Then çıktı {"n1":105,"n2":105,"n_total":210,"actual_power":0.9501,"critical":1.9714,"df":208,"ncp":3.6228}

  @verified-by-contract
  Scenario: Hesap tanımları
    Then df = n1 + n2 - 2
    And ncp = d * sqrt(n1*n2/(n1+n2))
    And critical = t_{1-alpha/tails}(df)
    And actual_power = P(merkezi olmayan t(df, ncp) ret bölgesinde)

  @verified-by-contract
  Scenario: Geçersiz girdi
    When d = 0 veya alpha <= 0 veya alpha >= 1 veya power <= 0 veya power >= 1 veya ratio <= 0 veya tails not in {1,2}
    Then çıktı {"error": "<açıklama>"} ve çıkış kodu sıfırdan farklı

  @hypothesis @REA-pending(L-05)
  Scenario: a priori arama
    Given hedef güç P
    Then döndürülen n1, actual_power >= P sağlayan EN KÜÇÜK n1'dir

  @hypothesis @REA-pending(L-04)
  Scenario: Eşit olmayan oranda n2
    When ratio 2.7
    Then n2 = ceil(ratio * n1)

  @hypothesis @REA-pending(L-07)
  Scenario: Tek yönlü test, negatif d
    When tails 1 ve d < 0
    Then hesap |d| ile yapılır

  @hypothesis @REA-pending(L-08)
  Scenario: power <= alpha
    When power <= alpha
    Then (G*Power davranışı: ?) -- REA ile belirlenecek

  @hypothesis @REA-pending(L-03)
  Scenario: Çok büyük N
    When gereken n1 > desteklenen azami değer
    Then {"error": "..."} -- sınır değeri REA ile belirlenecek

  @hypothesis @REA-pending(L-09)
  Scenario: post hoc
    When mode "post-hoc", n1 20, n2 40, d 0.8, alpha 0.05, tails 2
    Then actual_power merkezi olmayan t ile n1,n2'den hesaplanır; n_total = n1 + n2
```

## Çıktı alanları
`n1, n2, n_total` tam sayı; `actual_power, critical, ncp` ondalık (basamak sayısı: L-06); `df` tam sayı.
