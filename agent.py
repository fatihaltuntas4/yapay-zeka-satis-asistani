from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

# Aracı LangChain aracı olarak tanımla
from tools import search_inventory as search_inventory_func

def search_inventory(make: str = None, model: str = None, max_price: float = None, color: str = None, year: int = None) -> str:
    """
    Kullanıcının belirttiği kriterlere göre araç envanterini (SQLite veritabanı) arar.
    
    Args:
        make (str, optional): Aracın markası (örn: honda, toyota, ford).
        model (str, optional): Aracın modeli (örn: civic, camry, f-150).
        max_price (float, optional): Kullanıcının ödemek istediği maksimum fiyat limiti.
        color (str, optional): Aracın rengi. (örn: blue, red, black).
        year (int, optional): Aracın minimum yılı. Eğer "2015 ve sonrası" denirse year=2015 olur.
        
    Returns:
        JSON string formatında arama sonuçları. En fazla 5 araç döner.
    """
    return search_inventory_func(make, model, max_price, color, year)

def create_agent_executor():
    # API Anahtarını kontrol et
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı ayarlayın.")
        
    # Model oluştur
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
    
    # Araçları listeye ekle
    tools = [search_inventory]
    
    # Sistemi oluştur
    system_prompt = """Sen yetenekli ve kibar bir araç satış temsilcisisin. 
Kullanıcıların istedikleri araçları bulmalarına yardımcı oluyorsun.
Sana verilen `search_inventory` aracını kullanarak veritabanımızdan araçları sorgulayabilirsin.

Eğer kullanıcı bir araç sorarsa, aracı çağır.
Gelen sonuçları (fiyat, yıl, marka, model, renk, durum vb.) doğal ve ikna edici bir dille kullanıcıya sun.
Eğer sonuç bulunamazsa, kibarca bu kriterlere uygun araç olmadığını belirt ve farklı kriterler önermesini iste.
Kesinlikle uydurma veri kullanma, sadece aramanın sonucunda dönen verileri söyle.
Araçların linklerini (url) varsa mutlaka kullanıcıya ver."""

    # Ajanı oluştur
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return agent
