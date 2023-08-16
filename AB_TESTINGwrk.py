#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df_control = pd.read_excel(r"dataset/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel(r"dataset/ab_testing.xlsx", sheet_name="Test Group")

df_control.head()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
df_control.describe().T
df_test.describe().T


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz. Bidding(teklif verme) columns oluştur.

df_control["Bidding"] = "Maximum_Bidding"

df_control.groupby("Bidding").agg({"Purchase": "mean"})

df_test["Bidding"] = "Average_Bidding"

df_test.groupby("Bidding").agg({"Purchase": "mean"})

df = pd.concat([df_control, df_test])

df.head()
df.tail()


#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

# H0 : M1 = M2  # Average bidding ve Maksimum Bidding purchase ortalamaları Arasında İstatiksel Olarak Anlamlı Fark yoktur
# H1 : M1!= M2  # Average bidding ve Maksimum Bidding purchase ortalamaları Arasında İstatiksel Olarak Anlamlı Fark vardır

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby("Bidding").agg({"Purchase": "mean"})

#average bidding(test) > maximum bidding(control) doğru bir varsayım mı tesadüf mü? tesadüf olabilir bu nedenle A/B testi yapılacak.
#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = shapiro(df.loc[df["Bidding"] == "Maximum_Bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9773, p-value = 0.5891 H0 reddedilemez, normal dağılıyor.


test_stat, pvalue = shapiro(df.loc[df["Bidding"] == "Average_Bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9589, p-value = 0.1541 H0 reddedilmez normal dağılıyor.

# Varyans Homojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ


test_stat, pvalue = levene(df.loc[df["Bidding"] == "Maximum_Bidding", "Purchase"],
                           df.loc[df["Bidding"] == "Average_Bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 2.6393, p-value = 0.1083 H0 REDDEDİLMEZ varyanslar homojen.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

# Her iki varsayım da sağlanıyor. Yani bağımsız iki örneklem T testi yap. PARAMETRİK TEST


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.
# H0 : M1 = M2  # Average bidding ve Maksimum Bidding purchase ortalamaları Arasında İstatiksel Olarak Anlamlı Fark yoktur
# H1 : M1!= M2  # Average bidding ve Maksimum Bidding purchase ortalamaları Arasında İstatiksel Olarak Anlamlı Fark vardır

test_stat, pvalue = ttest_ind(df.loc[df["Bidding"] == "Maximum_Bidding", "Purchase"],
                           df.loc[df["Bidding"] == "Average_Bidding", "Purchase"],
                            equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################
# p-value değeri 0.3493 geldi. H0 REDDEDİLMEZ.Her iki yöntem arasında anlamlı bir fark yoktur.
# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#Her iki varsayım da sağlanıyor.Bağımsız İki Örneklem T Testi Yap. PARAMETRİK TEST


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

#Sonuçlara göre Average Bidding ile MAximum Bidding arasında Purchase ortalaması açısından anlamlı bir fark yoktur.
#Verilerin yetersizliği nedeiyle bir süre daha uygulamanın denenmesi önerilebilir.