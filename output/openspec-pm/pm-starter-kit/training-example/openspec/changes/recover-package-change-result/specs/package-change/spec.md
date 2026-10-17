## MODIFIED Requirements

### Requirement: Gönderim sonucu
Sistem yalnız doğrulanmış talep durumunu sonuç olarak göstermelidir (MUST).
Kabul edilmiş talebi "Talebiniz alındı", uygulanması doğrulanmış talebi
"Paketiniz uygulandı", doğrulanamayan sonucu "Sonuç kontrol ediliyor"
olarak göstermelidir (MUST). Kesin rette gerekçeyi ve uygun devam yolunu
sunmalıdır (MUST). Yanıt kaybı tek başına kesin ret değildir.

#### Scenario: Kabul yanıtı alınır
- GIVEN kullanıcı uygun paket değişikliği gönderdi
- WHEN backend talebi kabul etti ve yanıt cihaza ulaştı
- THEN "Talebiniz alındı" gösterilir
- AND paket uygulanmış gibi gösterilmez

#### Scenario: Yanıt alınamaz
- GIVEN talep gönderildi
- WHEN cihaz yanıt alamaz ve durum sorgusu da sonuç vermez
- THEN "Sonuç kontrol ediliyor" gösterilir
- AND kesin başarısızlık veya uygulanma gösterilmez

#### Scenario: Uygulanma doğrulanır
- GIVEN gönderilmiş bir talep var
- WHEN yetkili durum kaynağı uygulanmayı doğrular
- THEN "Paketiniz uygulandı" gösterilir

#### Scenario: Kesin ret doğrulanır
- GIVEN talep uygunluk nedeniyle kesin reddedildi
- WHEN yetkili durum kaynağı reti doğrular
- THEN uygunluk gerekçesi gösterilir
- AND kullanıcı paket seçimine geri dönebilir
- AND otomatik yeniden gönderim yapılmaz

## ADDED Requirements

### Requirement: Aynı niyetin tekrar gönderimi
Sistem aynı kullanıcı niyetinin tekrarında ikinci paket değişikliği
oluşturmamalıdır (MUST). Kullanıcının farklı yeni niyeti bağımsız
bir talep olarak ele alınmalıdır (MUST).

#### Scenario: Aynı niyet tekrar gönderilir
- GIVEN ilk gönderimin sonucu bilinmiyor
- WHEN aynı kullanıcı aynı niyeti tekrar gönderir
- THEN aynı talebin güncel durumu döndürülür
- AND ikinci talep oluşturulmaz

#### Scenario: Eşzamanlı tekrar
- GIVEN aynı niyetle eşzamanlı iki gönderim yapılır
- WHEN backend bu gönderimleri işler
- THEN en fazla bir talep kaydı oluşur
- AND iki yanıt aynı talebe bağlanır

#### Scenario: Yeni niyet
- GIVEN önceki talebin sonucu doğrulandı
- WHEN kullanıcı farklı bir paket seçip yeni değişikliği onaylar
- THEN bu niyet bağımsız talep olarak işlenir

### Requirement: Ekrana dönüşte toparlanma
Sistem ilgili ekrana dönen kullanıcı için önceki doğrulanmamış talebin
durumunu sorgulamalıdır (MUST). Durum yine doğrulanamazsa belirsiz
gösterimi korumalıdır (MUST).

#### Scenario: Uygulama yeniden açılır
- GIVEN talep gönderildikten sonra yanıt alınmadan uygulama kapandı
- WHEN aynı kullanıcı uygulamayı açıp paket değişikliği ekranına döner
- THEN önceki talebin durumu sorgulanır
- AND doğrulanırsa o sonuç gösterilir

#### Scenario: Dönüşte durum kaynağına erişilemez
- GIVEN önceki talebin sonucu doğrulanmadı
- WHEN kullanıcı döner fakat durum sorgusu sonuç vermez
- THEN "Sonuç kontrol ediliyor" korunur
- AND bu niyet için ikinci talep oluşturulmaz
