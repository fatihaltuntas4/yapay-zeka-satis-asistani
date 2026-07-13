import sys
from agent import create_agent_executor

def main():
    print("Satış Temsilcisi Yükleniyor...")
    
    try:
        agent_executor = create_agent_executor()
    except ValueError as e:
        print(f"\n[HATA] {e}")
        print("Lütfen projenin bulunduğu dizinde '.env' adında bir dosya oluşturun.")
        print("İçerisine şu satırı ekleyin:\nGOOGLE_API_KEY=sizin_api_anahtariniz\n")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("Merhaba! Ben Otonom Satış Temsilcisiyim.")
    print("Size nasıl bir araç bulmamı istersiniz?")
    print("Örnek: '20.000 doların altında mavi bir Honda Civic var mı?'")
    print("Çıkmak için 'q' veya 'quit' yazabilirsiniz.")
    print("="*50 + "\n")
    
    chat_history = []
    
    while True:
        try:
            user_input = input("Siz: ")
            
            if user_input.lower() in ['q', 'quit', 'çıkış', 'kapat']:
                print("Temsilci: İyi günler dilerim! Bizi tercih ettiğiniz için teşekkürler.")
                break
                
            if not user_input.strip():
                continue
                
            print("Temsilci: Düşünüyor (Envanter aranıyor)...")
            
            # Geçmişe kullanıcının mesajını ekle
            chat_history.append({"role": "user", "content": user_input})
            
            # Ajanı çalıştır
            response = agent_executor.invoke({
                "messages": chat_history
            })
            
            # Ajanın cevabını al
            bot_response_raw = response['messages'][-1].content
            if isinstance(bot_response_raw, list):
                # Liste içindeki text tipli kısımları birleştir
                bot_response = "\n".join([part['text'] for part in bot_response_raw if isinstance(part, dict) and 'text' in part])
            else:
                bot_response = str(bot_response_raw)
            
            print(f"\nTemsilci: {bot_response}\n")
            
            # Geçmişi güncelle (Tüm yeni mesajlar)
            chat_history = response['messages']
            
            # Çok uzamaması için son 10 mesajı tutalım
            if len(chat_history) > 10:
                chat_history = chat_history[-10:]
                
        except KeyboardInterrupt:
            print("\nÇıkış yapılıyor...")
            break
        except Exception as e:
            print(f"\n[BİR HATA OLUŞTU]: {e}\n")

if __name__ == "__main__":
    main()
