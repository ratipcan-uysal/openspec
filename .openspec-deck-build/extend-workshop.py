from pathlib import Path
import html, json, zipfile, base64, re

root = Path('/Users/ratipcanuysal/Documents/ChatGPT/openspec')
out = root / 'output/openspec-pm'
path = out / 'openspec-pm.html'
original = path.read_text()
if 'id="workshop-start"' in original:
    raise SystemExit('Workshop already added; edit HTML directly.')

kit = {}
kit['openspec/config.example.yaml'] = '''# Örnek: değerleri doğrulayarak mevcut config ile birleştirin.
# Bu şablon gerçek bir repo incelemesi değildir.
schema: spec-driven
context: |
  Ürün: <ürün>. Domain: <domain>. Kullanıcı: <segment>.
  Planlama root'u: <bu repo>. Kod repo eşlemesi docs/context/README.md'de.
  Artifact dili Türkçe; Requirement/Scenario başlık biçimini koru.
  Her işte önce docs/context/README.md ve kaynak sicilini oku.
  Sonra yalnız ilgili akış, kural, API ve karar dosyalarını aç.
  Kaynak dosyaları erişilemezse içeriklerini okumuş gibi davranma.
  Koddan gözlenen davranış ile onaylanmış hedef davranışı ayır.
  Mobil/backend commit, yayınlanan app sürümü ve ortamı kaydet.
  Canlı flag, deploy veya dış servis görülmediyse bilinmiyor yaz.
  Çelişen kaynakları ve kararı verecek kişiyi görünür kıl.
rules:
  proposal:
    - Kullanıcı problemi, başarı sinyali ve kapsam dışını yaz.
    - Etkilenen repo/ekipleri ve açık ürün kararlarını belirt.
  specs:
    - Gereksinimleri gözlemlenebilir davranışla ifade et.
    - İlgili timeout, tekrar, ret ve toparlanma yollarını ele al.
    - Ürün kuralının kaynağını veya açık karar sahibini belirt.
  design:
    - Eski mobil istemci, API uyumu ve release sırasını değerlendir.
    - Teknik varsayımları ve çözülmemiş bağımlılıkları açık yaz.
  tasks:
    - Repo ve doğrulama sorumluluğunu açık belirt.
    - Kritik senaryoları doğrulama görevleriyle ilişkilendir.
'''
kit['docs/context/README.md'] = '''# Domain bağlamının giriş noktası

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
'''
kit['docs/context/sources.md'] = '''# Kaynak sicili

| ID | Bilgi | Kaynak: repo/dosya/sembol veya belge bölümü | Sürüm/commit | Ortam | İnceleyen/tarih | Durum | Sahip |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | <...> | <...> | <...> | <...> | <...> | Gözlendi / Kararlaştırıldı / Varsayım / Bilinmiyor | <...> |

## Kaynak çelişkileri
| Konu | Kaynak A ne diyor? | Kaynak B ne diyor? | Ürün/teknik karar sahibi | Sonuç |
| --- | --- | --- | --- | --- |
| <...> | <...> | <...> | <...> | Açık / <karar ve dayanak> |

Onaylı iş kuralı hedef davranışı; kod ve test incelenen sürümün davranışını
açıklar. Bunları tek doğru gibi birleştirmeyin. Test dosyasını okumak testin
çalıştırıldığı anlamına gelmez. İncelenen commit canlı deploy kanıtı değildir.
'''
kit['docs/context/domain.md'] = '''# Domain sözlüğü ve kararlar

## Sözlük
| Terim | Üründeki kesin anlamı | Karıştırılmaması gereken terim | Kaynak |
| --- | --- | --- | --- |
| <...> | <...> | <...> | S<...> |

## İş kuralları
| Kural ID | Koşul ve sonuç | Hedef/mevcut | Kaynak | Sahip | Geçerlilik |
| --- | --- | --- | --- | --- | --- |
| R01 | <...> | <...> | S<...> | <...> | <tarih/sürüm> |

## Açık kararlar
| Soru | Neden şimdi gerekli? | Seçenekler | Karar sahibi | Sonuç/dayanak |
| --- | --- | --- | --- | --- |
| <...> | <...> | <...> | <...> | Açık |

## Kabul edilmiş kararlar
| Karar | Gerekçe | Kaynak/onay | Etkilenen akış | Yeniden değerlendirme koşulu |
| --- | --- | --- | --- | --- |
| <...> | <...> | <...> | <...> | <...> |
'''
kit['docs/context/flow.md'] = '''# Tek akışın mevcut davranışı

- Akış ve kullanıcı amacı: <...>
- Mobil commit / app release: <...> / <bilinmiyorsa bilinmiyor>
- Backend commit / deploy: <...> / <bilinmiyorsa bilinmiyor>
- Ortam / flag değerleri / dış servis bilgisi: <...>

## Uçtan uca iz
| Adım | Kullanıcı/istemci | API/servis/domain | Veri/olay | Kanıt |
| --- | --- | --- | --- | --- |
| 1 | <giriş> | <...> | <...> | S<...> |
| 2 | <...> | <...> | <...> | S<...> |

## Kritik dallar
| Koşul | Gözlenen sonuç | Beklenen sonuç | Kaynak/açık karar | Doğrulama |
| --- | --- | --- | --- | --- |
| Başarı | <...> | <...> | <...> | <...> |
| Kesin ret | <...> | <...> | <...> | <...> |
| Yanıt kaybı / timeout | <...> | <...> | <...> | <...> |
| Tekrar / eşzamanlılık | <...> | <...> | <...> | <...> |
| Ekrana dönüş / eski istemci | <...> | <...> | <...> | <...> |

Uygulanmayan dalları gerekçesiyle belirtin. Gözlenmeyen sonucu uydurmayın.
'''
kit['prompts/01-context-audit.txt'] = '''$openspec-explore
Ürün/domain: <...>. İncelenecek tek akış: <...>.
Planlama root'u: <mutlak yol>.
Mobil checkout: <mutlak yol>, incelenecek branch/commit: <...>.
Backend checkout: <mutlak yol>, incelenecek branch/commit: <...>.
İş kuralı / API / tasarım / analitik kaynakları: <erişilebilir dosya veya bölüm>.

Önce erişebildiğin kökleri ve eksik kaynakları raporla.
docs/context/README.md ve sources.md varsa oku. Dizinleri keşfet; dosya adlarını
ve stack'i varsayma. Bir akışı ekran -> istemci isteği -> API -> handler ->
domain kuralı -> veri/olay -> ilgili test boyunca izle.
Her bulguya repo, commit, dosya/sembol veya belge bölümü ekle.
Gözlem, onaylı kural, varsayım, çelişki ve bilinmeyeni ayır.
Canlı deploy/app release/flag bilgisi yoksa prod davranışı iddia etme.
Kod değiştirme. Repo içeriğini çıkar; kalıcı dosya taslağını review için öner.
Çıktı: kaynak sicili, akış haritası, domain sözlüğü, iş kuralları,
açık kararlar/sahipleri, etki alanı ve okunamayan kaynaklar.
'''
kit['prompts/02-first-change.txt'] = '''$openspec-propose recover-package-change-result
Bu örnek işi kendi domain'indeki tek kullanıcı sonucuna uyarlayın.
Amaç: yanıt alınamadığında doğrulanmış sonucu güvenle göstermek.
Girdi: incelenmiş docs/context/ paketi ve kararlaştırılmış ürün kuralları.
Kapsam dışı: fiyat, uygunluk politikası, kampanya ve geçmiş talepler.
Önce kullanılan kaynakları ve açık kararları özetle. İşin sonucunu belirleyen
karar açıksa varsayarak tamamlamak yerine karar sahibine sor.
Kararlar netse proposal, delta specs, design ve tasks üret.
Kritik senaryoları, etkilenen repoları ve eski mobil istemci uyumunu belirt.
Dosyaları kaynaklarla ilişkilendir. Kod uygulamaya geçme; review için dur.
'''
kit['AGENTS.context-snippet.md'] = '''# Mevcut proje AGENTS.md dosyasına birleştirilecek örnek
# OpenSpec bu snippet'i otomatik oluşturmaz; mevcut talimatları koruyun.

## Domain bağlamını okuma
- Yeni işe başlarken docs/context/README.md ve sources.md oku.
- Yalnız ilgili akış, kural, sözleşme ve karar dosyalarını ekle.
- Her iddiayı incelenen kaynak sürümüyle ilişkilendir.
- Koddan gözlenen davranış ile onaylı ürün davranışını ayır.
- Çelişki veya eksik kararı sessizce çözme; sahibini belirt.
- Bir path'i görmek içeriğini okumak değildir; erişemediğini raporla.
- Planlama root'u ve etkilenen kod repo'larını açık belirt.
'''
kit['README.md'] = '''# OpenSpec PM başlangıç paketi

Bu paket kurulumu çalıştırmaz. Kendi ürününüz için doldurulacak eğitim
şablonlarını içerir. Gerçek mobil/backend repo'su incelenmedi.

1. Node >=20.19.0, npm ve shell erişimini doğrulayın.
2. Global CLI kurulumundan sonra openspec --version kontrol edin.
3. Ekipçe planlama root'unu seçin; orada openspec init --tools codex çalıştırın.
   Claude/Cursor kullananlar tool ID'lerini init --help ile doğrulasın.
4. Mobil/backend checkout'larını asistana erişilebilir yapın. Yerel yollar ve
   branch/commit'leri oturumda belirtin. Sadece repo URL'si erişim sağlamaz.
5. prompts/01-context-audit.txt ile tek akışın kaynaklı incelemesini başlatın.
6. docs/context şablonlarını bulgularla doldurun, domain/teknik sahiplerle review edin.
7. openspec/config.example.yaml içeriğini mevcut config'e birleştirin; gerçek
   config'i veya AGENTS.md'yi toptan ezmeyin. Örnek alanları doğrulayarak doldurun.
8. prompts/02-first-change.txt ile dar bir değişiklik üretin. PM ürün kararlarını,
   mühendislik design/tasks'i, QA senaryo kapsamını incelesin.
9. Uygulama aşamasında ilgili component root'undan openspec-apply-change skill'i
   kullanılır; test kanıtı, ürün kabulü, sync ve archive ayrıca kontrol edilir.

Bağlam dosyalarının adı/dizini ve review rolleri eğitim önerisidir. OpenSpec
resmi dosyası openspec/config.yaml'dır. context metni artifact yönergelerine
eklenir; yazılan path'in tüm içeriği otomatik yüklenmez. Rules tavsiye/yönergedir,
otomatik ürün onayı veya CI engeli değildir.

Resmi belgeler (9 Ekim 2026 main kontrolü; kurulu sürüm farklı olabilir):
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/existing-projects.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md
- https://learn.chatgpt.com/docs/build-skills

Komut biçimi Codex örneğidir. Üretilen skill isimleri ve init çıktısı esastır.
Güven: belgelenmiş araç davranışında yüksek; bağlam paketi tasarımında orta.
'''
for filename, content in kit.items():
    p = out / 'pm-starter-kit' / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
