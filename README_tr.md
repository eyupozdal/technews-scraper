# 📰 TechNews Scraper & Aggregator

[Hacker News](https://news.ycombinator.com/) üzerinden en son teknoloji haberlerini çeken, terminalde basit ama şık bir tabloda gösteren ve JSON dosyasına kaydeden modüler bir Python projesi.

---

## 🚀 Özellikler
- **Modüler Mimari:** Veri çekme, kaydetme ve ekranda gösterme mantığı birbirinden tamamen bağımsızdır.
- **Güçlü Hata Yönetimi:** Ağ hatalarında otomatik yeniden deneme yapar ve hatalı satırlarda çökmez.
- **Şık Terminal Çıktısı:** `rich` kütüphanesi ile modern ve renkli tablo görünümü.
- **JSON Desteği:** Elde edilen verileri zaman damgasıyla yerel diske kaydeder.

---

## 💡 Yapay Zeka ve Öğrenme Üzerine Not
Bu proje, yazılım geliştirmeye ve GitHub kullanmaya ilk adımı atmak amacıyla yapay zeka yardımıyla hazırlanmış oldukça basit bir çalışmadır. Günümüz yazılım dünyasında kod yazmaktan ziyade; yazılan kodu okuyabilmek, mantığını anlayabilmek, hata görebilmek ve düzeltme yapabilmek çok daha önemlidir. Eğer bu projeyi inceleyip sadece kodu çalıştırmakla kalmayıp çalışma mantığını da kavrayabildiyseniz, bu proje amacına ulaşmış demektir :) Teşekkürler!

---

## 📄 Lisans

Bu proje, MIT Lisansı kapsamında yayınlanmıştır. Bunu, öğrenme amaçlı bir kaynak olarak ya da kendi veri toplama projeleriniz için bir başlangıç noktası olarak kullanmaktan çekinmeyin. :D

---

## ⚙️ Hızlı Başlangıç

```bash
# Projeyi klonlayın
git clone [https://github.com/](https://github.com/)<your-username>/technews-scraper.git
cd technews-scraper

# Sanal ortam oluşturun ve bağımlılıkları yükleyin
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Çalıştırın
python -m src