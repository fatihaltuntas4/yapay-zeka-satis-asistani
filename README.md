# Otonom Çok Amaçlı Satış Temsilcisi (AI Sales Agent)

Bu proje, Kaggle Craigslist araç veri seti kullanılarak geliştirilmiş, sadece konuşmakla kalmayıp harekete geçen ve veritabanı sorguları yapabilen diyalog tabanlı bir yapay zeka satış temsilcisidir.

## 🏗️ Sistem Tasarımı

Sistem 4 temel modülden oluşmaktadır:

1. **Veri Katmanı (`database_setup.py` & SQLite)**: 
   Yaklaşık 1.5 GB'lık Craigslist veri seti (CSV) Pandas kullanılarak okunur, temizlenir (eksik ve geçersiz veriler filtrelenir) ve performans için indeksler oluşturularak bir SQLite veritabanına (`inventory.db`) aktarılır. Bu yapı, LLM'in hızlı ve SQL tabanlı sorgular yapabilmesine olanak tanır.
   
2. **Araçlar (Tools) Katmanı (`tools.py`)**: 
   Ajanın envanterle iletişim kurmasını sağlayan Python fonksiyonlarını içerir. `search_inventory` fonksiyonu; marka, model, maksimum fiyat, renk ve yıl parametrelerini alarak veritabanında esnek SQL sorguları çalıştırır ve sonuçları yapılandırılmış JSON formatında ajana döndürür.

3. **LLM & Ajan Katmanı (`agent.py`)**: 
   LangChain ve OpenAI Function Calling mimarisi üzerine kuruludur. Kullanıcının doğal dil sorgusunu alır, niyetini anlar, gerekirse `search_inventory` aracını çağırarak elde ettiği JSON yanıtını tekrar doğal dile çevirerek kullanıcıya sunar. Ajan, satış temsilcisi karakterine bürünecek şekilde özel bir "System Prompt" ile yönlendirilmiştir.

4. **Kullanıcı Arayüzü (`main.py`)**: 
   Kullanıcıyla sohbeti başlatan, etkileşimi sürdüren ve sohbet geçmişini (memory) tutan komut satırı (CLI) uygulamasıdır.

## 🚀 Kurulum Talimatları

### 1. Gereksinimler
- Python 3.8+
- [Kaggle Craigslist Cars + Trucks Veri Seti](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data)

### 2. Adım Adım Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone <repo_linki>
   cd <repo_klasoru>
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Kaggle'dan indirdiğiniz `vehicles.csv` dosyasını proje ana dizinine kopyalayın.

4. Veritabanını oluşturun (Bu işlem dosya boyutuna bağlı olarak birkaç dakika sürebilir):
   ```bash
   python database_setup.py
   ```

5. API Anahtarınızı ayarlayın:
   Proje dizininde `.env` adında bir dosya oluşturun ve içine Google AI Studio'dan aldığınız API anahtarınızı ekleyin:
   ```env
   GOOGLE_API_KEY=sizin_api_anahtariniz_buraya
   ```

6. Ajanı Başlatın:
   ```bash
   python main.py
   ```

## 💬 Örnek Konuşmalar

**Kullanıcı:** Merhaba, 20.000 doların altında mavi bir Honda Civic var mı?
**Temsilci:** Düşünüyor (Envanter aranıyor)...
**Temsilci:** Merhaba! Evet, elimizde aradığınız kriterlere uygun harika seçenekler var. Örneğin 2012 model mavi bir Honda Civic sadece 8.500 dolar! Ayrıca 2013 model başka bir mavi Civic'imiz 14.500 dolar. Hangisinin detaylarını istersiniz veya linkini paylaşmamı tercih eder misiniz?

**Kullanıcı:** Peki ya 15.000 altına siyah Ford var mı?
**Temsilci:** Düşünüyor (Envanter aranıyor)...
**Temsilci:** Harika bir bütçe! Elimizde 15.000 dolar altında siyah Ford seçeneklerimiz mevcut. Örneğin 2015 model siyah bir Ford Focus 12.000 dolar, 2018 model bir Ford Fiesta ise 14.200 dolar. İlginizi çeken bir model oldu mu?