zip_path = out / 'pm-starter-kit.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for filename, content in kit.items():
        z.writestr('pm-starter-kit/' + filename, content)
zip_uri = 'data:application/zip;base64,' + base64.b64encode(zip_path.read_bytes()).decode()

cli = '''# macOS / Linux · terminal
node --version           # >= 20.19.0
npm --version
npm prefix -g            # mevcut hedefi gör

# Mevcut Node yöneticin varsa onun yolunu kullan:
npm install -g @fission-ai/openspec@latest
openspec --version'''
user_cli = '''# Alternatif: açıkça home altında npm kurulumu
npm install -g --prefix "$HOME/.local" @fission-ai/openspec@latest
export PATH="$HOME/.local/bin:$PATH"
command -v openspec
openspec --version'''
user_skills = '''# macOS / Linux · isteğe bağlı kişisel kurulum
mkdir -p "$HOME/.local/share/openspec-toolkit"
cd "$HOME/.local/share/openspec-toolkit"
openspec init --tools codex
mkdir -p "$HOME/.agents/skills"
for skill in "$HOME/.local/share/openspec-toolkit/.agents/skills"/openspec-*; do
  [ -d "$skill" ] || continue
  ln -s "$skill" "$HOME/.agents/skills/$(basename "$skill")"
done'''
workset = '''# BETA · önce kurulu sürümde --help kontrolü
openspec workset create package-change \\
  --member "$HOME/work/product-plans" \\
  --member "$HOME/work/mobile-app" \\
  --member "$HOME/work/backend" \\
  --tool codex
openspec workset open package-change'''
def esc(x): return html.escape(x)
def pre(id, content):
    return f'<pre id="{id}">{esc(content)}</pre><button type="button" class="small" data-copy-target="{id}">Kopyala</button>'
def scene(title, body, no, sub, source='', dark=False, steps=1):
    return f'''<section class="scene workshop" hidden data-title="{title}" data-steps="{steps}" {('data-theme="dark"' if dark else '')} {('data-source="'+source+'"' if source else '')} {('id="workshop-start"' if no==1 else '')}>
<div class="scene-head"><div class="eyebrow">Uygulama {no:02d} / 10 · bilgisayardan ilk işe</div><h1>{title}</h1><p class="sub">{sub}</p></div>{body}</section>'''

