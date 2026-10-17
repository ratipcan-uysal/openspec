# Tek akışın mevcut davranışı

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
