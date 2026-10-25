# T-Power (G*Power Engine & MCP Agent Suite)

Bu proje, G*Power (3.1.9.7) aracının "t tests -> iki bağımsız ortalama" hesaplama mantığının tersine mühendislikle incelenerek temiz odada (clean-room) yeniden yazıldığı bağımsız bir akademik yazılım çalışmasıdır (`tpower`). Proje; temel CLI arayüzü, MCP (Model Context Protocol) sunucusu ve doğal dilde çalışan bir AI ajan entegrasyonunu kapsamaktadır.

* **Uyum Oranı (Conformance Gate):** Oracle test vektörlerinde %100 (38/38) tam eşleşme başarısı sağlamıştır.
* **Yasal/Etik Not:** Tamamen bağımsız bir Python paketi olarak geliştirilmiştir; orijinal ikili dosyalarını (`GPower.exe`) içermez.

## Davranışsal Sabitler ve Konfigürasyon (`config.py`)

Matematiksel ders kitaplarında açıkça yer almayan ancak G*Power'ın iç mantığını taklit etmek için tersine mühendislikle saptanan davranışsal sabitler:

```python
# H-ROUND-N2: how n2 is derived from n1 and the allocation ratio (n2 = ratio * n1).
N2_ROUNDING = "floor"

# H-SEARCH-START: smallest n1 tried by the a priori search.
N1_MIN = 2

# H-SEARCH-MAX: upper bound on n1; beyond this the search gives up.
N1_MAX = 1_000_000

# H-DIGITS: decimals in the JSON output.
DIGITS = 4

# H-ONETAIL-SIGN: how one-tailed power treats negative d.
ONE_TAIL_NEGATIVE_D = "abs"

Kurulum ve Çalıştırma
Sanal Ortamı Başlatma:

PowerShell
python -m venv .venv
.\.venv\Scripts\activate
Bağımlılıkları Yükleme:

PowerShell
pip install -e ".[mcp,test]"
Uyum Testini Çalıştırma (%100 Başarı):

PowerShell
python tests/conformance.py
Mimari ve MCP / Ajan Katmanı
src/tpower/engine.py: Tüm istatistiksel hesaplamaları yürüten tek ve merkezi motor.

src/mcp_server.py: Hesaplama yapmadan doğrudan API katmanına bağlanan ince MCP sunucusu.

src/agent.py: Doğal dildeki istekleri OpenAI araç çağırma (tool-calling) özellikleri ile MCP araçlarına dönüştüren ajan katmanı.

Araç Adı,Girdi Parametreleri,Çıktı Alanları
t2_indep_sample_size,"d, alpha=0.05, power=0.8, tails=2, ratio=1.0","n1, n2, n_total, actual_power, critical, df, ncp"
t2_indep_power,"d, n1, n2, alpha=0.05, tails=2","actual_power, critical, df, ncp"