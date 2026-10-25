# Bağımsız-örneklem t testi güç motoru (eğitim projesi, YZM301 Ödev 5)

**Yapılan katmanlar:** CLI (temel) · MCP sunucusu (bonus) · AI ajan iskeleti (bonus, canlı API ile test edilecek)

Bu proje G\*Power 3.1.9.7'nin "t tests -> iki bağımsız ortalama" hesabını REA ile inceleyip kanıtlarıyla belgeleyen
ve temiz odada yeniden yazan bir ders çalışmasıdır. G\*Power ile ilişkili değildir ve onun yerine geçmez.
**Atıf:** Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007, 2009). G\*Power 3 / G\*Power 3.1.

## Kurulum ve çalıştırma
```bash
pip install -e ".[mcp,test]"
gpower-clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
# {"n1":105,"n2":105,"n_total":210,"actual_power":0.9501,"critical":1.9714,"df":208,"ncp":3.6228}
gpower-clone --test t2-indep --mode post-hoc --d 0.8 --n1 20 --n2 40
python -m pytest -q                      # birim + diferansiyel + CLI/MCP eşdeğerlik
python oracle/make_statsmodels_vectors.py
python tests/conformance.py              # G*Power vektörlerine uyum oranı (kapı: N >= %90)
```
CLI komut adı `gpower-clone` yönerge sözleşmesinden gelir; paket adı `tpower`'dır.

## Mimari
`src/tpower/engine.py` (tek hesap motoru) <- `api.py` (tek giriş) <- `cli.py`, `mcp_server.py`, `agent/`.
Davranış sabitleri (yuvarlama, arama sınırı, basamak) yalnızca `config.py` içinde, her biri LEDGER satırına bağlı.

## MCP araç şeması
| Araç | Girdi | Çıktı |
|------|-------|-------|
| `t2_indep_sample_size` | `d` (float), `alpha`=0.05, `power`=0.8, `tails`=2, `ratio`=1.0 (n2/n1) | `n1,n2,n_total,actual_power,critical,df,ncp` veya `{"error"}` |
| `t2_indep_power` | `d`, `n1`, `n2`, `alpha`=0.05, `tails`=2 | aynı alanlar |

## Köken (provenance) -- dürüstlük notu
`src/` iskeleti ders kitabı matematiğinden (merkezi olmayan t) ve kamuya açık scipy API'sinden yazıldı;
SPEC.md'den yazılmadı ve Ghidra çıktısı kullanılmadı. Temiz oda koşulunu karşılamak için Oturum 2'de motoru
yalnızca SPEC.md ile yeniden yazdırıp bu sürümle karşılaştırın veya bu durumu AGENT_COST.md'de açıkça belirtin.

## Henüz yapılmayanlar (teslimden önce)
- [ ] REA/Ghidra oturumu -> LEDGER.md [REA] satırları, SPEC.md `@verified`
- [ ] G\*Power'dan 44 vektör (oracle/gpower_vectors.csv) + ekran görüntüleri
- [ ] GPower.exe SHA-256: `sha256sum GPower.exe` -> buraya: `<HASH>`; REA/Ghidra kontrol ekran görüntüsü
- [ ] HALLUCINATIONS.md (>=2 gerçek kayıt), AGENT_COST.md
- [ ] ajanı canlı çalıştır (`agent/run_eval.py`), 60 sn demo videosu: `<LİNK>`
- [ ] ajan sürümü: Jev/LLM yönlendirici kalibrasyonu (isteğe bağlı)
