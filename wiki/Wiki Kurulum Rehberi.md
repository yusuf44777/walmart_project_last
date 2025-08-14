# 📚 Wiki Kurulum Rehberi

> **Obsidian + GitHub Pages** ile kurumsal wiki sistemi kurulumu

## 🎯 Wiki Sisteminin Amacı

Bu wiki sistemi **kurumsal hafıza oluşturma** ve **proje dokümantasyonu** için tasarlanmıştır:

- ✅ **Obsidian ile yerel çalışma** - Markdown tabanlı, hızlı ve güçlü
- ✅ **GitHub Pages ile ücretsiz yayın** - Otomatik publish, custom domain
- ✅ **Ekip çalışması** - Git-based collaboration
- ✅ **Arama ve linkler** - İçerik keşfedilebilirlik

## 🚀 Hızlı Kurulum

### Adım 1: Repository Hazırlığı
```bash
# Repository'yi klonlayın
git clone https://github.com/yusuf44777/walmart_project_last.git
cd walmart_project_last

# Wiki klasörü kontrolü
ls -la wiki/
```

### Adım 2: Obsidian Setup
1. **Obsidian indirin**: https://obsidian.md/download
2. **Vault açın**: `wiki` klasörünü seçin
3. **Settings > Files & Links**:
   - Use `[[Wikilinks]]`: ✅ Açık
   - New link format: `Shortest path`
   - Use Markdown links: ✅ Açık

### Adım 3: GitHub Pages Aktivasyonu
1. **GitHub repository** > **Settings** > **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: `main` 
4. **Folder**: `/ (root)` (wiki klasörünü manuel seçemiyoruz)
5. **Save** butonuna tıklayın

### Adım 4: Wiki Index Sayfası
Ana dizine `index.html` dosyası ekleyin:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; URL=wiki/index.html">
    <title>Walmart AI Wiki</title>
</head>
<body>
    <p><a href="wiki/index.html">Wiki'ye yönlendiriliyorsunuz...</a></p>
</body>
</html>
```

## 📖 Wiki Kullanımı

### Obsidian'da Çalışma
```
1. wiki/ klasörünü Obsidian'da vault olarak açın
2. README.md'den başlayın
3. [[Link]] formatı ile sayfa linkleyin
4. Ctrl+N ile yeni sayfa oluşturun
5. Ctrl+O ile hızlı sayfa arama
```

### GitHub'a Gönderme
```bash
# Değişiklikleri commit edin
git add wiki/
git commit -m "Wiki güncellendi: yeni sayfa eklendi"
git push origin main

# GitHub Pages otomatik güncellenecek (2-5 dakika)
```

### Wiki Sayfaları
Mevcut wiki yapısı:

```
wiki/
├── README.md              # Ana index
├── Ana Sayfa.md           # Proje ana sayfası  
├── Hızlı Başlangıç.md     # 5 dakika kurulum
├── Kullanım Kılavuzu.md   # Detaylı kullanım
├── Sistem Mimarisi.md     # Teknik mimari
├── Kurulum Rehberi.md     # Geliştirici kurulumu
├── Model Eğitimi.md       # AI model training
├── Deployment.md          # Production deployment
├── SSS.md                 # Sık sorulan sorular
└── assets/                # Görseller, dosyalar
```

## 🔗 Link Yönetimi

### Internal Links (Wiki İçi)
```markdown
# Wikilink formatı (Obsidian için)
[[Ana Sayfa]]
[[Hızlı Başlangıç]]

