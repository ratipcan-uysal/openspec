# OpenSpec / PM ustalık sunumu — Astra anlatım ve sanat yönetimi planı

Hazırlayan: Astra alt ajanı. Tarih: 9 Ekim 2026. Teslim: bağımsız, çevrimdışı çalışan tek HTML için uygulanabilir plan. Bu belge kod değildir. Güven: resmi araç davranışları yüksek; eğitim ve sanat yönetimi seçimleri orta (tasarım yargısı); tüm vaka verileri açıkça temsili.

## 1. Önceki sunumun teşhisi

`content.json` ve 20 slaytlık `montage.webp` incelendi. Sorun yalnızca “daha güzel görünmesi” değil: içerik nesneleri gösterilmiyor, adları sayılıyor. Dört belge anlatılıyor ama gerçek bir proposal–spec–task ilişkisi görülmüyor. “Mobil ve backend” dört sütun; hiçbir istek kaybolmuyor, çelişki ortaya çıkmıyor, durum değişmiyor. Delta sözcüğü var, önce/sonra farkı yok. İzleyici doğru ilkeleri duyuyor fakat iş yapmayı deneyimlemiyor.

Görsel dilin yaklaşık tamamı başlık + küçük metin + bol boşluk. Bu boşluk bilgi hiyerarşisi üretmediği için premium değil, seyrek görünüyor. İki dekoratif mimari görsel mekanizmayı açıklamıyor. Açılışta gerçek problem yerine marka geliyor; sonunda yetkinlik ölçümü yerine genel bir ödev var. Önceki metinlerin önemli kısmı doğru ve yeniden kullanılabilir; aynı sıra ve şablon yeniden kullanılmamalı.

Yeni sunumun kabul sorusu: **“İzleyici bu sahnede daha önce göremediği hangi ilişkiyi gördü?”** Cevap yalnızca “dört maddeyi okudu” ise sahne yeniden tasarlanmalı.

## 2. Ana tez ve öğrenme sözleşmesi

**Tek tez:** OpenSpec, ürün niyetini incelenebilir bir davranış sözleşmesine, değişikliği de kalıcı ürün hafızasına bağlar.

İzleyici eğitimin sonunda şunları yapabilmeli:

1. Mevcut davranışın kanıtı, kabul edilen ürün kararı ve çözülmemiş soruyu ayırmak.
2. Dar kapsamlı bir işi AI’a yeterli kaynak ve sınırlarla başlatmak.
3. Proposal, spec, design ve tasks arasında yanlışlık ya da kapsam sızıntısı bulmak.
4. Bir gereksinimi gözlemlenebilir senaryolarla değerlendirmek; eksik hata yolunu göstermek.
5. Değişikliğin ana spec’e nasıl geçtiğini ve hangi kanıtlarla kapanabileceğini anlatmak.
6. Mobil/backend işi için ortak sözleşmeyi ve repo bazlı uygulama sorumluluğunu ayırmak.

Komut ezberlemek ve her beta ayrıntısını bilmek hedef değil. Kullanma, sorgulama ve doğru referansa gitme yetkinliği hedef. Ana akış 16 sahne, yaklaşık 28–32 dakika; atlas soru-cevap ve iş başı referansı. Sahne sayısı süre tahmini değildir: ilk beş kısa, spec ve inceleme sahneleri daha uzun.

## 3. Tek vaka: yanıtı kaybolan paket değişikliği

Her vaka sahnesinde sessiz fakat okunur “Temsili ürün · örnek kurallar” satırı. Hiçbir sahte dosya gerçek repo bulgusu gibi sunulmayacak. Kod ve yolların yanında “temsili kod” yazacak; uydurma commit SHA’sı kullanılmayacak.

**Mevcut temsili sorun:** Kullanıcı mobil uygulamada paket değişikliği gönderir. Backend talebi kabul eder. Yanıt mobil cihaza ulaşmaz. Mobil genel hata gösterir; kullanıcı işlemin yapılmadığını sanarak yeniden dener. Görülen sorun: kullanıcıya kesin başarısızlık söylenmesi ve tekrar işlemin belirsizliği.

**Tek değişiklik niyeti:** “Paket değişikliği yanıtı alınamadığında kullanıcıya doğru durum ve güvenli devam yolu sunmak.”

**Sabit temsili ürün kararları:**

- Sonucu doğrulanamayan gönderim “başarısız” gösterilmez; “Sonuç kontrol ediliyor” gösterilir.
- Aynı kullanıcı niyetinin tekrar gönderimi ikinci bir paket değişikliği oluşturmaz.
- Kabul edilen talep “alındı” olarak gösterilir; “paket aktif” ancak uygulanma doğrulanınca söylenir.
- Kullanıcı ekrana yeniden geldiğinde mevcut talebin durumu sorgulanır.
- Kesin ret halinde gerekçe ve uygun devam yolu gösterilir.

