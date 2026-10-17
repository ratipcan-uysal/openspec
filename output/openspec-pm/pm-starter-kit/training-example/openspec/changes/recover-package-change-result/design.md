## Context
Temsili vakada istemci yanıt alamasa da sunucu kabul etmiş olabilir.
Bu eğitim taslağı bir çözüm yönü önerir; gerçek repo incelenmedi.
Ürün kabulü: delta spec. Uygulamaya geçiş için aşağıdaki açık teknik
kararlar mühendislikle tamamlanmalı.

## Goals / Non-Goals
Goals: aynı niyeti korumak, doğru durum göstermek, ekrana dönüşü toparlamak.
Non-Goals: fiyat/uygunluk politikasını değiştirmek, yeni geçmiş ekranı.

## Decisions (proposed; engineering review required)
- operationKey gönderimden önce istemcide oluşur, aynı niyette korunur.
  Yalnız yanıt içinde dönen requestId yeterli değil: yanıt kaybolabilir.
- Backend (authenticated user, operationKey) eşlemesini atomik tutar.
  Aynı key ve aynı payload aynı talebe bağlanır; farklı payload çelişki
  olarak ele alınır. Kesin davranış API sözleşmesinde netleşir.
- Yetkili durum sorgusu kabul / uygulanma / ret durumlarını ayırır.
- İstemci talep bağını kapanma/dönüş boyunca korur; hesap değişiminde
  başka kullanıcının talebini göstermez.

## Risks / Trade-offs
Eşzamanlı çift gönderim; key saklama süresi; eski istemci; geç gelen
sonuç; yetki sınırı; servis kesintisi; ölçümde aynı niyetin iki sayılması.

## Migration / Rollout
Backend uyumunu önce hazırla; eski mobil istemcileri ayrı doğrula.
Mobil sürüm/flag ve geri dönüş koşulunu ekipçe kararlaştır.
Sync/archive release yapmaz.

## Open Questions (block apply)
- Atomik eşlemenin mevcut altyapıdaki yöntemi ve testi nedir? Backend sahibi.
- Key saklama süresi / bitişte güvenli devam yolu nedir? PM + backend.
- Eski istemci ve payload uyumsuzluğu nasıl davranır? API + mobil sahipleri.
- Ret sözleşmesi, terminal durumlar ve yetki sınırı nedir? Domain + API.
- Hangi test ortamı, rollout/rollback ve gözlem koşulları? QA + release.
