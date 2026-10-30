"""Localization completeness is independent of translation quality.

English and Simplified Chinese are the maintained source languages. Other
languages normally use machine translation or English fallback text, but every
language must contain the same keys within each deployable mod root.
"""

LOCALIZATION_LANGUAGES = (
    "english", "simp_chinese", "french", "german", "spanish", "russian",
    "polish", "japanese", "korean", "braz_por", "turkish",
)

# Strongest to weakest. Provenance is registered explicitly, never inferred from
# the language after the user-requested initial inventory.
LOCALIZATION_GRADES = ("原创", "AI生成", "翻译", "占位", "缺失")
LOCALIZATION_GRADE_RANK = {grade: len(LOCALIZATION_GRADES) - index
                           for index, grade in enumerate(LOCALIZATION_GRADES)}
