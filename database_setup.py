import pandas as pd
import sqlite3
import os

DB_NAME = 'inventory.db'
CSV_FILE = 'vehicles.csv'

def setup_database():
    print(f"[{CSV_FILE}] dosyası okunuyor ve veritabanı oluşturuluyor. Lütfen bekleyin, bu işlem dosyanın boyutuna (1.4GB+) bağlı olarak birkaç dakika sürebilir...")
    
    # Veritabanı bağlantısı
    conn = sqlite3.connect(DB_NAME)
    
    # Kullanılacak sütunlar
    usecols = ['id', 'price', 'year', 'manufacturer', 'model', 'condition', 'cylinders', 'fuel', 'odometer', 'title_status', 'transmission', 'paint_color']
    
    # Dosyayı parça parça oku (Chunking)
    chunk_size = 50000
    try:
        for chunk in pd.read_csv(CSV_FILE, chunksize=chunk_size, usecols=usecols, low_memory=False):
            # Temel temizlik: model, manufacturer (make) ve price sütunu boş olanları atlayalım
            chunk = chunk.dropna(subset=['manufacturer', 'model', 'price', 'year'])
            
            # Fiyatı 0 veya anlamsız olanları filtreleyelim
            chunk = chunk[chunk['price'] > 0]
            
            # API aracı ile uyumlu olmak için sütun adlarını değiştiriyoruz
            chunk = chunk.rename(columns={'manufacturer': 'make', 'paint_color': 'color'})
            
            # Veritabanına yaz
            chunk.to_sql('vehicles', conn, if_exists='append', index=False)
            print(f"{len(chunk)} adet temizlenmiş kayıt eklendi...")
            
    except FileNotFoundError:
        print(f"HATA: '{CSV_FILE}' bulunamadı. Lütfen Kaggle veri setini bu dizine koyduğunuzdan emin olun.")
        return

    # Arama hızlandırmak için index ekle
    print("İndeksler oluşturuluyor, bu işlem sorguları hızlandıracaktır...")
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_make ON vehicles(make);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_model ON vehicles(model);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON vehicles(price);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_year ON vehicles(year);")
    conn.commit()
    conn.close()
    
    print("Veritabanı kurulumu başarıyla tamamlandı!")

if __name__ == "__main__":
    if os.path.exists(DB_NAME):
        print(f"Uyarı: '{DB_NAME}' zaten mevcut. Yeniden oluşturmak istiyorsanız dosyayı silin.")
    else:
        setup_database()
