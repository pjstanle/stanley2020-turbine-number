import numpy as np
import matplotlib.pyplot as plt
    
# hist = [-0.72471361, -0.87199882, -0.87199882, -1.54415816, -1.54415816, -1.54415816,
#         -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816,
#         -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816,
#         -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816,
#         -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816, -1.54415816,
#         -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942,
#         -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942,
#         -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942,
#         -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.75405942, -1.78274619,
#         -1.78274619, -1.78274619, -1.78274619, -1.78274619, -1.78274619, -1.78274619,
#         -1.78274619, -1.78475605, -1.79827759, -1.79827759, -1.79908961, -1.79908961,
#         -1.79908961, -1.79908961, -1.79908961, -1.79908961, -1.79908961, -1.79908961,
#         -1.79908961, -1.79908961, -1.80018021, -1.80018021, -1.80018021, -1.80018021,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337, -1.80186337,
#         -1.80186337, -1.82388192, -1.82388192, -1.82388192, -1.82388192, -1.82388192,
#         -1.82388192, -1.82388192, -1.82403464, -1.82403464, -1.82859493, -1.82859493,
#         -1.82859493, -1.82859493, -1.82859493, -1.82859493, -1.84584193, -1.84584193,
#         -1.84584193, -1.84710113, -1.85685547, -1.86023133, -1.86023133, -1.86115788,
#         -1.86115788, -1.86115788, -1.86115788, -1.86115788, -1.86115788, -1.86115788,
#         -1.86115788, -1.86115788, -1.86115788, -1.86115788, -1.86115788, -1.86115788,
#         -1.86115788, -1.86115788, -1.86115788, -1.86115788, -1.86115788, -1.86115788,
#         -1.86115788, -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906,
#         -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906,
#         -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906 , -1.8613906,
#         -1.8613906 , -1.8613906 , -1.86140915, -1.86140915, -1.86140915, -1.86140915,
#         -1.86140915, -1.86140915, -1.86140915, -1.86140915, -1.86140915, -1.86140915,
#         -1.86140915, -1.86140915, -1.86156624, -1.86156624, -1.86156624, -1.86156624,
#         -1.86156624, -1.86156624, -1.86156624, -1.86156624, -1.86156624, -1.86156624,
#         -1.86156624, -1.86156624, -1.86156624, -1.86156624, -1.86171695, -1.86171695,
#         -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695,
#         -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695,
#         -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695,
#         -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86171695, -1.86174618,
#         -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.86174618,
#         -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.86174618,
#         -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.86174618,
#         -1.86174618, -1.86174618, -1.86174618, -1.86174618, -1.88208546, -1.88208546,
#         -1.88208546, -1.88208546, -1.88208546, -1.88208546, -1.88208546, -1.88208546,
#         -1.88208546, -1.88208546, -1.88208546, -1.88208546, -1.88208546, -1.88399628,
#         -1.88399628, -1.88399628, -1.88483662, -1.88483662, -1.88499898, -1.88559275,
#         -1.88630755, -1.88630755, -1.88630755, -1.88715302, -1.88715302, -1.88715302,
#         -1.88715302, -1.88715302, -1.88715302, -1.88715302, -1.88715302, -1.88745545,
#         -1.88745545, -1.88745545, -1.88745545, -1.8879842 , -1.8879842 , -1.8879842,
#         -1.8879842 , -1.8879842 , -1.88820974, -1.88820974, -1.88820974, -1.88820974,
#         -1.88820974, -1.88820974, -1.88820974, -1.88820974, -1.88820974, -1.88820974,
#         -1.88820974, -1.88823094, -1.88823094, -1.88827404, -1.88827404, -1.88827404,
#         -1.88827404, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799, -1.88840799,
#         -1.88840799, -1.88840799, -1.88840799, -1.88840799]


hist = [-4.27427284, -4.27427284, -4.59173964, -4.59173964, -4.59173964 ,-4.97744598,
 -4.97744598, -5.29736671, -5.29736671, -5.29736671, -5.46084837 ,-5.61552231,
 -5.63739731, -5.91074371, -5.91074371, -5.91074371, -5.91074371 ,-5.91074371,
 -5.91074371, -5.91074371, -5.91074371, -5.91074371, -5.91074371 ,-5.91074371,
 -5.94391632, -5.95702131, -5.98667934, -6.07736096, -6.11385275 ,-6.11385275,
 -6.11385275, -6.11385275, -6.11385275, -6.11869844, -6.11869844 ,-6.12864425,
 -6.12864425, -6.12864425, -6.12864425, -6.12864425, -6.12864425 ,-6.12864425,
 -6.12939887, -6.13836431, -6.14801597, -6.14801597, -6.14801597 ,-6.17770239,
 -6.17770239, -6.17770239, -6.17770239, -6.17770239, -6.17770239 ,-6.17770239,
 -6.22805702, -6.22805702, -6.22805702, -6.22805702, -6.23020771 ,-6.23020771,
 -6.23020771, -6.23020771, -6.23020771, -6.23020771, -6.23020771 ,-6.23020771,
 -6.23020771, -6.23020771, -6.23020771, -6.23378779, -6.23378779 ,-6.24200287,
 -6.24200287, -6.24200287, -6.24200287, -6.24200287, -6.24200287 ,-6.24200287,
 -6.24200287, -6.24267338, -6.24267338, -6.24267338, -6.24267338 ,-6.24746322,
 -6.24746322, -6.24746322, -6.24746322, -6.2710148 , -6.2710148  ,-6.2710148,
 -6.2710148 , -6.2710148 , -6.2710148 , -6.2710148 , -6.2710148  ,-6.2710148,
 -6.2710148 , -6.2710148 , -6.2710148 , -6.2710148 , -6.2710148  ,-6.2710148,
 -6.2710148 , -6.27768751, -6.28066575, -6.28066575, -6.28156114 ,-6.28156114,
 -6.28156114, -6.28156114, -6.28156114, -6.28156114, -6.28822327 ,-6.28822327,
 -6.28822327, -6.28822327, -6.28822327, -6.28822327, -6.28822327 ,-6.28822327,
 -6.29072685, -6.29072685, -6.29072685, -6.29072685, -6.29364171 ,-6.29364171,
 -6.29364171, -6.29364171, -6.29364171, -6.29364171, -6.29809268 ,-6.29809268,
 -6.29809268, -6.29809268, -6.29809268, -6.29809268, -6.29809268 ,-6.29809268,
 -6.29809268, -6.29809268, -6.29809268, -6.2981473 , -6.2981473  ,-6.2981473,
 -6.2981473 , -6.2981473 , -6.29889515, -6.29889515, -6.29889515 ,-6.29889515,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878, -6.30622878, -6.30622878 ,-6.30622878,
 -6.30622878, -6.30622878, -6.30622878]

plt.plot(hist)
plt.show()