**Bilinçli olarak kapsam dışında:** fiyat/faturalama, uygunluk politikasını değiştirmek, kampanyalar, geçmiş talepler listesi, yeni bildirim kanalı. Geçerlilik zamanı için uydurma bir “24 saat” veya “sonraki dönem” kuralı koymayın. Vaka yalnızca sistemin bildirdiği zamanı gösterebilir; politika açık soru olarak kalır.

**İki ayrı durum kümesi:**

- Sunucudaki talep: kabul edildi → uygulanıyor → uygulandı; ilgili noktalardan reddedildi/başarısız olabilir. Bunlar örnek domain durumlarıdır.
- İstemcinin bilgisi: gönderiliyor → yanıt alındı / sonuç bilinmiyor → durum sorgulanıyor → doğrulanmış son durum.

“Sonuç bilinmiyor” sunucu iş durumu değildir. Sunumun en güçlü kavramsal düğümü budur.

**Örnek teknik yaklaşım (design kararı):** istemcinin gönderimden önce ürettiği `operationKey`; yeniden gönderimde aynı anahtar; backend aynı anahtarı aynı işleme eşler. `POST /package-changes`, `GET /package-changes/by-operation/{operationKey}` yolları temsili API tasarımıdır, OpenSpec özelliği değildir. POST yanıtı kaybolabileceği için yalnızca yanıtta dönen requestId ile toparlanma anlatılmamalı. Anahtar saklama süresi, yarışların atomikliği, yetkilendirme ve eski istemci uyumluluğu mühendisliğin çözmesi gereken tasarım sorularıdır; atlas bunları açıkça işaretler.

## 4. Sahne planı

### 01 — “Bir dokunuş. İki gerçek.”

**Ana mesaj:** Aynı işlem için mobil ve backend farklı gerçekler sunabilir; ürün belirsizliği burada kullanıcıya dönüşür.

**Kompozisyon:** Koyu fonda solda büyük, inandırıcı ama markasız mobil ekran: paket satırı, değiştir düğmesi, sonra “İşlem tamamlanamadı”. Sağda sunucu olay şeridi: “Talep kabul edildi”. İkisinin arasında yatay tek istek ve kesilen dönüş çizgisi. Ortada boşluk; dekor yok. “OpenSpec / ürün kararından doğrulanmış davranışa” küçük alt imza.

**Reveal:** 1 dokunma, 2 giden istek ve backend kabulü, 3 dönüş çizgisinde kopma ve mobil hata. Başlangıç otomatik hareket etmesin; anlatıcı ritmi yönetsin. Son karede iki sonucu eşzamanlı görünür tut.

**Anlatıcı:** “Kullanıcı açısından işlem olmadı. Sunucu açısından talep var. Şimdi ikinci kez dokunuyor. Ürünün ne yapması gerektiğini nerede kararlaştırdık?” Burada cevap istemek sahne içi öğretimdir; teknik bir test demosu yapıldığı izlenimi vermeyin.

### 02 — “Karar nerede kayboldu?”

**Ana mesaj:** Kısa talep, uygulama ayrıntılarını değil ürün kararlarını da açık bırakabilir.

**Kompozisyon:** Açık fonda yatay dönüşüm: solda tek cümlelik talep kâğıdı, ortada kopuk bir davranış köprüsü, sağda iki ayrılan uygulama çizgisi. Köprünün boş yerlerine “Yanıt yoksa?”, “Tekrar gönderirse?”, “Ne zaman aktif?” soruları oturur. Alt sırada bu soruların mobil, servis ve testte farklı varsayımlara dönüşmesi ince çizgilerle gösterilir.

**Reveal:** İlk kare yalnız talep ve sonuç. Sonraki adım eksik kararları ortaya çıkarır. Sonra boş köprüye “incelenmiş davranış sözleşmesi” yerleşir; bunu OpenSpec’in otomatik karar verdiği biçimde göstermeyin.

**Anlatıcı:** “Daha uzun ticket yazmak tek başına çözüm değil. Hangi durumda ne olacağını, hangi kararların henüz verilmediğini görünür kılmalıyız.”

### 03 — “OpenSpec: değişikliğin çalışma dosyası”

**Ana mesaj:** Kalıcı davranış referansı ve o referansa önerilen değişiklik ayrı tutulur.

**Kompozisyon:** Gerçek dosya yapısından üç zaman kesiti. Sol: `openspec/specs/package-change/spec.md` içinde mevcut bir gereksinim. Orta ve en büyük: `changes/recover-package-change/` ve bir küçük delta parçası. Sağ: güncellenmiş ana spec; altında küçülen tarihli archive dosyası. Oklar “öner”, “birleştir”, “geçmişi koru”. Masaüstü klasör ikonları yerine tipografik dosya sayfaları ve diff çizgileri.

