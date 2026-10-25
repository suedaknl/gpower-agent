# Oturum 2 -- Temiz oda yazımı  [ilk prompt]

Bu oturum YENİ bir oturumdur. Elinde yalnızca SPEC.md vardır. Ghidra çıktısını, LEDGER.md'yi ve
G*Power'ı görmezsin.

Görevin: SPEC.md'deki kabul kriterlerini sağlayan bir "iki bağımsız ortalama t testi" güç/örneklem
büyüklüğü motoru ve CLI yazmak (dil: Python). Önce her Gherkin senaryosunu teste çevir, sonra yaz.
CLI sözleşmesi: `gpower-clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1`
çıktı tek satır JSON; geçersiz girdide {"error": "..."} ve sıfırdan farklı çıkış kodu.
Dağılım fonksiyonları için scipy kullanabilirsin. Hesap tek modülde olsun; CLI/MCP yalnızca onu çağırsın.
SPEC'te belirsiz kalan yerde tahmin etme; "SPEC belirsiz: ..." diye listele.
