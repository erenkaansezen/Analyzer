# Google Play Yorum Analizi

Bu proje, bir  uygulamanın Google Play’deki kullanıcı yorumlarını otomatik olarak toplayıp analiz eder. 

---

## Teknik Cevap

├── Yorum analizi için hangi NLP modeli/kütüphaneyi kullandınız ve neden?
- Çok dilli ve rakamsal çıktı ve güven skoru veriyor
- model olarak  nlptown/bert-base-multilingual-uncased-sentiment`,kütüphane ise Hugging Face `transformers.pipeline`  

├──Sahte yorum tespiti için hangi stratejiyi izlediniz?
- all-MiniLM-L6-v2 ile gömme vektörüne çevirip DBSCAN ile kümeleme işlemi yaptım  
- Kümelere dahil olamayan outlier yorumları -1 olarak etiketleyerek sahte yorum olarak belirledim.

├──Duygu skorlarını nasıl hesapladınız?
- Hugging Face pipeline’ın sağladığı score değerini kullandım.  
- BERT temelli hazır çözüm kullandım

├──İlginç yorumları seçmek için hangi yöntemi kullandınız?
- Bunu keyword belirlemeleri ile sağladım çoğunlukla, önerici yorumlardan anahtar kelimeler üzerinden analiz ederek verileri sağladım.

├──Yorum scraping’i nasıl yaptınız? Veriler güncellenebilir mi?
- google-play-scraper’ın reviews_all fonksiyonunu, pycountry ile tüm dillerde döngüye alarak kullandım.  
- script’i düzenli çalıştırarak güncel tutabilirsiniz.

├──Projeyi ölçeklenebilir ve gerçek zamanlı hâle nasıl getirirdiniz?
-Bir ilerleyiş seneryosu kurmak gerekirse eğer verileri sürekli güncel tutucak şekilde yenilemesi için yukarıda bahsettiğim gibi sctrip'i task scheduler ile
düzenli aralıklarla yenilerim ardından  her yenilemede bir database üzerinde verileri tutarım. Kullanıcıdan bir istek geldiğinde ilk kısa süreli bir cache kontrol eder
eğer  yok ise database üzerinde tuttuğum güncel verileri arayüz üzerinde gösteririm