**Reveal:** Orta delta sağdaki ana spec’e taşınır, change aşağıdaki arşive iner. İki farklı işlemi tek sihirli animasyonda eritmeyin.

**Anlatıcı:** “Ana spec bizim sürümlenen davranış referansımızdır. Canlı sistemin otomatik taranmış aynası değildir; güncelliğini ekip korur.” Kaynak: concepts / getting-started.

### 04 — “Önce sistemi okuyun”

**Ana mesaj:** AI’a bütün şirketi özetletmek yerine bir kullanıcı akışının kaynaklarını izletin.

**Kompozisyon:** Geniş bir iki-repo kesiti. Sol mobil: `PackageChangeViewModel.submit()` temsili 4 satır; orta API sözleşmesi; sağ backend `PackageChangeService.submit()` temsili 4 satır; altta test izi. Seçili satırlar bir iz rotasıyla birleşir. İlgisiz dosyalar soluk birkaç isim olarak periferiye çekilir.

**Reveal:** “Gönder” tıklandığında hat boyunca mobil catch bloğu → POST → backend kabulü → test adımı sırayla aydınlanır. Son adım kanıt kaydı: kaynak yolu, sembol, incelenen sürüm, bulgu, bilinmeyen.

**Anlatıcı:** “Repo erişimi, branch/commit ve ilgili domain dokümanlarını sağlayın. Bir repo adını yazmak erişim sağlamaz. Koddan canlı konfigürasyonu, yayımlanan sürümü veya iş niyetini kesinleştiremeyiz.” Kaynak: existing-projects; kanıt kaydı bu eğitimin önerisi.

### 05 — “Kod kanıttır. Ürün kararı size aittir.”

**Ana mesaj:** Gözlenen uygulama ile olması gereken davranış aynı bilgi türü değildir.

**Kompozisyon:** İncelemeci masası: solda iki kanıt parçası, ortada çatışma, sağda karara bağlanacak boş sözleşme satırı. Mobil kanıtı: “timeout → genel hata”. Backend kanıtı: “talep daha önce kabul edilmiş olabilir”. Bunların arasına “hangisi doğru?” yazmak yerine “beklenen kullanıcı davranışı?” oku. Alt küçük çizgi: gözlendi / bilinmiyor / kararlaştırıldı, renk ve açık metinle.

**Reveal:** “AI önerisini göster” eylemi hatalı “timeout olursa başarısız say” cümlesini açar. “Kararı düzelt” eylemi bu cümleyi redline ile değiştirir: “Sonuç doğrulanana kadar belirsizlik gösterilir.”

**Anlatıcı:** “AI çelişkiyi gösterebilir. Hangi davranışı ürün sözüne dönüştüreceğimizi ekip belirler. Fiyat veya geçerlilik kuralını kod boşluğundan icat etmesine izin vermeyin.”

### 06 — “Bir değişiklik, tek niyet”

**Ana mesaj:** Küçük ama uçtan uca bir sonuç, incelenebilir bir change üretir.

**Kompozisyon:** Gerçek `proposal.md` görünümlü tek büyük sayfa. Neden, Değişecek Davranış, Etkilenen Alanlar başlıkları altında vakaya özel toplam 70–90 kelime. Yanında sayfa dışına çıkan soluk talepler: “kampanya önerisi”, “geçmiş talepler”, “faturalama yenileme”. Sayfanın kenar çizgisi kapsam sınırıdır; kutu kartları yok.

**Reveal:** Yeni özellikler sayfanın içine sızmaya çalışır; anlatıcı “Kapsamı daralt” ile dışarı alır. Bu dramatizasyon yalnız iki adım.

**Anlatıcı:** “Sınır, AI’ın kaliteli görünen ama başka problemi çözen kapsam üretmesini engeller.” Beklenen net niyet yukarıdaki vaka cümlesidir.

### 07 — “Dört belge, tek tutarlılık zinciri”

**Ana mesaj:** Belgeler ayrı formlar değil, aynı kararın farklı görünümleridir.

**Kompozisyon:** Dört küçük gerçek belge kesiti tek açık çalışma yüzeyinde; en büyük spec. Proposal’da “belirsiz sonucu toparlama”; spec’te gözlemlenebilir davranış; design’da `operationKey`; tasks’te “aynı anahtarla tekrar gönderimi uygula ve test et”. Aynı kararın kelimeleri ince iz çizgisiyle birbirine bağlı. Alt yazı: varsayılan `spec-driven` yapısı.

**Reveal:** Bir gereksinim seçildiğinde ona bağlı tasarım ve görev parçası aydınlanır. “Kuyruk teknolojisi” ifadesi spec’ten design’a taşınır: ne / nasıl ayrımı somutlaşır.

**Anlatıcı:** “PM niyet ve davranışı, mühendislik teknik yaklaşımı, QA senaryo yeterliliğini birlikte değerlendirir. Bu sahiplik önerimizdir; araç rol atamaz. Design bir ekran tasarımı dosyası değildir.”