scenes = []
scenes.append(scene('Bir kere kur. Her ürüne ayrı bağlam ver.', '''
<div class="visual scope-stack">
<div class="scope-row"><span class="scope-num">01</span><div><h3>Kullanıcı hesabı</h3><p>CLI + kişisel araç tercihleri</p></div><code>npm global prefix<br>openspec config path</code><span class="scope-tag">Bir makine / kullanıcı</span></div>
<div class="scope-row" data-reveal="1"><span class="scope-num">02</span><div><h3>Asistanın çalışma yöntemi</h3><p>OpenSpec workflow skill’leri</p></div><code>&lt;repo&gt;/.agents/skills/<br>veya ~/.agents/skills/</code><span class="scope-tag">Codex örneği</span></div>
<div class="scope-row" data-reveal="2"><span class="scope-num">03</span><div><h3>Ürün / domain</h3><p>Kurallar + kaynaklar + değişiklikler</p></div><code>&lt;root&gt;/openspec/config.yaml<br>docs/context/ + specs/</code><span class="scope-tag">Ekipçe sürümlenir</span></div>
</div><div class="caption"><span>Öneri: ortak yöntem kullanıcıya; domain bilgisi ilgili projenin sürümlenen bağlamına.</span><button class="small" data-open-atlas="8">Kurulum rehberi ↗</button></div>''',1,'CLI kurulumu, skill kapsamı ve ürün hafızası üç ayrı katmandır.','installation.md',True,2))
scenes.append(scene('CLI gerçekten user altında nasıl kurulur?', f'''
<div class="visual workshop-two"><div class="terminal"><div class="terminal-label">01 / Mevcut Node düzeni</div>{pre('install-standard',cli)}</div><div class="paper"><div class="file">02 / Açıkça home hedefi</div>{pre('install-home',user_cli)}<p class="annotation">Bu export yalnız mevcut shell’e etki eder. Kalıcılık için PATH satırını kullandığınız shell’in başlangıç dosyasına ekleyin.</p></div></div>
<div class="caption"><span><code>-g</code> hedefi prefix belirler. nvm/fnm kullanıyorsanız CLI aktif Node sürümüne bağlıdır.</span><button class="small" data-open-atlas="8">PATH · Windows · hata çözümü ↗</button></div>''',2,'Önce runtime ve hedefi kontrol et. Kurulumun çalıştığını sürüm çıktısıyla doğrula.','installation.md',steps=0))
scenes.append(scene('“Her projemde skill görünsün” diyorsan…', '''
<div class="visual workshop-two"><div><div class="folder-map"><span class="micro">NORMAL PROJE KURULUMU</span><code>product-repo/<br> ├─ .agents/skills/openspec-*/<br> └─ openspec/</code><p>Repo’da <code>openspec init --tools codex</code>. Ekibin yöntemi repo ile taşınır.</p></div><div class="folder-map" data-reveal="1"><span class="micro">İSTEĞE BAĞLI USER KAPSAMI</span><code>~/.agents/skills/openspec-*/<br>        ↳ kişisel toolkit’ten symlink</code><p>Skill bütün projelerde keşfedilir. Ürün bağlamı hâlâ ilgili root’tadır.</p></div></div><div class="paper"><div class="file">Kişisel toolkit · ayrı ve güncellenebilir</div><pre>~/.local/share/openspec-toolkit/<br>  .agents/skills/openspec-*/SKILL.md<br><br># Sonra bu toolkit içinde:<br>openspec update</pre><p class="annotation">Bu, Codex’in user skill desteğinden yararlanan önerilen manuel düzenlemedir. OpenSpec’in <code>init --global</code> komutu değildir.</p><button class="small" data-open-atlas="9">Tam symlink komutları ↗</button></div></div>
<div class="caption"><span>Aynı isimli user ve repo skill’leri birleşmez; ikisi seçicide görünebilir. Bir bakım yolu seçin.</span><span class="micro">Codex user: ~/.agents/skills</span></div>''',3,'Varsayılan yol proje kurulumu. Kullanıcı genelinde dağıtım ayrıca yönetilir.','supported-tools.md'))
scenes.append(scene('Mobil + backend: komut nerede çalışacak?', '''
<div class="visual root-choices"><div class="root-choice"><span class="micro">A / TEK REPO</span><h3>Repo root’u</h3><pre>product/<br>  mobile/<br>  backend/<br>  openspec/</pre><p>Bir monorepo; ortak root ve ilgili domain spec’leri.</p></div><div class="root-choice selected"><span class="micro">B / İLK ÇOKLU REPO PİLOTU</span><h3>Planlama root’u</h3><pre>work/<br>  product-plans/ ← PM burada<br>  mobile-app/<br>  backend/</pre><p>Plan burada; iki kod checkout’u asistana ayrıca erişilebilir.</p></div><div class="root-choice"><span class="micro">C / EKİP ÖLÇEĞİ · BETA</span><h3>Store + component</h3><pre>team-plans/ ← ortak spec<br>mobile/     ← yerel change<br>backend/    ← yerel change</pre><p>Ortak sözleşme referanslanır. Component uygulaması kendi root’unda.</p></div></div>
<div class="caption"><span>Terminal: seçilen root’ta <code>openspec init --tools codex</code>. Sohbet: root + kod yolları + erişim kapsamını açık belirt.</span><button class="small" data-open-atlas="10">Çoklu repo reçetesi ↗</button></div>''',4,'Repo URL’si, yerel dosya erişimi ve OpenSpec root’u birbirinden farklıdır.','existing-projects.md',steps=0))
scenes.append(scene('En güçlü bağlam: küçük giriş, derin kanıt.', '''
<div class="visual context-layers"><div class="context-layer"><span>01</span><h3>İşin niyeti</h3><p>Kullanıcı · sorun · beklenen sonuç · kapsam dışı</p><small>Her işe özel</small></div><div class="context-layer" data-reveal="1"><span>02</span><h3>Domain paketi</h3><p>Sözlük · kurallar · akış · API · karar sahipleri</p><small>Sürümlenen ortak bilgi</small></div><div class="context-layer" data-reveal="1"><span>03</span><h3>İlgili kaynak dilimi</h3><p>Mobil ekran → API → handler → domain → veri → test</p><small>Repo + commit + sembol</small></div><div class="context-layer" data-reveal="2"><span>04</span><h3>Çalışma gerçekliği</h3><p>App release · deploy · ortam · flag · dış servis</p><small>Doğrulanmış veya bilinmiyor</small></div><div class="context-layer" data-reveal="2"><span>05</span><h3>Değişiklik ve kabul</h3><p>İlgili spec · delta · kritik senaryolar · ölçüm</p><small>Bu işin referansı</small></div></div>
<div class="caption"><span>Güç = ilgililik + kaynak + sürüm + açık karar. Bütün repo’yu sohbet içine yapıştırmak bu dört şeyi sağlamaz.</span><button class="small" data-open-atlas="11">Bağlam paketi ↗</button></div>''',5,'AI’a okuma rotası ver; ilgili dosyaları gerçekten okuduğunu kaynaklarla göstermesini iste.','customization.md',True,2))
scenes.append(scene('Repo’dan bağlam çıkar. Kararı uydurma.', '''
<div class="visual workshop-two"><div class="scan-route"><div><b>1</b><span>Kökleri keşfet<small>README, dizinler, sözleşmeler; stack’i varsayma.</small></span></div><div><b>2</b><span>Tek akışı izle<small>Ekrandan veriye, iki repo boyunca.</small></span></div><div><b>3</b><span>Kanıtı kaydet<small>Repo, commit, dosya/sembol, gözlenen davranış.</small></span></div><div><b>4</b><span>Çelişki ve kararı ayır<small>Onaylı kural ≠ bug ≠ hedef davranış.</small></span></div></div><div class="evidence-ledger"><div class="evidence-heading">ÇIKTI / KAYNAK SICİLİ</div><div><span class="evidence-dot seen"></span><strong>Gözlendi</strong><p>İncelenen mobil sürüm genel hata gösteriyor.</p></div><div><span class="evidence-dot decision"></span><strong>Kararlaştırıldı</strong><p>PM + domain sahibi belirsiz sonucu ayrı gösterme kararını aldı.</p></div><div><span class="evidence-dot unknown"></span><strong>Bilinmiyor</strong><p>Canlı flag değeri ve eski istemcinin davranışı henüz doğrulanmadı.</p></div></div></div>
<div class="caption"><span>Kodu okumak canlı davranışı, test dosyasını okumak da geçen testi kanıtlamaz.</span><button class="small" data-open-atlas="12">Repo tarama prompt’u ↗</button></div>''',6,'Üç bilgi türünü aynı cümlede kesin gerçek gibi birleştirmeyin.','existing-projects.md',steps=0))
scenes.append(scene('Bağlam sohbetten sonra da yaşamalı.', '''
<div class="visual workshop-two"><div class="paper"><div class="file">openspec/config.yaml · kısa ortak yönlendirme</div><pre>schema: spec-driven<br>context: |<br>  Ürün ve domain: ...<br>  Önce docs/context/README.md oku.<br>  İlgili kaynakları sürümleriyle belirt.<br>  Çelişkiyi ve açık kararı görünür kıl.<br>rules:<br>  specs:<br>    - Kritik hata/toparlanma yollarını yaz.<br>  design:<br>    - Eski mobil istemci uyumunu değerlendir.</pre></div><div class="file-index"><div><code>docs/context/README.md</code><span>Ürün sınırı + repo haritası + okuma rotası</span></div><div><code>sources.md</code><span>Kaynak + sürüm + ortam + güncellik</span></div><div><code>domain.md</code><span>Terimler + kurallar + karar sahipleri</span></div><div><code>flow.md</code><span>Tek akış + kritik dallar + kanıt</span></div><p class="annotation">Bu docs/context/ düzeni eğitim önerisidir. Dolu örnek şablonlar başlangıç paketinde.</p></div></div>
<div class="caption"><span><code>context</code> yönergeye eklenir. Bir path yazmak dosyanın tamamını otomatik yüklemez; okuma adımını açık belirtin.</span><button class="small" data-open-atlas="11">Tam config + şablonlar ↗</button></div>''',7,'Context ortak arka planı; rules ilgili belgeyi yönlendirir. İnceleme ve güncelleme sahibi atayın.','customization.md',steps=0))
scenes.append(scene('Kendi domain’inle ilk incelemeyi başlat.', '''
<div class="visual prompt-workbench"><form id="contextForm" class="context-form"><label>Ürün / domain<input name="product" value="Mobil paket yönetimi" required></label><label>İncelenecek tek akış<input name="flow" value="Paket değişikliği sonrası yanıt kaybı" required></label><label>Mobil checkout yolu<input name="mobile" value="/path/to/mobile-app" required></label><label>Backend checkout yolu<input name="backend" value="/path/to/backend" required></label><label>Planlama root’u<input name="planning" value="/path/to/product-plans" required></label><label>Kapsam dışı<input name="outside" value="Fiyat, kampanya, uygunluk politikasını değiştirmek" required></label></form><div class="terminal generated"><div class="terminal-label">CODEX SOHBETİ · İNCELEME</div><pre id="generatedContext"></pre><button class="small" data-copy-target="generatedContext">Prompt’u kopyala</button></div></div>
<div class="caption"><span>Yolları gerçek checkout’larla değiştir. Asistan önce erişimi doğrulasın; sonra kaynaklı akış haritasını çıkarsın.</span><button class="small" data-open-atlas="12">Daha ayrıntılı iki prompt ↗</button></div>''',8,'Alanları değiştir; mesaj anında domain’ine uyarlansın. Bu adım ürün kuralı icat etmez.','explore.md',steps=0))
scenes.append(scene('İlk iş: araştır → karar → plan → kanıt.', '''
<div class="visual first-work"><div class="work-step"><span class="micro">01 / AI + PM</span><code>$openspec-explore</code><h3>Kaynaklı mevcut durum</h3><p>Akış, kurallar, çelişkiler ve açık karar sahipleri.</p></div><div class="work-step"><span class="micro">02 / PM + DOMAIN SAHİBİ</span><code>Ürün kararlarını netleştir</code><h3>Hedef ve sınır</h3><p>Bir kullanıcı sonucu; başarı sinyali ve kapsam dışı.</p></div><div class="work-step"><span class="micro">03 / AI + EKİP REVIEW</span><code>$openspec-propose &lt;iş&gt;</code><h3>Dört belgeyi incele</h3><p>Proposal, delta specs, design, tasks. Aynı niyet mi?</p></div><div class="work-step" data-reveal="1"><span class="micro">04 / İLGİLİ COMPONENT</span><code>$openspec-apply-change &lt;iş&gt;</code><h3>Uygula ve doğrula</h3><p>Gerçek test sonucu, ürün kabulü, sync ve archive.</p></div></div>
<div class="gate-note">Review için durma kuralı ekibin çalışma anlaşmasıdır; OpenSpec otomatik PM onay kapısı oluşturmaz.</div>
<div class="caption"><span>Plan değişince <code>$openspec-update-change</code>; kodu etkiliyorsa yeniden apply. Her çağrıda doğru root’u kontrol et.</span><button class="small" data-open-atlas="12">Tam günlük çalışma reçetesi ↗</button></div>''',9,'PM’in işi yalnız komut çalıştırmak değil; kaynak, karar ve kabulün tutarlılığını yönetmek.','commands.md'))
scenes.append(scene('PM yarın bu işi tek başına başlatabilir mi?', f'''
<div class="visual workshop-two"><div class="readiness-list"><label><input type="checkbox"><span>CLI sürümü doğrulandı<small>Doğru executable ve Node sürümü.</small></span></label><label><input type="checkbox"><span>Root ve skill görülebiliyor<small>Komutun yazacağı yer net.</small></span></label><label><input type="checkbox"><span>Mobil + backend erişimi kanıtlandı<small>İlgili checkout/commit ve kaynaklar.</small></span></label><label><input type="checkbox"><span>Bağlam ve açık karar sahipleri hazır<small>Gözlem ile ürün kararı ayrıldı.</small></span></label><label><input type="checkbox"><span>Tek iş ve kabul senaryoları net<small>Review ve gerçek doğrulama sahibi belli.</small></span></label><p id="readinessStatus" aria-live="polite">0 / 5 hazırlık noktası tamamlandı.</p></div><div class="field-guide"><span class="micro">İŞ BAŞINDA BAŞVURU</span><h2>Takılınca doğru yere bak.</h2><div><strong>Komut bulunamadı</strong><span>PATH / prefix / aktif Node sürümü</span></div><div><strong>Skill görünmüyor</strong><span>Doğru tool, generated dosya, yeniden yükleme</span></div><div><strong>AI genel cevap veriyor</strong><span>Gerçek dosya okuma + kaynak kanıtı</span></div><div><strong>Yanlış proje planı</strong><span>CWD / root / store / global default</span></div><div class="inline-controls"><button class="small" data-open-atlas="13">Sorun giderme ↗</button><a class="action download-kit" href="{zip_uri}" download="openspec-pm-starter-kit.zip">Başlangıç paketini indir ↓</a></div></div></div>
<div class="caption"><span>Her PM’e: ortak yöntem + kendi domain paketi + gerçek ilk iş + karar verecek insanlar.</span><span class="micro">Araç bilgisi: yüksek güven<br>Bağlam düzeni: ekip önerisi</span></div>''',10,'Bu kontrol hazırlık içindir; CLI kurulumu veya ürün kabulü otomatik yapılmaz.','troubleshooting.md',True,0))