# Markdown link formatı (GitHub Pages için)
[Ana Sayfa](Ana%20Sayfa.md)
[Hızlı Başlangıç](Hızlı%20Başlangıç.md)
```

### External Links
```markdown
[GitHub Repository](https://github.com/yusuf44777/walmart_project_last)
[Streamlit Cloud](https://share.streamlit.io)
[Ollama](https://ollama.ai)
```

## 🎨 Wiki Customization

### Obsidian Tema ve Plugins
```json
// .obsidian/app.json'da önerilen ayarlar
{
  "theme": "obsidian",
  "cssTheme": "Blue Topaz",
  "plugins": [
    "obsidian-git",           // Git entegrasyonu
    "templater-obsidian",     // Şablon sistemi
    "obsidian-admonition",    // Callout boxes
    "dataview",               // Dinamik içerik
    "table-editor-obsidian"   // Tablo editörü
  ]
}
```

### CSS Customization
```css
/* .obsidian/snippets/custom.css */
.markdown-preview-view h1 {
    color: #2196F3;
    border-bottom: 2px solid #E3F2FD;
}

.markdown-preview-view blockquote {
    background: #F5F5F5;
    border-left: 4px solid #2196F3;
    padding: 10px;
}
```

## 📱 Responsive Wiki

### Mobile Uyumluluk
GitHub Pages otomatik responsive olacak şekilde ayarlanmıştır:

- **📱 Mobile**: Tam özellik desteği
- **💻 Desktop**: En iyi deneyim  
- **📋 Tablet**: Optimized layout

### Search Özelliği
```javascript
// Gelecekte eklenebilir: Wiki içi arama
function searchWiki(query) {
    // Implement client-side search
}
```

## 🔄 Workflow

### Günlük Wiki Yönetimi
```bash
# 1. Güncel wiki'yi çek
git pull origin main

# 2. Obsidian'da düzenlemeler yap
# 3. Değişiklikleri kaydet

# 4. Git'e gönder
git add wiki/
git commit -m "docs: [sayfa-adı] güncellendi"
git push origin main

# 5. GitHub Pages kontrolü (2-5 dakika)
```

### Ekip Çalışması
```bash
# Feature branch oluştur
git checkout -b docs/yeni-sayfa

# Wiki sayfa oluştur/düzenle
# Obsidian'da çalış

# Pull request oluştur
git add wiki/
git commit -m "docs: yeni sayfa eklendi"
git push origin docs/yeni-sayfa

# GitHub'da PR aç
# Review sonrası merge
```

## 📊 Wiki Analytics

### GitHub Insights
- **Traffic**: Settings > Insights > Traffic
- **Popular pages**: Hangi sayfalar çok ziyaret edilmiş
- **Referrers**: Nereden gelinmiş

### Content Management
```markdown
<!-- Her sayfanın altında -->
---
*📅 Son güncelleme: 14 Ağustos 2025 | 
👤 Güncelleyen: @username | 
📊 Versiyon: 1.2*
```

## 🔒 Güvenlik ve Backup

### Automatic Backup
```bash
# Git repository otomatik backup'tır
# Ek olarak:

# Local backup
rsync -av wiki/ ~/backup/wiki-$(date +%Y%m%d)/

# Cloud backup
# GitHub otomatik, ek olarak GitLab/Bitbucket mirror
```

### Access Control
```yaml
# Public repository - herkes okuyabilir
# Private repository - sadece team members
# Organization secrets - API keys vs.
```

## 📈 Wiki Growth Strategy

### İçerik Stratejisi
1. **Core Documentation** ✅ (Tamamlandı)
   - Kurulum rehberleri
   - Kullanım kılavuzları
   - Teknik dokümantasyon

2. **User Generated Content** 🔄 (Devam ediyor)
   - SSS genişletme
   - Use case studies
   - Best practices

3. **Advanced Topics** 📅 (Planlanıyor)
   - Performance tuning
   - Advanced configurations
   - Integration guides

### Community Building
```markdown
# Katkıda bulunma rehberi
1. Wiki eksiklerini belirleyin
2. Issue açın veya mevcut issue'ya atanın
3. Branch oluşturup çalışın
4. PR gönderin
5. Review ve merge süreci
```

## 🎯 Wiki Success Metrics

### KPI'lar
- **📖 Page Views**: Aylık wiki ziyaret sayısı
- **🔍 Search Usage**: İçerik keşfedilebilirlik
- **⏱️ Time on Page**: İçerik kalitesi göstergesi
- **🔄 Return Visits**: Wiki'nin değeri
- **📝 Contribution Rate**: Ekip katılımı

### Feedback Sistemi
```markdown
<!-- Her sayfanın altında -->
## 💭 Bu sayfa yararlı oldu mu?
👍 Evet | 👎 Hayır | 💬 [Geri bildirim bırak](issues/new)
```

---

## 🎉 Wiki Kurulumu Tamamlandı!

Artık kurumsal wiki sisteminiz hazır:

- ✅ **Obsidian ile güçlü editör**
- ✅ **GitHub Pages ile ücretsiz hosting**
- ✅ **Otomatik deployment**
- ✅ **Ekip çalışması desteği**
- ✅ **Mobile responsive**

### Sonraki Adımlar
1. **Takımı eğitin** - Obsidian ve workflow
2. **İçerik genişletin** - Yeni sayfalar ekleyin
3. **Feedback toplayın** - Kullanıcı deneyimi
4. **Analytics setup** - Başarı metriklerini takip edin

---

*📚 Wiki kurulum versiyon: 1.0 | 🌐 Platform: GitHub Pages | ⚡ Setup süresi: 15 dakika | 💰 Maliyet: Ücretsiz*
