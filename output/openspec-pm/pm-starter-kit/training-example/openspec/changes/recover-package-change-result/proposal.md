## Why
Eğitim vakasında backend talebi kabul etse de yanıt kaybolabiliyor.
Genel hata kullanıcıyı aynı niyeti yeniden göndermeye yöneltiyor.
Beklenen sonuç: belirsizliği doğru gösterip ikinci talebi önlemek.

## What Changes
- Doğrulanamayan sonucu belirsiz göster; kesin ret olarak etiketleme.
- Kabul edilen ve uygulanması doğrulanmış talebi ayrı göster.
- Aynı niyetin tekrarını aynı talebe bağla.
- İlgili ekrana dönüşte doğrulanmamış talebi toparla.
- Kesin ret gerekçesini ve uygun devam yolunu göster.
Kapsam dışı: fiyat/fatura, uygunluk politikası, kampanya,
geçmiş talep ekranı ve yeni bildirim kanalı.

## Capabilities
### New Capabilities
- Yok.
### Modified Capabilities
- package-change: sonuç gösterimi, aynı niyet ve toparlanma davranışı.

## Impact
Mobil gönderim ve dönüş akışı; backend talep eşleme ve durum sorgusu;
API sözleşmesi; eski mobil sürüm uyumu; ilgili testler ve ölçüm.
Ürün kararları: bu eğitim için kararlaştırılmış örnek kurallar.
Gerçek işte kaynak/sürüm, karar sahipleri ve hedef ölçüm eklenir.
