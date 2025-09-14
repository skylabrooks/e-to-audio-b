class VoiceClassifier:
    @staticmethod
    def classify_voice(name, language_code, gender):
        return {
            'language': 'English',
            'region': 'US' if 'US' in name else 'GB',
            'gender': gender.lower(),
            'quality': 'Standard',
            'use_case': 'General',
            'character_theme': 'Neutral',
            'tone': 'Friendly',
            'age': 'Adult'
        }