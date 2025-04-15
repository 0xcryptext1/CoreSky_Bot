# CoreSky Otomatik Login ve Checkin Uygulaması

Bu uygulama, CoreSky platformunda otomatik olarak giriş yapma, görev tamamlama ve puan sorgulama işlemlerini gerçekleştirir.

## Özellikler

- Ethereum cüzdanları ile otomatik giriş
- İmzalama ile günlük görev tamamlama
- Güncel puan bilgisi sorgulama
- Proxy desteği
- Ayarlanabilir bekleme süreleri
- Kaldığı yerden devam edebilme

## Gereksinimler

- Python 3.6 veya daha yeni
- Aşağıdaki Python kütüphaneleri:
  - `requests`
  - `eth-account`
  - `web3`

## Kurulum

1. Gerekli Python kütüphanelerini yükleyin:
   ```
   pip install requests eth-account web3
   ```

2. Dosyaları indirin ve klasöre çıkarın.

3. `wallets.txt` dosyasını oluşturun ve her satıra bir cüzdan bilgisi ekleyin:
   ```
   0xCÜZDAN_ADRESİ,ÖZEL_ANAHTAR
   0xCÜZDAN_ADRESİ2,ÖZEL_ANAHTAR2
   0xCÜZDAN_ADRESİ3,ÖZEL_ANAHTAR3
   ```

4. (İsteğe bağlı) Proxy kullanmak istiyorsanız, `proxy.txt` dosyasını oluşturun ve her satıra bir proxy bilgisi ekleyin:
   ```
   IP:PORT:KULLANICI_ADI:ŞİFRE
   ```

## Kullanım

1. `run.bat` dosyasını çalıştırın veya komut satırından şu komutu verin:
   ```
   python checkin.py
   ```

2. Uygulama başladığında aşağıdaki ayarları yapabilirsiniz:
   - Proxy kullanımı (E/H)
   - Minimum bekleme süresi (saniye)
   - Maksimum bekleme süresi (saniye)

3. Program otomatik olarak tüm cüzdanlar için işlemleri gerçekleştirir ve sonuçları ekranda gösterir.

## Dosya Açıklamaları

- `checkin.py`: Ana program dosyası
- `wallets.txt`: Cüzdan adresleri ve özel anahtarları
- `proxy.txt`: (İsteğe bağlı) Proxy bilgileri
- `position.txt`: Program tarafından oluşturulan, kaldığı cüzdan pozisyonunu kaydeden dosya

## Kod İşlevleri

### `sign_message(private_key, message)`
Ethereum cüzdanı ile belirtilen mesajı imzalar.

### `login(address, signature, proxies)`
CoreSky platformuna giriş yapar ve token alır.

### `sign_taskwall(token, proxies)`
Günlük görevleri tamamlamak için taskwall API'sine istek gönderir.

### `get_score(token, address, proxies)`
Kullanıcının güncel puanını sorgular.

### `load_proxies()`
Proxy listesini dosyadan yükler.

### `get_proxy(index, proxies, use_proxy)`
Belirtilen index için uygun proxy yapılandırmasını döndürür.

## Güvenlik Notları

- Özel anahtarlarınızı güvenli bir şekilde saklayın, başkalarıyla paylaşmayın.
- Proxy kullanımı önerilir ancak zorunlu değildir.
- Program her 4 işlemden birinde proxy kullanmadan işlem yapmaktadır.

## Sorun Giderme

- API hataları alıyorsanız, bekleme sürelerini artırmayı deneyin.
- Proxy sorunları yaşıyorsanız, proxy'lerinizin çalıştığından emin olun veya proxy kullanımını kapatın.
- Program beklenmedik şekilde kapanırsa, `position.txt` dosyası sayesinde kaldığı yerden devam edebilirsiniz.