css = '''
/* Practical workshop */
.tools #workshopBtn{background:var(--lime);color:var(--deep);font-weight:650}.progress button{width:15px}.workshop-two{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}.workshop .visual{min-height:320px}.scope-row{display:grid;grid-template-columns:60px 1.15fr 1.35fr 160px;gap:22px;align-items:center;padding:24px 0;border-top:1px solid var(--line)}.scope-num{font:35px Georgia,serif;color:var(--lime)}.scope-row h3{font:26px Georgia,serif;margin-bottom:6px}.scope-row p{font-size:16px;margin:0;color:var(--muted)}.scope-row code{font-size:15px;line-height:1.65}.scope-tag{font-size:12px;color:var(--muted);text-align:right}.terminal{background:#152d29;color:#f4f0e7;padding:24px 26px;border:1px solid #446258;min-width:0}.terminal-label{font:11px var(--mono);letter-spacing:.09em;color:#bbcbc1;margin-bottom:20px}.terminal pre{font-size:14px;line-height:1.8}.terminal .small{margin-top:15px}.workshop .paper pre{font-size:14px;line-height:1.75}.workshop .paper>button{margin-top:15px}.folder-map{border-top:1px solid var(--line);padding:17px 0}.folder-map code{display:block;font-size:17px;line-height:1.6;margin:10px 0}.folder-map p{font-size:16px;margin:0}.root-choices{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}.root-choice{border-top:1px solid var(--line);padding-top:20px}.root-choice.selected{border-top:4px solid var(--blue);padding-top:17px}.root-choice h3{font:28px Georgia,serif;margin:14px 0}.root-choice pre{font-size:17px;line-height:1.8}.root-choice p{font-size:16px;color:var(--muted);margin-top:22px}.context-layer{display:grid;grid-template-columns:45px 225px 1fr 180px;align-items:center;gap:20px;padding:18px 0;border-top:1px solid var(--line)}.context-layer>span{font:12px var(--mono);color:var(--lime)}.context-layer h3{font:23px Georgia,serif;margin:0}.context-layer p{margin:0;font-size:16px}.context-layer small{font-size:12px;color:var(--muted);text-align:right}.scan-route>div{display:flex;gap:22px;align-items:start;padding:18px 0;border-top:1px solid var(--line)}.scan-route b{font:27px Georgia,serif;color:var(--blue);min-width:24px}.scan-route span{font-size:23px}.scan-route small{display:block;font-size:14px;color:var(--muted);margin-top:8px}.evidence-ledger{border:1px solid var(--line);padding:24px 26px}.evidence-heading{font:11px var(--mono);letter-spacing:.1em;color:var(--muted);margin-bottom:12px}.evidence-ledger>div:not(:first-child){position:relative;border-top:1px solid var(--line);padding:18px 0 10px 24px}.evidence-ledger p{font-size:15px;color:var(--muted);margin:7px 0 0}.evidence-dot{position:absolute;left:0;top:23px;width:9px;height:9px;border-radius:50%}.evidence-dot.seen{background:var(--blue)}.evidence-dot.decision{background:#54713c}.evidence-dot.unknown{background:var(--amber)}.file-index>div{padding:17px 0;border-top:1px solid var(--line)}.file-index code{display:block;color:var(--blue);font-size:15px;margin-bottom:9px}.file-index span{font-size:16px}.prompt-workbench{display:grid;grid-template-columns:340px 1fr;gap:35px;align-items:start}.context-form{display:grid;grid-template-columns:1fr 1fr;gap:13px 16px}.context-form label{font-size:11px;color:var(--muted);line-height:1.4}.context-form label:nth-child(n+3){grid-column:1/3}.context-form input{display:block;width:100%;padding:10px 9px;margin-top:6px;border:1px solid var(--line);color:var(--ink);background:var(--white);font-size:12px;border-radius:2px}.generated pre{font-size:13px;line-height:1.65}.first-work{display:grid;grid-template-columns:repeat(4,1fr);gap:26px}.work-step{border-top:2px solid var(--line);padding-top:20px}.work-step code{display:block;color:var(--blue);font-size:12px;overflow-wrap:anywhere;line-height:1.6;margin:16px 0}.work-step h3{font:25px Georgia,serif}.work-step p{font-size:16px;color:var(--muted)}.gate-note{padding:13px 18px;border-left:3px solid var(--amber);background:#ede4d4;font-size:13px;margin-top:5px}.readiness-list label{display:flex;align-items:start;gap:15px;border-top:1px solid var(--line);padding:13px 0;font-size:18px;cursor:pointer}.readiness-list input{accent-color:#c9ef68;width:18px;height:18px;margin-top:4px}.readiness-list small{display:block;color:var(--muted);font-size:12px;line-height:1.5;margin-top:5px}.readiness-list>p{font:13px var(--mono);color:var(--lime);margin-top:14px}.field-guide h2{font-size:32px;margin:12px 0 15px}.field-guide>div:not(.inline-controls){border-top:1px solid var(--line);padding:12px 0;display:flex;flex-direction:column;gap:5px;font-size:15px}.field-guide>div span{font-size:13px;color:var(--muted)}.download-kit{text-decoration:none;display:inline-block;font-size:13px}.atlas-content .copy-row{margin-top:12px}.atlas-content .warning-note{border-left:3px solid var(--amber);padding:12px 16px;background:#ece3d4;font-size:14px}.atlas-content code{overflow-wrap:anywhere}.workshop-return{margin-bottom:15px}.atlas-content pre{max-height:none}
@media(min-width:761px) and (max-height:800px){.workshop .visual{min-height:280px}.scope-row{padding:18px 0}.scope-row h3{font-size:23px}.scope-row code{font-size:13px}.scope-row p{font-size:14px}.terminal{padding:18px 20px}.terminal-label{margin-bottom:12px}.terminal pre{font-size:12px;line-height:1.65}.workshop .paper pre{font-size:12px;line-height:1.6}.workshop .paper .annotation{font-size:12px}.context-layer{padding:14px 0;grid-template-columns:35px 190px 1fr 150px}.context-layer h3{font-size:21px}.context-layer p{font-size:14px}.folder-map{padding:12px 0}.folder-map code{font-size:15px}.folder-map p{font-size:14px}.root-choice pre{font-size:15px}.root-choice p{font-size:14px}.scan-route>div{padding:14px 0}.scan-route span{font-size:21px}.scan-route small{font-size:12px}.evidence-ledger{padding:18px 20px}.evidence-ledger>div:not(:first-child){padding-top:14px}.evidence-dot{top:20px}.evidence-ledger p{font-size:13px}.file-index>div{padding:13px 0}.file-index span{font-size:14px}.generated pre{font-size:11px;line-height:1.6}.context-form{gap:10px}.context-form input{padding:8px;font-size:11px}.first-work{gap:20px}.work-step{padding-top:16px}.work-step h3{font-size:23px}.work-step p{font-size:14px}.gate-note{padding:10px 15px;font-size:12px}.readiness-list label{padding:11px 0;font-size:16px}.field-guide h2{font-size:28px}.field-guide>div:not(.inline-controls){padding:10px 0;font-size:14px}.field-guide .inline-controls{margin-top:12px}.readiness-list>p{margin-top:10px}.progress button{width:11px}}
@media(max-width:1100px){.brand span{display:none}.scope-row{grid-template-columns:42px 1fr 1.3fr}.scope-tag{display:none}.context-layer{grid-template-columns:30px 180px 1fr}.context-layer small{display:none}.prompt-workbench{grid-template-columns:290px 1fr}.first-work{gap:18px}.work-step code{font-size:11px}.progress{gap:3px}.workshop-two{gap:26px}}
@media(max-width:760px){.tools #workshopBtn{font-size:11px;padding:9px 7px}.tools #notesBtn{display:none}.workshop-two,.root-choices,.prompt-workbench,.first-work{grid-template-columns:1fr;gap:24px}.workshop .visual{min-height:0}.scope-row{grid-template-columns:32px 1fr;gap:14px;padding:20px 0}.scope-row h3{font-size:24px}.scope-row code{grid-column:2;font-size:13px}.scope-num{font-size:24px}.scope-row p{font-size:14px}.context-layer{grid-template-columns:25px 1fr;gap:10px;padding:18px 0}.context-layer h3{font-size:23px}.context-layer p{grid-column:2;font-size:14px}.terminal{padding:20px 18px}.terminal pre,.workshop .paper pre{font-size:12px}.root-choice p{margin-top:12px}.root-choice pre{font-size:15px}.generated pre{font-size:12px}.context-form{grid-template-columns:1fr;gap:12px}.context-form label,.context-form label:nth-child(n+3){grid-column:auto}.context-form input{font-size:14px;padding:11px}.readiness-list label{font-size:17px}.readiness-list>p{font-size:12px}.field-guide .inline-controls{align-items:stretch}.download-kit{text-align:center}.gate-note{margin-top:22px}.brand{font-size:17px}.tools{gap:0}.tools button{font-size:11px;padding:9px 5px}#fullBtn{display:none}}
@media print{.workshop-two{gap:25px}.scope-row{color:#142623;padding:17px 0}.scope-num,.scope-row p,.context-layer span,.context-layer p,.context-layer h3,.readiness-list small,.field-guide span,.readiness-list>p{color:#142623!important}.terminal{background:#fff;color:#142623;border-color:#c4cbc0}.terminal-label{color:#52645e}.workshop .small,.download-kit{display:none!important}.workshop .visual{min-height:0}.prompt-workbench{grid-template-columns:290px 1fr}.context-layer{padding:14px 0}.readiness-list input{accent-color:#142623}.field-guide>div{color:#142623}.scope-row code{color:#142623}.context-form input{color:#142623;background:white}.progress{display:none}}
'''
original = original.replace('</style>', css + '\n</style>', 1)
original = original.replace('<button type="button" id="tocBtn">', '<button type="button" id="workshopBtn">Kurulum atölyesi</button><button type="button" id="tocBtn">', 1)
original = original.replace('</main>', '\n' + '\n\n'.join(scenes) + '\n</main>', 1)
original = original.replace('16 sahne · yaklaşık 30 dakika · her sahneye doğrudan geçebilirsiniz.', '16 anlatım sahnesi + 10 uygulama sahnesi. Kısa eğitim için ana anlatım; kendi bilgisayarında başlamak için kurulum atölyesi.')
original = original.replace('01 / 16 · adım 0 / 2', '01 / 26 · adım 0 / 2')
original = original.replace('16 / Kapanış', '16 / Ana anlatımın kapanışı')