### 08 — “Sözleşme iki repo arasında yaşar”

**Ana mesaj:** Kullanıcı sözü, mobil ve servis sınırındaki ortak davranışla taşınır.

**Kompozisyon:** Gerçek sequence diagram: Kullanıcı / Mobil / API / Talep kaydı olmak üzere dört dikey hat. Geniş oklar yalnız kritik adımlar. POST üzerinde `operationKey: K1`; backend kabulü; dönüşte kopma; mobil durum sorgusu aynı anahtarla; doğrulanmış “alındı”. Sağ alt küçük telefon kesiti o anki metni gösterir.

**Reveal:** İki alternatif kontrol: “Yanıt ulaştı” / “Yanıt kayboldu”. Aynı görsel topolojiyi değiştirmeden iki akışı göster. İkinci gönderim aynı K1 ile aynı talebe döner. Bu etkileşim öğretim simülasyonudur, API çağrısı yapmaz.

**Anlatıcı:** “İşlem anahtarını örnek teknik çözüm olarak seçtik. Ürün gereksinimi ikinci işlem yaratmamak; bunun nasıl garanti edileceği tasarım ve test konusudur.”

### 09 — “Belirsizlik de bir durumdur”

**Ana mesaj:** Sunucudaki işlem durumu ile istemcinin bildiği durum ayrılmalı.

**Kompozisyon:** İki katmanlı durum makinesi. Üstte sunucu: kabul edildi → uygulanıyor → uygulandı. Altta istemci: gönderiliyor → sonuç bilinmiyor → durum sorgulanıyor → doğrulanmış sonuç. Dikey kesikli çizgiler bilgi edinimini temsil eder. “Bilinmiyor” düğümü sıcak kehribar; başarısızlık düğümü kızıl, birbirinden ayrı.

**Reveal:** “Bağlantıyı kes” ile yalnız alt katman bilinmiyor durumuna geçer; üst katman yürüyebilir. “Ekrana dön” ile sorgulama ve toparlanma yolu belirir.

**Anlatıcı:** “Timeout, sunucudaki işlemin başarısız olduğuna dair tek başına kanıt değildir. ‘Talep alındı’ da ‘paket aktif’ demek değildir.” İki bağımsız yanılgıyı aynı sahnede ayırın.

### 10 — “İyi spec, sınanabilir cümledir”

**Ana mesaj:** Requirement davranış sözünü, scenario o sözü sınayacak belirli koşulu taşır.

**Kompozisyon:** Sol %55 gerçek Markdown; sağ %45 üç karelik kullanıcı deneyimi şeridi. Kaynak biçimini koruyun:

```markdown
### Requirement: Belirsiz sonucun gösterimi
Sistem, gönderimin sonucu doğrulanamıyorsa kullanıcıya
“Sonuç kontrol ediliyor” durumunu göstermelidir (MUST).

#### Scenario: Kabul yanıtı cihaza ulaşmaz
- GIVEN paket değişikliği talebi gönderildi
- WHEN istemci yanıtı alamadı ve sonuç doğrulanamadı
- THEN kullanıcı “Sonuç kontrol ediliyor” durumunu görür
```

**Reveal:** GIVEN / WHEN / THEN satırları sırayla sağdaki bağlam / olay / gözlenen sonuca bağlanır. İkinci örnek sekmesi: “Aynı talebi yeniden gönderme” ayrı requirement ve scenario; tek gereksinime bütün kapsamı doldurmayın.

**Anlatıcı:** “Yalnızca ‘hataları düzgün yönetir’ yazsaydık hangi testi yazacağımızı bilemezdik. Bunu testi yazacak kişiye verdiğimizde sonucu gözleyebiliyor mu?”

### 11 — “Değişikliği yazın; ürünü yeniden yazmayın”

**Ana mesaj:** Delta, var olan referansa göre ekleme, değiştirme veya kaldırma tarifidir.

**Kompozisyon:** Üç panelli gerçek diff masası: Önce / Delta / Sonra. Solda mevcut requirement “Gönderim sonucu”; ortada `## MODIFIED Requirements` altında tam yeni requirement ve senaryosu; sağda eski bloğun yerine geçen yeni blok. Değişmeyen uygunluk gereksinimi her iki uçta aynı gri satır olarak korunur.

**Reveal:** Birleştir ile yalnız hedef blok değişsin. Yan küçük seçim “Yeni yetenek olsaydı?” ile ADDED örneği. REMOVED atlas bağlantısı yeterli; ana sahnede üç dev metin göstermeyin.

**Anlatıcı:** “MODIFIED yalnız ‘şu cümleyi değiştir’ notu değildir: gereksinimin yeni tam hâlini içerir. Mevcut spec’te gereksinim yoksa hayali bir tabanı değiştirmiyoruz; yeni spec davranışı ADDED ile kurulabilir. Bu vakada mevcut ana spec olduğunu varsaydık.”

