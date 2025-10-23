document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Gözetlenecek hedef elementi seç
    const mapElement = document.getElementById("map-container");

    // Harita container'ı sayfada bulunamazsa dur
    if (!mapElement) {
        console.warn("Harita container (map-container) bulunamadı.");
        return;
    }

    //------------------------------------------------------------------
    // HARİTA BAŞLATMA FONKSİYONLARI
    // (Scriptler yüklendikten SONRA çalışacaklar)
    //------------------------------------------------------------------

    /**
     * Verdiğiniz ilk kod bloğu: Haritayı başlatır.
     */
    function initializeMap() {
        console.log("Harita başlatılıyor (new FlaMap)...");
        try {
            // map_cfg objenizin script'lerden önce tanımlandığından emin olun
            map_cfg.mapWidth = 0;
            var map = new FlaMap(map_cfg);
            map.drawOnDomReady('map-container');
            
            // Harita çizilme komutu verildi, şimdi DOM değişikliklerini
            // izleyen gözlemciyi kur (zoom butonlarını kaldırmak için).
            setupMapMutationObserver();

        } catch (e) {
            console.error("Harita başlatılırken hata oluştu (FlaMap):", e);
        }
    }

    /**
     * Verdiğiniz ikinci kod bloğu: Zoom butonlarını kaldırır.
     */
    function setupMapMutationObserver() {
        console.log("Zoom butonlarını kaldırmak için MutationObserver kuruluyor...");
        const targetNode = document.getElementById('map-container');
        if (!targetNode) return;

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        // Yeni eklenen node'un kendisi butonsa kaldır
                        if (node.matches('a.fm-scale-plus, a.fm-scale-minus')) {
                            node.remove();
                        }
                        // Yeni eklenen node'un *içinde* buton varsa onları da kaldır
                        if (node.querySelectorAll) {
                            node.querySelectorAll('a.fm-scale-plus, a.fm-scale-minus').forEach((el) => el.remove());
                        }
                    }
                });
            });
        });

        // Gözlemlemeyi başlat
        observer.observe(targetNode, { childList: true, subtree: true });
        
        // Gözlemci çalışmaya başlamadan önce (eğer harita çoktan çizildiyse)
        // mevcut butonları da temizlemeyi dene
        targetNode.querySelectorAll('a.fm-scale-plus, a.fm-scale-minus').forEach((el) => el.remove());
    }

    //------------------------------------------------------------------
    // SCRIPT YÜKLEYİCİ
    //------------------------------------------------------------------

    /**
     * Dinamik olarak script yükler ve bittiğinde haber verir (Promise).
     */
    const loadScript = (src) => {
        return new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src = src;
            script.onload = () => resolve(script); // Yüklenme başarılı
            script.onerror = () => reject(new Error(`Script yüklenemedi: ${src}`)); // Yükleme başarısız
            document.body.appendChild(script);
        });
    };

    //------------------------------------------------------------------
    // INTERSECTION OBSERVER (Tetikleyici)
    //------------------------------------------------------------------

    /**
     * Element görünüme girdiğinde çalışacak ana fonksiyon.
     */
    const observerCallback = async (entries, observer) => {
        // Element görünüme girdi mi?
        if (entries[0].isIntersecting) {
            console.log("Harita görünüme girdi. Scriptler yükleniyor...");

            try {
                // *** DOSYA YOLLARINI KONTROL EDİN ***
                // 1. Raphael'i yükle
                await loadScript("/static/assets/js/raphael.min.js"); 
                
                // *** DOSYA YOLLARINI KONTROL EDİN ***
                // 2. Harita script'ini yükle
                await loadScript("/static/assets/js/map.min.js");
                
                // 3. Scriptler yüklendi, şimdi haritayı başlatan fonksiyonu çağır
                initializeMap(); 

            } catch (error) {
                console.error("Harita scriptleri yüklenirken hata oluştu:", error);
            }

            observer.unobserve(mapElement);
        }
    };

    const options = {
        rootMargin: '200px 0px' 
    };
        const observer = new IntersectionObserver(observerCallback, options);
    observer.observe(mapElement);
});