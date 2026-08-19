🇬🇧 [Click here for English](README.md)

# AI Destekli Pazarlama Analiz Asistanı

Kampanya performans verisini (CSV) otomatik analiz eden ve AI destekli yorum/öneriler üreten bir araç — haftalık kampanya raporlama sürecini otomatikleştirmek için geliştirildi.

## Amaç

Pazarlama ekipleri, haftalık/aylık raporlar için sayıları manuel toplama, metrik hesaplama ve öneri yazma işlerine ciddi zaman harcıyor. Bu araç tüm bu süreci otomatikleştiriyor: ham kampanya verisini alır, tüm temel performans metriklerini hesaplar, neyin işe yaradığını neyin yaramadığını belirler ve AI kullanarak somut, veri odaklı öneriler üretir — hepsini tek bir PDF raporunda birleştirir.

**Kısaca: veri + AI yorumu, birlikte ve otomatik olarak sunuluyor.**

## Özellikler

- **Otomatik veri girişi** — kampanya performans verisini doğrudan bir CSV dosyasından okur
- **Metrik hesaplama** — her kampanya için CTR, CPC, CPA, Dönüşüm Oranı ve ROAS'ı otomatik olarak hesaplar
- **Performans tespiti** — en iyi performans gösteren kampanyayı (en yüksek ROAS) ve en maliyetli olanı (en yüksek CPA) otomatik olarak işaretler
- **AI destekli öneriler** — hesaplanan metrikleri OpenAI API'ye gönderir ve somut öneriler alır: hangi kampanyaların bütçesi artırılmalı, hangileri durdurulmalı veya düzeltilmeli
- **Görsel raporlama** — Matplotlib ile net grafikler oluşturur (kampanya bazlı ROAS, Harcama vs Gelir)
- **PDF rapor** — metrik tablosunu, grafikleri ve AI yorumlarını tek, düzenli bir PDF'te birleştirir, paylaşıma veya sunuma hazır
- **Otomatik pipeline** — tek bir komut (`python main.py`) tüm süreci baştan sona çalıştırır


## Örnek Çıktı

Aşağıda, `data/campaigns_sample.csv` verisinden pipeline tarafından otomatik olarak oluşturulan grafikler yer alıyor:

### Kampanya Bazlı ROAS
![Kampanya Bazlı ROAS](outputs/charts/roas_by_campaign.png)

### Harcama vs Gelir
![Harcama vs Gelir](outputs/charts/spend_vs_revenue.png)

Metrik tablosu, yukarıdaki her iki grafik ve AI destekli önerileri içeren tam rapor burada: [`outputs/reports/weekly_report.pdf`](outputs/reports/weekly_report.pdf)


## Kullanılan Teknolojiler

- Python
- Pandas — veri işleme
- Matplotlib — grafik oluşturma
- OpenAI API — AI destekli yorum üretimi
- ReportLab — PDF rapor oluşturma

## Proje Yapısı

```
ai-marketing-analytics/
├── data/
│   └── campaigns_sample.csv
├── outputs/
│   ├── charts/
│   └── reports/
├── src/
│   ├── data_loader.py       # CSV okuma + metrik hesaplama
│   ├── charts.py            # Grafik oluşturma
│   ├── ai.py                # OpenAI API ile AI yorumu üretme
│   ├── report_builder.py    # PDF rapor oluşturma
│   └── main.py               # Tüm süreci baştan sona çalıştırır
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Kurulum

1. Repoyu klonla:
```bash
git clone <repo-url>
cd ai-marketing-analytics
```

2. Sanal ortam oluştur ve aktifleştir:
```bash
python -m venv venv
source venv/bin/activate  # Windows'ta: venv\Scripts\activate
```

3. Gerekli paketleri yükle:
```bash
pip install -r requirements.txt
```

4. Proje kök dizininde bir `.env` dosyası oluştur ve OpenAI API anahtarını ekle:
```
OPENAI_API_KEY=senin_api_anahtarın
```

## Kullanım

Tüm süreci çalıştırmak için:
```bash
cd src
python main.py
```

Bu komut sırasıyla:
1. `data/campaigns_sample.csv` dosyasını yükler ve analiz eder
2. Her kampanya için CTR, CPC, CPA, Dönüşüm Oranı ve ROAS hesaplar
3. En iyi ve en sorunlu kampanyayı belirler
4. `outputs/charts/` klasörüne iki grafik kaydeder
5. AI destekli öneriler ister
6. `outputs/reports/weekly_report.pdf` içine final raporu oluşturur


## Metrik Açıklamaları

| Metrik | Formül | Anlamı |
|---|---|---|
| CTR | Tıklama / Gösterim × 100 | Tıklama oranı |
| CPC | Harcama / Tıklama | Tıklama başına maliyet |
| CPA | Harcama / Dönüşüm | Dönüşüm başına maliyet |
| Dönüşüm Oranı | Dönüşüm / Tıklama × 100 | Tıklamaların dönüşüme oranı |
| ROAS | Gelir / Harcama | Reklam harcaması getirisi |
```