### 12 — “AI taslağına itiraz edin”

**Ana mesaj:** İyi PM incelemesi, akıcı metnin gizlediği yanlış kararları yakalar.

**Kompozisyon:** Tek belge üzerinde gerçek redline incelemesi. Üç numaralı satır: “Talep 24 saat içinde uygulanır”, “Tüm hatalarda yeniden gönder”, “Geçmiş talepler ekranı ekle”. Kenarda üç inceleme gerekçesi için boş alan. UI bir doküman incelemesi gibi; quiz oyun kartları gibi değil.

**Reveal:** Satır tıklanınca sırasıyla “Kaynağı olmayan iş kuralı”, “Belirsiz sonucu başarısızlık sayıyor”, “Kapsam dışı” görünür. Son düğme temizlenmiş taslağı gösterir. Kullanıcı bir kez yanlış yeri seçerse moral veren animasyon yok; yalnız gerekçe.

**Anlatıcı:** “Üç satır da profesyonel yazılmış olabilir. İyi yazılmış olması doğru olduğu anlamına gelmez.” İnceleme sırası proposal → specs → tasks; teknik yaklaşım gerektiğinde mühendislikle.

### 13 — “Komut değil, çalışma döngüsü”

**Ana mesaj:** Öğrendikçe planı düzeltir, uygulamayı yeni plana uydurur ve sonra kapatırsınız.

**Kompozisyon:** Lineer tren yerine ortasında gerçek change klasörü olan sade döngü. Sol explore → üst propose → sağ apply → alt inceleme → archive. `update` plan belgelerine geri bağlanan görünür yan yol. `sync` ana spec’e giden ayrı dal. İnceleme bir ekip eylemi; komutmuş gibi `/opsx:review` yazılmayacak.

**Reveal:** “Yeni bilgi: yanıt kaybolabiliyor” seçimi apply’dan update’a ve tekrar apply’a dönüşü izletir. Aşağıdaki açılabilir ince şerit iki çalışma yüzeyini gösterir: terminal `openspec …`; AI sohbeti `/opsx:…`; Codex `$openspec-propose`.

**Anlatıcı:** “Explore isteğe bağlıdır. Update plan belgelerini değiştirir; kodu değiştirmez. Sync ayrı kullanılabilir; archive gerektiğinde senkronizasyon teklif eder. Bu bir zorunlu faz kapıları sistemi değildir.” Detaylı 12 komut tablosunu ana sahneye yığmayın.

### 14 — ““Bitti” için hangi kanıt?”

**Ana mesaj:** Dosyanın doğru biçimde olması, davranışın doğru çalıştığını kanıtlamaz.

**Kompozisyon:** Bir kabul senaryosundan başlayan üç bağlı kanıt katmanı: format kontrolü küçük terminal çıktısı; uygulama incelemesi küçük diff; en büyük parça scenario/test/sonuç tablosu. Satırlar: yanıt kaybolması / aynı anahtarla tekrar / uygulamaya geri dönüş / kesin ret. İlk durumda üçüncü satır “Çalıştırılmadı”. Sayfanın sağında “tamamlandı” mührü yok.

**Reveal:** “AI: tüm görevler tamamlandı” önce görünür. “Kanıtı aç” gerçek eksik satırı ortaya çıkarır. “Örnek tamamlanmış kayıt” ayrı seçenekte tamamen temsili ve eğitim simülasyonu etiketli test sonuçları gösterilebilir; bunlar gerçek test çalışması gibi sunulamaz.

**Anlatıcı:** “Validate biçimi; verify belge ile uygulama uyumunu inceler. Verify expanded profildedir ve arşivi engelleyen zorunlu kapı değildir. Ürün kabulünün dayanağı ilgili senaryoların gerçek kanıtlarıdır. Archive yayınlama değildir.”

### 15 — “İki repo. Bir ortak sözleşme.”

**Ana mesaj:** Ortak davranış bir yerde sahiplenilir; mobil ve backend kendi uygulama işlerini taşır.

**Kompozisyon:** Üstte domain planı, altta yan yana mobil ve backend repo kesitleri; üstten ikisine aynı requirement kimliği gider. Her repoda ayrı görev ve inceleme izi bulunur. Sağ kenarda mini sürüm matrisi: sözleşme revizyonu / mobil sürüm / backend sürüm / uyumluluk. “Tek sözleşme” otomatik senkronizasyonu ima etmez.

**Reveal:** “Stores beta yapısını gör” aynı topolojinin üst düğümünü ayrı Git plan reposuna dönüştürür. Ok etiketleri “davranış referansı”, “uygulama planı”; veri senkronizasyonu ya da deployment okları çizilmez.

