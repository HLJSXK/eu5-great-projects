"""Localization completeness is independent of translation quality.

English and Simplified Chinese are the maintained source languages. Other
languages normally use machine translation or English fallback text, but every
language must contain the same keys within each deployable mod root.
"""

LOCALIZATION_LANGUAGES = (
    "english", "simp_chinese", "french", "german", "spanish", "russian",
    "polish", "japanese", "korean", "braz_por", "turkish",
)