notes = [
['Kurulum kapsamlarını ayırın','Global CLI domain bilgisi taşımaz. Asistan skill’i iş yöntemini taşır. Ürün bağlamı ilgili root’un config ve sürümlenen kaynaklarında tutulur. USER skill kullanmak ürün specs klasörünü home altında ortaklaştırmayı gerektirmez.','Önce CLI’ın nereye kurulduğunu görelim.'],
['Home kurulumunu somut gösterin','Mevcut Node yöneticisi varsa onu koruyan standart global kurulumu tercih edin. Home prefix alternatifinde sadece bu kurulumun hedefi açıkça belirlenir. PATH export mevcut terminal içindir; yeni terminal veya GUI uygulaması için kullandığınız shell ve başlatma ortamına uygun kalıcı PATH gerekir. Gerçek init veya kurulum bu HTML tarafından çalıştırılmaz.','CLI ve skill aynı şey değildir.'],
['Kişisel skill yolunu öğretin','OpenSpec Codex init proje .agents/skills dizinine üretir. Codex USER discovery ~/.agents/skills dizinidir ve symlink destekler. Kişisel toolkit üretimi + symlink bu iki belgelenmiş davranıştan kurulmuş manuel bir öneridir. ln -s hedefi ezmez. Aynı isimler birleştirilmez; global ve local kurulum birlikte bakımsız çoğaltılmamalıdır.','Ürünün planını hangi root’ta tutacağız?'],
['Root kararını ekipçe netleştirin','Monorepo tek root basittir. Ayrı mobil/backend için planlama repo’su PM işi için ortak bir root olabilir; asistan kod dosyalarını ayrıca okuyabilmelidir. Store ve workset beta’dır. Component uygulaması ayrı yerel change/reference ile sınırlandırılabilir. Store pointer görevleri repolara otomatik dağıtmaz.','Root seçildi. Şimdi hangi bağlam okunmalı?'],
['Bağlamın beş katmanını öğretin','Bu model eğitim önerisidir. Niyet, domain paketi, ilgili kaynaklar, runtime gerçekliği ve change bilgisi birlikte çalışır. Tokene sığan her şeyi dökmek yerine rotayı verin, önemli dosyaları gerçekten okutun ve iddiaları kaynaklara bağlayın.','Kaynaklı çıkarımı nasıl alacağız?'],
['Gözlemi ürün kararından ayırın','Tarama sırası stack ve dosya adı varsaymadan başlar. Testin okunması çalıştırılması değildir. Mobil/backend commit canlı deployment kanıtı değildir. Kaynak çelişkisi görünür kalmalı; domain sahibi beklenen davranışı netleştirmelidir.','Çıkarılan bilgiyi konuşmada kaybetmeyelim.'],
['Kalıcı giriş dosyasını gösterin','OpenSpec context arka planı her artifact yönergesine ekler; rules ilgili artifact içindir. docs/context dosya adları resmi ürün gereksinimi değildir. Config’e dosya yolunu koymak içeriğin otomatik yüklenmesi değildir; loader protokolü ve okuma kanıtı gerekir. Generated OpenSpec skill’lerini özelleştirerek domain bilgisi koymayın; update bunları yeniler.','Katılımcı kendi domain’inin yollarını girsin.'],
['Prompt’u katılımcının işiyle uyarlayın','Formdaki yollar temsili. Gerçek checkout, branch/commit, ürün amacı ve erişilebilir iş kuralları verilmelidir. Erişim raporu ilk adımdır; okunamayan belge görülmüş gibi sayılmaz. Bu oturum yalnız keşif talep eder.','Araştırmadan sonra karar ve proposal gelir.'],
['İlk değişiklikte insan kararını görünür kılın','PM hedef/scope kararına, engineering teknik tasarıma, QA senaryo kapsamına katkı verir. Bunlar ekip önerisidir. Apply’i ilgili implementation root’unda yürütün. Update plan değişimidir; code adaptasyonu ayrıca apply gerektirir. Sync/archive deployment değildir.','Hazırlığı beş noktada kontrol edelim.'],
['Bağımsız başlangıcı ölçün','Checkbox eğitimde hatırlatma içindir; kurulumun ya da repo erişiminin otomatik tespiti değildir. Başlangıç paketi örnek config, context dosyaları, AGENTS snippet ve iki prompt içerir. Şablonları mevcut repo içeriğine review ederek birleştirin.','İlk gerçek dar işi seçin; eksikleri ilgili sahiplerle tamamlayın.']
]
original = original.replace("const sourceLink=", 'notes.push(...' + json.dumps(notes, ensure_ascii=False) + ');\nconst sourceLink=', 1)
original = original.replace('const atlas=[', 'const kit=' + json.dumps(kit, ensure_ascii=False) + ';\nconst escapeHtml=s=>String(s).replace(/[&<>"\']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","\\\'":"&#39;"}[c]||c));\nconst kitBlock=(id,key)=>`<pre id="${id}">${escapeHtml(kit[key])}</pre><button class="small" data-copy-target="${id}">Kopyala</button>`;\nconst externalSrc=(url,title)=>`<a href="${url}" target="_blank" rel="noopener">${title}</a>`;\nconst atlas=[', 1)