**Anlatıcı:** “Stores planlamayı ayrı repo’da tutabilir. Git paylaşımı, kod erişimi ve sürüm eşleştirmesi ayrıca yönetilir. Store seçmek, ilgili tüm kod repolarının okunmuş olması demek değildir. Başlangıçta bütün şirket için dev taksonomi kurmayın.”

### 16 — “Artık siz yönetin”

**Ana mesaj:** Yetkinlik bir sonraki komutu ezberlemek değil, bir sonraki doğru kararı vermektir.

**Kompozisyon:** Açılıştaki aynı mobil/server sahnesi, bu kez arada incelenmiş küçük spec sayfası. Sağda üç iş: “Bir ürün kararı eksik”, “Bir senaryo eksik”, “Bir kanıt eksik”. Tıklanabilen satırlar. Her yanıt şeffaf bir çizgiyle ilgili belge veya kanıt noktasına bağlanır. Altta tek kopyalanabilir başlangıç istemi ve Atlas bağlantısı.

**Reveal:** Üç yanıt sırayla: geçerlilik politikasını domain sahibine sor; app yeniden açılınca toparlanma senaryosunu ekle; aynı anahtarla eşzamanlı tekrar testi sonucunu iste. Cevaplar örnek; katılımcının daha iyi gerekçeli alternatifleri kabul edilir.

**Anlatıcı:** “Kendi domain’inizde de aynı üç soruyu sorun: Neyi biliyoruz? Neye karar verdik? Neyle doğruladık?” Kapanışta yeni kavram açmayın. Başlangıç istemi: “Şu akışın mevcut davranışını bu mobil/backend kaynaklarından incele. Gözlemleri kaynaklarıyla, varsayımları ve açık ürün kararlarını ayrı yaz. Amacımız …; kapsam dışı … . Kararlar netleşince dar kapsamlı proposal ve senaryo taslağı oluştur.”

## 5. Detay atlası: aynı HTML içinde, ana akıştan ayrı

Atlas tam ekran modal veya ikinci görünüm olabilir; sunumun yerini/sahne adımını koruyarak geri dönmeli. Solda içerik dizini, sağda okunabilir belge. Arama filtresi faydalı, ağ gerektirmeyecek. Her bölümde “ne zaman açarım?”, somut örnek, kaynak bağlantısı olsun. 8 bölüm yeterli:

1. **Başlatma ve komut yüzeyleri:** Kurulum, init, araç seçimi; terminal/sohbet/Codex ayrımı. Core altılı ve expanded altılı kompakt tablo. `openspec update` ile `/opsx:update` aynı şey değildir. Core/expanded profili ve kurulu sürüm farkı.
2. **Dosya ve sorumluluk haritası:** Ana spec, change, metadata, proposal/spec/design/tasks; varsayılan schema ve özelleştirilebilirlik. PM/mühendislik/QA dağılımı öneri olarak etiketli.
3. **Gereksinim ve senaryo anatomisi:** Başlık seviyeleri; SHALL/MUST, SHOULD, MAY; iyi/kötü örnek; hata ve toparlanma kapsamı. Vakanın dört tam gereksinimi ayrı gösterilsin.
4. **Delta ve kapanış:** ADDED/MODIFIED/REMOVED, gerektiğinde RENAMED referansı; yeni capability Purpose; sync ile archive ayrımı; retirement gibi ileri durumu kaynak bağlantısıyla ver, ana akışı şişirme.
5. **Mevcut repo’dan bağlam:** İnceleme prompt’u, repo/sürüm kaydı, bulgu–varsayım–karar şablonu; canlı flag ve dış servis bilinmeyenleri; tüm eski PRD’yi topluca dönüştürme yerine ilgili dilimi kullanma.
6. **İnceleme ve kabul:** Proposal→spec→tasks kontrolü, kapsam sızıntısı, kaynak uydurma, test kanıtı, unrun/failed/passed ayrımı; validate/verify/insan kabulü sınırları.
7. **Ekip/domain/multi-repo:** `config.yaml` context ve artifact rules; özel schema’nın amacı; ortak sözleşme + component işleri; stores beta, repo erişimi, Git paylaşımı, root seçimi, çalışma bağlamı. CLI flag’leri gerekiyorsa yalnız güncel resmi kopyalar.
8. **Tam vaka ve kaynak sicili:** Temsili proposal, spec delta, design, tasks; karar logu; kapsam dışı; teknik açık sorular; resmi kaynaklara claim bazlı bağlantılar. Kontrol tarihi ve main dalı niteliği.

Atlas içeriği sunum notlarıyla aynı şey değil. Notlar anlatıcıya, atlas katılımcının iş başındaki sorusuna cevap verir. Genel “OpenSpec öğrenmeye devam” link listesi atlasın yerini tutmaz.

## 6. Sanat yönetimi: teknik dosya + editoryal anlatım

