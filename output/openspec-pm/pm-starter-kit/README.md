# OpenSpec PM başlangıç paketi

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