atlas = [
{'title':'User CLI kurulumu ve PATH','tags':'user kullanıcı home global kurulum npm prefix node path mac windows linux codex','body':f'''<h2>Kullanıcı hesabında CLI kurulumu</h2><p class="when">Kurulum atölyesi / 02. Komutlar çalıştırılacak talimattır; HTML kurulum yapmaz.</p><h3>1. Runtime ve mevcut hedef</h3>{pre('atlas-install',cli)}<p>Node 20.19.0 ve üzeri gerekir. Önce mevcut Node/npm yöneticisini öğrenin. nvm/fnm kurulumunda CLI aktif Node sürümüne bağlı olabilir. Kurulu sürümü takımın kullandığı sürümle eşleştirin; main belgeleri daha yeni olabilir.</p><h3>2. Özellikle home altında istiyorsan</h3>{pre('atlas-home',user_cli)}<p>macOS/Linux örneği. <code>--prefix</code> bu npm komutunun hedefini seçer; bütün npm ayarlarını değiştirmez. PATH’i kalıcı yapmak için aşağıdaki satırı kullandığınız shell’in uygun başlangıç dosyasına ekleyin; yeni terminal açarak doğrulayın.</p><pre>export PATH="$HOME/.local/bin:$PATH"</pre><p>zsh kullanan macOS terminalinde <code>~/.zshrc</code> yaygın yoldur. GUI’dan başlatılan asistanın aynı PATH’i görmesi ayrıca kontrol edilmelidir. Bir sürüm yöneticiniz varsa onun PATH düzenini kullanın.</p><h3>3. Windows</h3><pre>node --version\nnpm --version\nnpm prefix -g\nnpm install -g @fission-ai/openspec@latest\nopenspec --version</pre><p>Windows’ta global executable prefix dizininin doğrudan içindedir; Unix gibi <code>bin/</code> eklemeyin. Gösterilen dizinin kullanıcı PATH’inde olmasını kontrol edin ve terminali yeniden açın. Unix HOME/symlink komutlarını PowerShell’e aynen taşımayın.</p><h3>4. Her proje için kurulum</h3><pre>cd /gercek/planlama-root\nopenspec init --help\nopenspec init --tools codex\nopenspec --version</pre><p>Claude + Cursor: <code>openspec init --tools claude,cursor</code>. Yeni bir config oluştururken <code>--language Turkish</code> kullanılabilir; mevcut projede dil talimatı context’e eklenir. Eski OpenSpec kurulumu varsa init’in legacy dosya temizleme etkisini önce inceleyin.</p><h3>5. Güncelleme</h3><pre>npm install -g @fission-ai/openspec@latest\n# Home --prefix ile kurduysan aynı --prefix'i koru.\n# Sonra ilgili proje root'unda:\nopenspec update</pre><p>Asistanın CLI’ı bulduğu, generated skill’in göründüğü ve doğru root’ta çalışıldığı doğrulanmadan kurulumu tamamlandı saymayın.</p><div class="source-list">Resmi kaynaklar: <a href="https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md">OpenSpec installation</a> <a href="https://github.com/Fission-AI/OpenSpec/blob/main/docs/troubleshooting.md">PATH sorunları</a> <a href="https://docs.npmjs.com/cli/v11/configuring-npm/folders/">npm global dizinleri</a> <a href="https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally/">npm user prefix</a></div>'''},
{'title':'Codex user skill kurulumu','tags':'codex user skill global symlink agents toolkit kişisel proje çakışma','body':f'''<h2>OpenSpec skill’lerini kullanıcı genelinde kullanma</h2><p class="when">Kurulum atölyesi / 03. İsteğe bağlı, macOS/Linux manuel düzenlemesi.</p><p>Normal <code>openspec init --tools codex</code> proje <code>.agents/skills/</code> dizinine yazar. Codex ayrıca user <code>~/.agents/skills/</code> dizininden ve symlink’lerden skill okur. Aşağıdaki reçete bu iki davranışı birleştiren öneridir.</p>{pre('atlas-user-skills',user_skills)}<p class="warning-note">Hedef varsa <code>ln -s</code> hata verir ve mevcut dosyayı ezmez. Çakışan skill’i inceleyin; körlemesine <code>-f</code> eklemeyin. Repo ve user aynı skill name’i taşıyorsa ikisi görünebilir; Codex bunları birleştirmez.</p><h3>Güncelleme sahibi</h3><pre>cd "$HOME/.local/share/openspec-toolkit"\nopenspec update</pre><p>CLI güncellemesini kullandığınız package manager ve aynı prefix ile yapın. Symlink’ler toolkit’i izler. Workflow seçimini azaltırsanız toolkit’ten kaldırılan skill için kırık symlink kalabilir; ilgili kullanıcı bağlantısını inceleyip temizleyin. Proje skill’leri kullanıyorsanız ayrıca proje içinde update gerekir.</p><h3>Doğrulama</h3><pre>ls "$HOME/.agents/skills/openspec-propose"\n# Codex sohbetinde:\n$openspec-propose</pre><p>Skill görünmüyorsa Codex’i yeniden açın. İşe başlamadan ilgili proje/planlama root’unun init/config durumu ve erişimini kontrol edin. Toolkit’in boş openspec klasörü ürününüzün planlama root’u değildir.</p><p>Öneri: ekip için repo scoped yöntem; kişisel pilot için user skill. Domain kurallarını global skill’in içine gömmeyin. Generated OpenSpec dosyaları update’te yeniden üretilir; domain’i proje config ve bağlam dosyalarında tutun.</p><div class="source-list"><a href="https://learn.chatgpt.com/docs/build-skills">OpenAI: USER/REPO scope, symlink ve aynı isimler</a> <a href="https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md">OpenSpec: Codex yolu ve managed dosyalar</a></div>'''},
{'title':'Mobil–backend çalışma root’u','tags':'mobil backend multi repo root store workset references context beta monorepo erişim','body':f'''<h2>Bir ürün, iki repo: çalışma düzeni</h2><p class="when">Kurulum atölyesi / 04. Paths ve repo isimleri temsili.</p><h3>Basit başlangıç</h3><pre>~/work/\n  product-plans/   # PM planlama root'u\n    openspec/\n    docs/context/\n  mobile-app/      # gerçek checkout\n  backend/         # gerçek checkout</pre><p>Planlama root’unda init yapın. Asistana iki kod checkout’unu ilgili çalışma ortamında ekleyin ve okunabildiğini doğrulatın. Normal klasör düzeni için store gerekmez. Engineering uygulamasında change ve task sahibi root ayrıca belirlenir.</p><h3>Beta workset: aynı klasörleri yeniden aç</h3>{pre('atlas-workset',workset)}<p>İlk member birincil klasördür. Bu örnek terminal Codex oturumu açar; açık desktop chat’in çalışma dizinini taşımaz. Folder erişimi, bağlantı/sandbox kısıtları ve edit yetkisi ayrıca geçerlidir. Workset kişiseldir, Git’le paylaşılmaz.</p><h3>Beta store: ortak sözleşmeyi ayrı repo’da sahiplen</h3><pre># Yeni store için:\nopenspec store setup team-plans --path "$HOME/work/team-plans"\n# Mevcut takım store checkout'u için:\nopenspec store register "$HOME/work/team-plans"\n# Bu store'da plan yarat:\nopenspec new change recover-result --store team-plans</pre><p>Mevcut store’u setup ile yeniden kurmayın; clone sonrası register edin. Paylaşım ve güncelleme Git ile yapılır; OpenSpec otomatik pull/push yapmaz. AI tool skill kurulumu için store root’unda init çıktısını kontrol edin.</p><h3>Component uygulaması</h3><pre># mobile/backend: kendi yerel openspec root'u\n# ve config içinde ortak bağlam referansı\nschema: spec-driven\nreferences:\n  - team-plans</pre><p>Yerel component change’i ortak sözleşmenin belirli revizyonuna dayanır ve yalnız o repo’nun görevlerini taşır. <code>store: team-plans</code> bir yönlendirme, <code>references:</code> upstream okuma bağlamıdır; farklı davranır. Store pointer tek task listesini repolara otomatik dağıtmaz.</p><h3>İki “context” aynı şey değil</h3><p><code>openspec context --json</code> root + referenced stores kümesini listeler. <code>config.yaml → context:</code> AI yönergelerine verilen proje arka planıdır. Komut tüm mobil/backend kodunu otomatik taramaz. <code>openspec doctor</code> root/reference sağlığını raporlar; kod testi değildir.</p><p class="warning-note">Stores/worksets/references beta. Önce kurulu sürümün <code>--help</code> çıktısını kontrol edin. Farklı domain’ler için bir global defaultStore atamak yerine root’u açık seçmek bu eğitimin önerisidir.</p><div class="source-list"><a href="https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md">Resmi stores/worksets ve component rehberi</a></div>'''},
{'title':'Güçlü ve kalıcı bağlam paketi','tags':'bağlam context config rules kaynak sürüm domain paket glossary karar flag sahip güncel','body':'''<h2>Her PM için ürününe özel bağlam paketi</h2><p class="when">Kurulum atölyesi / 05–07. Aşağıdaki dosya düzeni eğitim önerisidir.</p><h3>Bir kez çıkar, iş başında daralt</h3><p>Her PM’e ortak komut yöntemini verin; ürün/domain kaynaklarını ayrıca eşleyin. İlk pilotta bütün uygulamayı dönüştürmek yerine tek gerçek akış için sözlük, iş kuralı, kaynak sicili ve kritik dalları çıkarın. Her yeni işte yalnız etkilenen bölüm ve ilgili specs/change okunur.</p><table><tr><th>Bilgi</th><th>En uygun kaynak</th><th>Kontrol</th></tr><tr><td>Neden / kullanıcı sorunu</td><td>Görüşme, ticket, analitik, destek kaydı</td><td>Segment, tarih, ölçüm tanımı</td></tr><tr><td>Beklenen iş kuralı</td><td>Onaylı domain kararı / policy</td><td>Karar sahibi ve geçerlilik</td></tr><tr><td>Mevcut davranış</td><td>Kod, API contract, test, gözlem</td><td>Repo/commit, ortam, gerçekten ne incelendi?</td></tr><tr><td>Canlı çalışma koşulu</td><td>Release, deploy, config, flag kaydı</td><td>Canlı sürüm kodla aynı mı?</td></tr><tr><td>Hedef değişiklik</td><td>Proposal + delta + kabul</td><td>Açık kararlar çözüldü mü?</td></tr></table><p>Kod ve onaylı kural çelişirse biri diğerini sessizce geçersiz kılmaz. Mevcut/hedef ayrımını ve karar sahibini yazın. Kaynak göstermek yeterli değil; ilgili bölüm gerçekten okunmalı.</p><h3>Tam örnek config</h3>${kitBlock('atlas-config','openspec/config.example.yaml')}<p>Mevcut config’e birleştirin. Context’e kısa yönlendirme ve sabit gerçekleri koyun; ilgili belgeler okuma rotasıyla açılır. Rules artifact özelidir. Bunlar enforce edilen CI kontrolleri veya otomatik ürün onayı değildir.</p><h3>Takımın giriş dosyası</h3>${kitBlock('atlas-context-index','docs/context/README.md')}<details><summary>Kaynak sicili şablonu</summary>${kitBlock('atlas-sources','docs/context/sources.md')}</details><details><summary>Domain kuralları ve karar şablonu</summary>${kitBlock('atlas-domain','docs/context/domain.md')}</details><details><summary>Akış ve kritik dallar şablonu</summary>${kitBlock('atlas-flow','docs/context/flow.md')}</details><details><summary>AGENTS.md okuma protokolü örneği</summary>${kitBlock('atlas-agents','AGENTS.context-snippet.md')}</details><h3>Güncel tutma</h3><p>PM niyet/scope/ürün kararlarını; teknik sahip repo/API/uyum bilgisini; QA doğrulama kanıtını incelesin. API, kural, flag veya release değiştiğinde etkilenen bağlam kayıtlarını güncelleyin. Yeni işte kaynak sürümünü yeniden kontrol edin. Bu sorumluluk dağılımı öneridir.</p>${src(['customization.md','Resmi context/rules davranışı'],['existing-projects.md','Mevcut projede dar başlangıç'])}'''},
{'title':'Hazır prompt’lar ve ilk iş','tags':'prompt explore propose apply codex günlük ilk iş komut review update sync archive verify','body':'''<h2>İki hazır prompt ve günlük çalışma reçetesi</h2><p class="when">Kurulum atölyesi / 08–09. Codex çağrıları. Placeholder’ları gerçek bilgilerle doldurun.</p><h3>1. Kaynaklı mevcut durum</h3>${kitBlock('atlas-explore-prompt','prompts/01-context-audit.txt')}<p>Eksik kaynaklar ortaya çıktıktan sonra PM/domain sahibinin kararını alın. Belirsiz iş kuralını AI’ın tahminine bırakmayın. İnceleme sırasında kaynaklar erişilemezse daha küçük erişilebilir dilimle ilerleyin.</p><h3>2. İlk change</h3>${kitBlock('atlas-propose-prompt','prompts/02-first-change.txt')}<h3>3. İnceleme ve uygulama</h3><ol><li>Proposal: doğru problem, başarı sinyali, kapsam dışı ve etkilenen ekip.</li><li>Specs: observable davranış, ilgili kritik dallar ve mevcut spec’e doğru delta.</li><li>Design: API uyumu, veri etkisi, eşzamanlılık, eski mobil sürüm ve release sırası.</li><li>Tasks: ilgili repo/sahip ve kabul senaryosuna bağlı doğrulama işi.</li><li>İlgili implementation root’unda apply; gerçek test ve ürün kabulünden sonra sync/archive.</li></ol><p>Review’de durma bu prompt’un talimatıdır. OpenSpec otomatik approval sistemi değildir.</p><table><tr><th>İşlem</th><th>Codex sohbetine</th><th>Claude Code örneği</th></tr><tr><td>Araştır</td><td>$openspec-explore</td><td>/opsx:explore</td></tr><tr><td>Planla</td><td>$openspec-propose &lt;iş&gt;</td><td>/opsx:propose &lt;iş&gt;</td></tr><tr><td>Uygula</td><td>$openspec-apply-change &lt;iş&gt;</td><td>/opsx:apply &lt;iş&gt;</td></tr><tr><td>Planı düzelt</td><td>$openspec-update-change &lt;iş&gt;</td><td>/opsx:update &lt;iş&gt;</td></tr><tr><td>Spec’i birleştir</td><td>$openspec-sync-specs &lt;iş&gt;</td><td>/opsx:sync &lt;iş&gt;</td></tr><tr><td>Arşivle</td><td>$openspec-archive-change &lt;iş&gt;</td><td>/opsx:archive &lt;iş&gt;</td></tr></table><p>Cursor’da colon yerine hyphen: <code>/opsx-propose</code>. Her tool için init’in oluşturduğu dosya ve çağrı biçimi esastır.</p><h3>Terminalde plan ilerlemesini kontrol et</h3><pre>openspec list\nopenspec status --change recover-package-change-result\nopenspec validate recover-package-change-result</pre><p>Validate format/yapıyı kontrol eder. Expanded verify istersen profile seçiminden sonra project update yapıp <code>$openspec-verify-change</code> kullanın. Gerçek testin yerine geçmez. Kapanış deployment değildir.</p>${src(['supported-tools.md','Exact skill names'],['commands.md','Workflow davranışı'])}'''},
{'title':'Takıldığında teşhis ve hazır olma','tags':'hata troubleshooting teşhis path skill erişim context karar root defaultstore profil node npm','body':'''<h2>Takıldığında belirti → kontrol → düzeltme</h2><p class="when">Kurulum atölyesi / 10. Teşhis; otomatik tamir veya test çalıştırma değildir.</p><table><tr><th>Belirti</th><th>Kontrol</th><th>Sonraki adım</th></tr><tr><td>openspec bulunamadı</td><td>node --version, npm prefix -g, executable yolu</td><td>Doğru global bin/PATH; yeni terminal; aynı Node sürümü</td></tr><tr><td>Permission / EACCES</td><td>npm hedefi user altında mı?</td><td>Mevcut version manager veya user prefix; sudo’yu varsayılan çözüm yapma</td></tr><tr><td>Codex /opsx göstermiyor</td><td>.agents/skills/openspec-*/SKILL.md</td><td>Codex skills-only; $openspec-propose kullan</td></tr><tr><td>Yeni workflow yok</td><td>CLI sürümü, profile ve generated skill dosyaları</td><td>Paket güncelle, workflow’u seç, root’ta openspec update</td></tr><tr><td>AI genel metin üretiyor</td><td>Gerçek dosya/simge/commit gösteriyor mu?</td><td>Root ve kaynak yollarını düzelt, ilgili dosyaları okut</td></tr><tr><td>Yanlış ürünün planı değişiyor</td><td>CWD, resolved root, store seçimi, defaultStore</td><td>Root’u açık seç; global fallback’i incele</td></tr><tr><td>Kaynaklar çelişiyor</td><td>Belge sürümü, code/release ve ortam eşleşiyor mu?</td><td>Çelişki kaydı + karar sahibi; sessizce uzlaştırma</td></tr><tr><td>Apply ilerlemiyor</td><td>status --change; eksik artifact veya açık karar</td><td>Bağımlılığı tamamla; taslakları incele</td></tr></table><h3>Read-only teşhis</h3><pre>openspec --version\nopenspec config path\nopenspec config list\nopenspec list\nopenspec status --change &lt;iş&gt;\n# Beta destekli kurulu sürümde:\nopenspec doctor --json\nopenspec context --json</pre><p>Doctor bulgularını okuyun; exit code 0 tek başına bütün sağlığın iyi olduğu anlamına gelmez. CLI/agent erişimi ile code/ürün testleri ayrı konulardır.</p><h3>Eğitimde başarı ne?</h3><p>PM kendi makinesinde CLI/skill/root ayrımını gösterebilmeli, erişilebilir kaynaklarla tek akış inceletebilmeli, açık kararı sahibine götürmeli ve kaynaklı bir change taslağını inceleyebilmeli. “Her detayı biliyorum” hissi yerine bu beceriyi kısa gerçek uygulamayla ölçün.</p>${src(['troubleshooting.md','Resmi sorun giderme'],['cli.md','Teşhis ve profile'])}'''}
]