**Görsel karakter:** Bir ürün değişikliğinin adli incelemesi. Belgeler, bağlantılar, silinen/eklenen kurallar, kaybolan cevap, yeniden kurulan bilgi. “AI geleceği” render’ları, cam küreler, 3D bina, büyük gradient blob yok. Soyut teknoloji resmi kullanmayın. Her çizginin bir ilişkiyi taşıması gerekir.

**Renk:** Ana kâğıt `#F4F0E7`, metin `#142623`, koyu zemin `#102A27`. Değişiklik/karar vurgusu `#C9EF68` yalnız koyu yüzeyde veya koyu metinle; açık zeminde lime metin kullanılmaz. Belirsizlik `#B87923`; çelişki/silme `#A7443F`; teknik akış `#3F6F8D`. Bu renkler etiket ve çizgi biçimiyle desteklenecek, bilgi yalnız renge dayanmayacak.

**Tipografi:** Çevrimdışı sistem fontlarıyla sağlam sonuç: başlık `Georgia` veya mevcut gömülebilir editorial serif; gövde `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`; kod `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`. Bir güzel font bulmak uğruna ağ bağımlılığı kurmayın. Başlık 48–64 px; gövde 22–28 px; kanıt/kod 18–23 px; footnote 13–15 px @ 1440x900. Türkçe karakterler test edilmeli. Başlık en fazla iki satır, hedef tek satır.

**Grid:** 12 sütun, yüzde 6 dış marj. İçerik genişliği 1320 px civarında; 16:9 ve 16:10 ekranlarda merkezlenir ama `transform:scale()` ile okunamaz hâle getirilmez. Sahne başlığı sabit hizada; diyagramların geometri gereksinimi serbest.

**Ritim:** 01 koyu sahne; 02–07 açık inceleme yüzeyleri; 08 koyu sequence; 09–12 açık; 13 koyu döngü; 14–15 açık; 16 koyu dönüş. Her üç sahnede farklı görsel geometri: telefon, iz haritası, dosya, durum grafiği, diff, editör. Aynı 3 kart düzeni iki kez bile ana şablon olmasın.

**Hareket:** Gerekçeli 180–300 ms opacity/short translation; olay ilerlemesi anlatıcının kontrolünde. Yay/spring, parallax ve sürekli animasyon yok. Veri akışında çizginin vurgulanması yeterli. Reduced-motion durumunda geçiş anlık; tüm anlam korunur. Bir nesne taşınıyorsa anlamı da taşınmalı (delta’nın ana spec’e geçmesi gibi).

## 7. Tek HTML davranış sözleşmesi

- CSS, JS, diyagramlar, içerik ve varsa font tek dosyada. CDN, fetch, remote font, framework yükleme yok. Harici kaynak linkleri çevrimdışı sunumu bozmaz; tıklanınca tarayıcıya gider.
- Ana kullanım: ileri/geri ok, Space/PageDown, PageUp, Home/End. İleri önce mevcut sahnenin reveal adımlarını tamamlar, sonra sonraki sahneye geçer. Geri adım önce reveal’ı geri alabilir; davranış tutarlı ve yardımda yazılı olsun.
- Görünür geri/ileri düğmeleri; küçük sahne/adım sayacı; içindekiler. URL hash sahne numarasını koruyabilir. Atlas veya notlarda yazı yazarken kısayollar tetiklenmesin.
- `F` tam ekran, `N` notlar, `A` atlas, `?` yardım; `Esc` önce açık overlay’i kapatsın. Fullscreen API reddedilirse arayüz kırılmasın.
- Notlar gerçek metin: amaç, konuşma geçişi, örnek yanıtlar, resmi kaynak. Notlar sunum ekranını kaplayabilir ama yalnız isteğe bağlı görünür; hiçbir iddia yalnız notta düzeltilmesin.
- Focus-visible, semantik button, aria-label, klavyeyle diyagram alternatiflerini seçebilme. Modal focus yönetimi ve kapatınca eski öğeye dönüş. Kaynak linkleri erişilebilir isimli.
- Telefon genişliğinde tek kolon / dikey akış. Geniş diyagram okunamayacak kadar küçültülmez; küçük ekran için sıra düzeni veya içerik yatay kaydırma alanı. Ana gezinme her zaman erişilir.
- Print CSS: tüm sahneler tüm reveal içerikleriyle, notlar isteğe göre ayrı blok; interaktif kontroller gizli. PDF üretmek şart değil, basılabilir görünüm düşünülmeli.
- Kopyala eylemleri `file://` ortamında clipboard izni yoksa seçilebilir metin ve açık fallback sunsun. Ağ yokken konsol hatası yok.

## 8. Kalite kabul kriterleri

### İçerik

