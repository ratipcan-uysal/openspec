# Domain bağlamının giriş noktası

Bu dosya ve altındaki şablonlar eğitim önerisidir; OpenSpec zorunlu formatı değildir.
<...> alanlarını gerçek kaynaklarla doldurun. Bilinmeyeni bilinmiyor bırakın.

## Ürün sınırı
- Ürün / domain / hedef kullanıcı: <...>
- Domain sahibi / teknik sahip / QA sahibi: <...>
- Bir sonraki gerçek iş: <tek kullanıcı sonucu>
- Başarı sinyali ve mevcut ölçüm kaynağı: <...>
- Kapsam dışı: <...>

## Repo eşlemesi
| Rol | Repo kimliği | Bu makinedeki checkout | Branch/commit | İlgili alan |
| --- | --- | --- | --- | --- |
| Planlama | <remote> | <yerel yol> | <...> | openspec/ |
| Mobil | <remote> | <yerel yol> | <...> | <akış dizini> |
| Backend | <remote> | <yerel yol> | <...> | <domain dizini> |

Yerel yollar kişiye özgüdür; takım dokümanında remote/repo kimliğini esas alın.
Asistana checkout yollarını oturumda ayrıca verin ve erişimini doğrulatın.

## Okuma sırası
1. sources.md: kaynak kimliği, sürüm, güncellik, otorite.
2. domain.md: sözlük, kurallar, sahipler ve kararlar.
3. flow.md: incelenen işin uçtan uca mevcut davranışı.
4. İlgili API sözleşmesi, kod sembolleri ve testler.
5. İlgili openspec/specs/... ve aktif change belgeleri.

## Bağlamı yenileme
API/kural/flag değişince, yeni app veya backend release'i çıkınca ve yeni işe
başlarken etkilenen kayıtları yeniden inceleyin. İnceleyen, tarih ve kaynak
sürümünü güncelleyin. Eski bilgiyi yeni doğrulanmış bilgi gibi kullanmayın.
