from Helper import eda
import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = eda.load_data("ab_testing.xlsx", sheet_name='Control Group')
df_test = eda.load_data("ab_testing.xlsx", sheet_name='Test Group')
eda.check_df(df_control)
eda.check_df(df_test)
# Görev 1:A/B testinin hipotezini tanımlayınız.

# H0: Average Bidding'den elde edilen getiri ile Maximum Bidding'den elde edilen getiri arasında fark bulunmamaktadır.
# H1:... fark bulunmaktadır.

# Görev 2: Çıkan test sonuçlarının istatistiksel olarak anlamlı olup olmadığını yorumlayınız.

# Normallik Varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df_control["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value 0,05'ten büyük olduğu için HO reddedilemez. Normal dağılımdadır.

test_stat, pvalue = shapiro(df_test["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value 0,05'ten büyük olduğu için HO reddedilemez. Normal dağılımdadır.

# Varyans Homojenligi Varsayımı
# H0: Varyanslar Homojendir.
# H1: ... Homojen Değildir.

test_stat, pvalue = levene(df_control["Earning"],
                           df_test["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value 0,05'ten büyük olduğu için HO reddedilemez. Varyanslar Homojendir.

# Görev 3: Hangi testleri kullandınız? Sebeplerini belirtiniz.

###############################################################################
# 1. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 2. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir. Welch testi (equal_var=False)
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.
###############################################################################

# Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) uygulandı.

test_stat, pvalue = ttest_ind(df_control["Earning"],
                              df_test["Earning"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value 0,05'ten büyük olduğu için HO reddedilemez.

# Görev 4: Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?

# Earnings'e göre bakıldığında Average Bidding ile Maximum Bidding arasında
# istatiksel olarak anlamlı bir fark bulunmamaktadır.


# Click/Earning değeri üzerinden AB Testi

df_control["click/Earning"] = df_control["Click"] / df_control["Earning"]
df_test["click/Earning"] = df_test["Click"] / df_test["Earning"]

print(df_control.columns)
# Normallik Varsayımı
test_stat, pvalue = shapiro(df_control["click/Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_test["click/Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value 0,05'ten küçük olduğu için HO reddedilir. Normal dağılımda değildir.

# Varyans homojenliği
test_stat, pvalue = levene(df_control["click/Earning"].dropna(),
                           df_test["click/Earning"].dropna())

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# nonparametrik

test_stat, pvalue = mannwhitneyu(df_control["click/Earning"],
                                 df_test["click/Earning"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))