- 16 ana sahnenin her birinde tek öğretim işi ve somut bir vaka parçası var.
- Bütün örnek ürün kuralları, endpoint’ler ve kod parçaları temsili olarak tanımlı. Gerçek test sonucu veya repo incelemesi uydurulmuyor.
- “Sonuç bilinmiyor” istemcinin bilgi durumudur; backend iş durumu ile karıştırılmıyor.
- Kabul edilme ve uygulanma ayrıdır; sonradan gelen bilgiler buna uyuyor.
- Recovery POST yanıtından alınamayan kimliğe bağımlı değil; örnek tasarım bunun için baştan üretilen operationKey kullanıyor.
- Aynı requirement, proposal/spec/design/tasks/test örneklerinde birbiriyle çelişmiyor.
- Varsayılan yapı, önerilen ekip pratiği ve beta özellik birbirinden ayrılıyor.
- Sync zorunlu faz değil; archive sync teklif edebilir; update planı düzenler; verify expanded’dır ve zorunlu arşiv kapısı değildir.
- Katılımcı çıkış egzersizinde bir eksik karar, bir eksik senaryo ve bir eksik kanıtı açıklayabiliyor.

### Görsel

- En az 11 ana sahne anlam taşıyan diyagram, gerçek belge kesiti, durum geçişi, diff veya inceleme içeriyor.
- Her sahne 1440x900 ve 1280x720’de normal görüntüde okunuyor. Gövdede küçültmeyle sığdırma yok.
- Tam sahne ekran görüntülerinde taşma, çakışma, kırpılan başlık, aşırı boş alan ve mikroskobik kod yok.
- Vaka telefon ekranları birbiriyle aynı ürün hissini veriyor; metinler durum modeliyle tutarlı.
- Ana figür görsel alanın en az yarısını kullanıyor; metin figürün açıklaması, figür metnin süsü değil.
- Renk kontrastı ölçülüyor; yeşil/kehribar/kırmızı anlamları metinle destekleniyor.

### İşlev

- HTML doğrudan `file://` açılıyor; ağ kapalıyken tüm ana içerik, atlas, notlar, diagram reveal’ları çalışıyor.
- Klavye ile bütün sahneler ve atlas kullanılabiliyor; focus kaybolmuyor.
- Her reveal geri alınabiliyor veya sahne sıfırlanabiliyor; içindekilerden doğrudan giriş anlamlı başlangıç durumu açıyor.
- Tam ekran, escape, notlar, yardım, reduced-motion, küçük ekran, print kontrol ediliyor.
- Konsolda hata yok; tüm kaynak linkleri doğru URL’ye gidiyor; kaynakların erişilememesi sunumu kırmıyor.

## 9. Kaynak doğrulama sicili

Resmi `Fission-AI/OpenSpec` main belgeleri 9 Ekim 2026 tarihinde tarayıcı aracıyla okundu. Main hareketli hedef olduğu için sunuma “doküman kontrol tarihi” yazılmalı; paket sürümü doğrulanmadıkça sürüm numarası uydurulmamalı.

- [Getting Started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md): terminal–sohbet ayrımı, ilk akış, dosyalar, yapı doğrulaması.
- [Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md): core/expanded komutlar, Codex sözdizimi; update’ın yalnız plan belgelerine etkisi; sync’in isteğe bağlı olması; archive’ın senkronizasyon teklifi. Bu kaynak ayrıca mevcut update akışında yazmadan önce belge bazında teyit istendiğini söyler; atlas gerekirse bunu “güncel workflow davranışı” olarak aktarsın.
- [Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md): specs ve changes ayrımı, davranış sözleşmesi, schema ve varsayılan belge rolleri; esnek/iteratif yaklaşım.
- [Writing Good Specs](https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md): gözlemlenebilir requirement/scenario, normatif kelimeler, delta türleri, MODIFIED’ın tam yeni metni.
- [Reviewing a Change](https://github.com/Fission-AI/OpenSpec/blob/main/docs/reviewing-changes.md): plan inceleme sırası; scope, requirement ve task uyumu; verify’ın denetim niteliği ve expanded profili.
- [Existing Projects](https://github.com/Fission-AI/OpenSpec/blob/main/docs/existing-projects.md): tüm kod tabanını önceden belgelemek gerekmez; ilgili değişiklik diliminden başlama; eski dokümanlar kaynak malzemedir.
- [Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md): context, artifact rules, schema; operation guidance ayrı ve tavsiye niteliğindedir.
- [Stores User Guide — beta](https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md): ayrı plan reposu; ortak davranış ve component uygulama planları; code erişiminin ayrıca gerekmesi; Git paylaşımının kullanıcı/ekip işi olması. Store config ve varsayılan root çözümü gelişmekte, komutlar kopyalanacaksa belge tekrar kontrol edilmeli.

Bu planın durum makinesi, operationKey API tasarımı, karar kanıt sicili, önerilen rol dağılımı ve öğretim etkileşimleri özgün eğitim tasarımıdır. OpenSpec’in otomatik sağladığı özellikler gibi sunulamaz.