# Bodies with ${...} snippets intentionally remain JS template strings.
extra = '\natlas.push(\n' + ',\n'.join('{title:'+json.dumps(a['title'],ensure_ascii=False)+',tags:'+json.dumps(a['tags'],ensure_ascii=False)+',body:`'+a['body'].replace('`','\\`')+'`}' for a in atlas) + '\n);\n'
original = original.replace('let index=0,step=0,atlasIndex=0;', extra+'let index=0,step=0,atlasIndex=0;', 1)
js = '''
document.getElementById('workshopBtn').onclick=()=>{closeDialogs();go(16);};
function generateContextPrompt(){const f=new FormData(document.getElementById('contextForm'));document.getElementById('generatedContext').textContent=`$openspec-explore
Ürün/domain: ${f.get('product')}
Akış: ${f.get('flow')}
Root: ${f.get('planning')}
Mobil: ${f.get('mobile')} · commit: <belirt>
Backend: ${f.get('backend')} · commit: <belirt>
Kapsam dışı: ${f.get('outside')}

Önce erişimi doğrula. Varsa docs/context/README.md ve sources.md oku.
Tek akışı ekran → API → domain → veri → test boyunca izle.
Her bulguya kaynak ve sürüm ekle. Gözlem, varsayım, çelişki ve açık kararları ayır.
Canlı flag/deploy bilinmiyorsa belirt. Kod değiştirme.
Çıktı: kaynak sicili, akış, kurallar ve karar sahipleri.`;}
document.getElementById('contextForm').addEventListener('input',generateContextPrompt);
document.getElementById('contextForm').addEventListener('submit',e=>e.preventDefault());generateContextPrompt();
document.querySelectorAll('.readiness-list input').forEach(e=>e.addEventListener('change',()=>{const n=document.querySelectorAll('.readiness-list input:checked').length;document.getElementById('readinessStatus').textContent=`${n} / 5 hazırlık noktası tamamlandı.`;}));
document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy-target]');if(!b)return;const target=document.getElementById(b.dataset.copyTarget);if(!target)return;try{await Promise.race([navigator.clipboard.writeText(target.textContent),new Promise((_,reject)=>setTimeout(()=>reject(Error('timeout')),1200))]);toast('Metin kopyalandı.');}catch(_){const r=document.createRange();r.selectNodeContents(target);const s=window.getSelection();s.removeAllRanges();s.addRange(r);toast('Metin seçildi. ⌘C veya Ctrl+C ile kopyalayabilirsiniz.');}});
'''
original = original.replace("window.addEventListener('hashchange'", js+"\nwindow.addEventListener('hashchange'",1)
original = original.replace("document.getElementById('nextBtn').textContent=step<maxStep()?'Sonraki adım →':end?'Sunum tamamlandı':'Sonraki sahne →';", "document.getElementById('nextBtn').textContent=step<maxStep()?'Sonraki adım →':end?'Atölye tamamlandı':index===15?'Kurulum atölyesi →':'Sonraki sahne →';")
# Keep notes and file paths dynamic. Main closing leads into workshop.
path.write_text(original)
print(json.dumps({'html':str(path),'slides':len(re.findall('class="scene', original)),'kit_files':len(kit),'zip_bytes':zip_path.stat().st_size},ensure_ascii=False))
