import sqlite3
import json

DB_NAME = 'inventory.db'

def search_inventory(make: str = None, model: str = None, max_price: float = None, color: str = None, year: int = None) -> str:
    """
    Araç envanterini (SQLite veritabanı) sorgular ve JSON formatında sonuçları döndürür.
    
    Args:
        make (str, optional): Aracın markası (örn: honda, toyota).
        model (str, optional): Aracın modeli (örn: civic, camry).
        max_price (float, optional): Maksimum fiyat.
        color (str, optional): Aracın rengi.
        year (int, optional): Aracın minimum yılı (bu yıl ve sonrası araçlar).
        
    Returns:
        str: Sorgu sonuçlarının JSON string temsili. (En fazla 5 sonuç döndürür)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Sütun isimleriyle erişmek için
        cursor = conn.cursor()
        
        query = "SELECT make, model, year, price, color, odometer, condition, url FROM vehicles WHERE 1=1"
        params = []
        
        if make:
            query += " AND LOWER(make) = ?"
            params.append(make.lower())
        
        if model:
            # Model isimleri içinde kelime geçebileceği için LIKE kullanıyoruz
            query += " AND LOWER(model) LIKE ?"
            params.append(f"%{model.lower()}%")
            
        if max_price:
            query += " AND price <= ?"
            params.append(max_price)
            
        if color:
            query += " AND LOWER(color) = ?"
            params.append(color.lower())
            
        if year:
            # Verilen yıldan daha yeni araçları getir
            query += " AND year >= ?"
            params.append(year)
            
        # Sonuçları ucuzdan pahalıya sırala ve en fazla 5 sonuç al
        query += " ORDER BY price ASC LIMIT 5"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append(dict(row))
            
        conn.close()
        
        if not results:
            return json.dumps({"status": "error", "message": "Aradığınız kriterlere uygun araç bulunamadı."})
            
        return json.dumps({"status": "success", "results": results})
        
    except sqlite3.OperationalError:
        return json.dumps({"status": "error", "message": "Veritabanı bağlantı hatası. Lütfen önce database_setup.py dosyasını çalıştırın."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Test amaçlı
if __name__ == "__main__":
    print(search_inventory(make="honda", model="civic", max_price=20000, color="blue"))
