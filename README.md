A/B Testi ile Bidding Yöntemlerinin Dönüşüm Karşılaştırması

Bu proje, bir müşterinin web sitesindeki teklif verme yöntemlerini karşılaştırmak amacıyla gerçekleştirdiği A/B testinin sonuçlarını analiz ediyor.

İş Problemi

Bombabomba.com, yeni bir teklif verme yöntemi olan "average bidding"i mevcut "maximum bidding" yöntemiyle karşılaştırmak istiyor. Bu iki yöntem arasındaki dönüşüm oranlarını karşılaştırmak ve hangi yöntemin daha iyi performans gösterdiğini belirlemek amaçlanıyor.

Veri Seti

Proje, "ab_testing.xlsx" adlı Excel dosyasından elde edilen verileri içermektedir. Veri seti kontrol ve test gruplarına ayrılmıştır.


Analiz Adımları

Veri Seti Hazırlama ve Analiz Etme:


Kontrol ve test grupları ayrı ayrı analiz edilir.
Veri setleri birleştirilir ve "Bidding" sütunu eklenir.

A/B Testinin Hipotezinin Tanımlanması:

İki hipotez tanımlanır: H0 (Null hypothesis) ve H1 (Alternative hypothesis).
Kontrol ve test gruplarının "Purchase" ortalamaları incelenir.
Hipotez Testinin Gerçekleştirilmesi:

Normallik varsayımı ve varyans homojenliği kontrol edilir.
Uygun test seçilir (bağımsız iki örneklem T testi).
Elde edilen p-value değeri yorumlanır.

Sonuçların Analizi:

Elde edilen p-value değerine göre gruplar arasındaki anlamlı fark değerlendirilir.
Müşteriye tavsiye sunulur.

Sonuçlar

Yapılan A/B test sonucunda, "average bidding" ve "maximum bidding" yöntemleri arasında Purchase ortalamaları açısından anlamlı bir fark bulunmadığı sonucuna ulaşıldı. Müşteriye, daha fazla veri toplayarak ve testi daha uzun süre devam ettirerek daha kesin sonuçlar elde etmesi önerildi.

Bu proje, Python programlama dili kullanılarak veri analizi adımlarının ayrıntılı bir şekilde gösterildiği bir örnektir. Projenin tamamı "ab_test_analysis.py" dosyasında yer almaktadır. Detaylı bilgi için lütfen kodu inceleyin.