**Kullanıcı:** Kırmızı Ferrari arıyorum.
**Temsilci:** Düşünüyor (Envanter aranıyor)...
**Temsilci:** Maalesef şu anda envanterimizde kırmızı bir Ferrari bulunmuyor. Dilerseniz size spor hissi verebilecek kırmızı renkli Ford Mustang veya Chevrolet Camaro modellerimize bakabiliriz. Ne dersiniz?

## 🐍 Python, Yapay Zeka (AI) ve GitHub'ın Projedeki Rolleri

### 1. Python'ın Rolü
Python, projenin **iskeletini ve veri işleme motorunu** oluşturur:
- **Veri İşleme:** 1.5 GB boyutundaki devasa CSV dosyasının `pandas` yardımıyla bellek dostu (chunking) yöntemle işlenmesini ve `sqlite3` modülü ile SQL veritabanına aktarılmasını sağlar.
- **Arayüz ve Entegrasyon:** Komut satırı (CLI) uygulamasının hızlı ve temiz bir şekilde kodlanmasına imkan tanır.
- **Orkestrasyon:** LangChain framework'ünü barındırarak veri katmanı ile yapay zeka katmanı arasındaki köprüyü kurar.

### 2. Yapay Zeka (AI) Bileşenlerinin Rolü
Yapay zeka (LLM), sisteme **akıl ve otonom karar verme yeteneği** kazandırır:
- **Doğal Dil Anlama (NLU):** Kullanıcının "10 bin dolar altına kırmızı renkli aile arabası var mı?" şeklindeki karmaşık ve düzensiz cümlelerini anlar.
- **Otonom Araç Çağrısı (Function Calling):** Kullanıcı cümlesinden `max_price=10000`, `color='red'` gibi parametreleri çıkararak `search_inventory` fonksiyonunu ne zaman çağıracağına kendisi karar verir.
- **Doğal Dil Üretimi (NLG):** Veritabanından dönen soğuk ve yapılandırılmış JSON verisini (fiyat, model, link vb.) analiz ederek, müşteriyi ikna edecek kibar ve profesyonel bir satış temsilcisi yanıtına dönüştürür.

### 3. GitHub'ın Rolü
GitHub, projenin **versiyon kontrolü, işbirliği ve sunum** aşamalarında kritik rol oynar:
- **Versiyon Kontrolü:** Projenin gelişim sürecindeki tüm değişiklikler düzenli ve anlamlı commit mesajlarıyla kayıt altına alınmıştır.
- **Dosya Güvenliği (`.gitignore`):** Git takibine takılmaması gereken büyük boyutlu verilerin (`vehicles.csv`, `inventory.db`) ve gizli API anahtarlarının (`.env`) GitHub'a yüklenmesini engelleyerek güvenliği sağlar.
- **Belgelendirme ve Dağıtım:** Kapsamlı bir `README.md` dosyasıyla projenin kurulumu ve çalışma prensipleri açıkça belgelenerek başkaları tarafından kolayca incelenebilmesini sağlar.

---

## 🧠 Zorluklar ve Öğrenilenler

**Zorluklar:**
- **Büyük Veri Yönetimi:** 1.5 GB boyutundaki CSV dosyasını tek seferde belleğe almak (Pandas ile) sistem kaynaklarını tüketiyordu. Bu sorunu aşmak için dosyayı `chunksize` ile parçalara bölerek okuma ve SQLite'a parça parça yazma (`chunk.to_sql`) yöntemi geliştirildi.
- **Parametre Çıkarımı:** Kullanıcının doğal dilinden "20.000 altı" veya "2015 ve sonrası" gibi ifadeleri doğru bir şekilde API argümanlarına dönüştürmesini sağlamak için Function Calling ve LLM prompt tasarımı üzerinde hassas ayarlamalar yapıldı.
- **Hız ve Performans:** Milyonlarca satırlık veritabanında LLM'in yaptığı sorguların hızlı dönmesi için SQLite üzerinde sık aranan sütunlara (make, model, price) `INDEX` yapısı eklendi.

**Öğrenilenler:**
- LangChain ve yapay zeka modelinin birlikte ne kadar güçlü çalıştığı deneyimlendi.
- Bir uygulamanın arka planında veri ile LLM'i bir araya getiren "Agentic" (Ajan tabanlı) sistem mimarisi daha iyi kavrandı.
- Büyük veri setlerini veritabanlarına aktarırken Pandas chunking yönteminin ve SQL indekslemenin önemi uygulamalı olarak görüldü.

