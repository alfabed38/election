# Türkiye Seçim Simülatörü (2025-2027)

Bu proje, Türkiye genel seçimleri için gelişmiş bir simülasyon ve analiz aracıdır. 2023 seçim sonuçlarını baz alarak, güncel anket verileri ve RAS algoritmasıyla (Iterative Proportional Fitting) seçmen oy geçişlerini tahmin eder ve D'Hondt sistemiyle milletvekili dağılımını hesaplar.

## Özellikler

*   **Gelişmiş Simülasyon:** 2023 verileri ve güncel anketler (Wikipedia) kullanılarak ile il bazında tahminler.
*   **RAS Algoritması:** Oy geçiş matrisi oluşturmak için yapılandırılabilir iterasyon ayarı (10.000 - 100.000).
*   **İttifak Yönetimi:** Sürükle-bırak veya menü ile partileri ittifaklara atama, yeni ittifak kurma.
*   **D'Hondt Sistemi:** İl bazında ve ittifak içi (Yeni Seçim Yasası uyumlu) sandalye dağılımı.
*   **Fırsat Haritası (Öncelik Analizi):** Hangi ilde kaç oy farkla vekil kazanılıp kaybedildiğini yüzdesel olarak gösterir.
*   **Detaylı Tablolar:**
    *   Ulusal Seçim Sonuçları (Parti ve İttifak Bazlı)
    *   İl İl Milletvekili Dağılımı
    *   İl İl Oy Oranları
    *   Oy Geçiş Matrisi (Heatmap)
*   **Görselleştirme:** Meclis sandalye dağılım grafiği ve renk kodlu analizler.

## Nasıl Kullanılır?

Proje tamamen istemci taraflı (client-side) çalışır. Kurulum gerektirmez.

1.  `index.html` dosyasını tarayıcınızda açın (Çift tıklayın).
2.  Sol panelden **Anket Dönemi** ve **Veri Tipi** seçin.
3.  İttifakları düzenleyin (Parti ekleyin, çıkartın veya ittifak ismini değiştirin).
4.  **Simülasyonu Başlat** butonuna tıklayın.

## Dosya Yapısı

*   `index.html`: Uygulamanın kendisi (HTML, CSS, JS içerir).
*   `polls.js`: Wikipedia'dan çekilmiş güncel anket verileri.
*   `fetch_polls.py`: (Geliştirici) Anket verilerini yenilemek için kullanılan Python betiği.

## Veri Güncelleme

Yeni anket verileri eklemek için `fetch_polls.py` betiğini çalıştırabilir veya `polls.js` dosyasını manuel olarak düzenleyebilirsiniz.

## Lisans

MIT License.
