## 1. Karar ve sözleşme
- [ ] 1.1 Design açık sorularını sahipleriyle çöz; spec ile hizala.
- [ ] 1.2 API durum/payload/ret/yetki sözleşmesini sürümle.
- [ ] 1.3 Eski istemci uyumu ve release/rollback sırasını kararlaştır.

## 2. Backend (yalnız kararlar tamamlandıktan sonra)
- [ ] 2.1 Aynı niyet eşlemesini atomik uygula; yeni niyeti ayrı tut.
- [ ] 2.2 Yetkili durum sorgusunu ve payload çelişkisini uygula.
- [ ] 2.3 Tekrar/eşzamanlılık/yetki testlerini çalıştır, kanıt kaydet.

## 3. Mobil
- [ ] 3.1 Niyet anahtarını ilk gönderimden önce üret ve dönüşte koru.
- [ ] 3.2 Belirsiz / alındı / uygulandı / ret gösterimlerini ayır.
- [ ] 3.3 Dönüş, hesap değişimi ve erişilemeyen durum senaryolarını doğrula.

## 4. Kabul ve kapanış
- [ ] 4.1 Tüm delta senaryolarını ortam/sürüm/test bağlantısıyla kaydet.
- [ ] 4.2 Başarısız ve çalıştırılmamış senaryoları görünür tut; PM/QA review.
- [ ] 4.3 Deltayı sync et; ana spec'i incele; tamamlanan işi archive et.
- [ ] 4.4 Gerçek release ve gözlem kaydını ayrı yürüt.
