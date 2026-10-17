# Package Change

## Purpose
Paket değişikliği sonucunu kullanıcıya doğru durumla göstermek.
Bu başlangıç davranışı eğitim örneğidir, gerçek repo bulgusu değildir.

## Requirements

### Requirement: Gönderim sonucu
Sistem başarılı kabul yanıtında talebin alındığını göstermelidir (MUST).
Yanıt alınamazsa sistem genel hata göstermelidir (MUST).

#### Scenario: Kabul yanıtı alınır
- GIVEN kullanıcı uygun bir paket değişikliği gönderdi
- WHEN backend talebi kabul etti ve yanıt cihaza ulaştı
- THEN kullanıcı "Talebiniz alındı" görür

#### Scenario: Yanıt alınamaz
- GIVEN kullanıcı paket değişikliği gönderdi
- WHEN cihaz yanıt alamaz
- THEN kullanıcı genel hata görür
