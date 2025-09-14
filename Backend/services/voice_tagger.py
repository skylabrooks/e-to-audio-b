import json
from .voice_classifier import VoiceClassifier

class VoiceTagger:
    @staticmethod
    def tag_all_voices(voices):
        """Tag all voices with comprehensive classification"""
        tagged_voices = []
        
        for voice in voices:
            # Get language code (first one if multiple)
            language_code = voice['language_codes'][0] if voice['language_codes'] else 'unknown'
            
            # Get classification
            classification = VoiceClassifier.classify_voice(
                voice['name'], 
                language_code, 
                voice['ssml_gender']
            )
            
            # Create tagged voice with all metadata
            tagged_voice = {
                # Original voice data
                'name': voice['name'],
                'language_codes': voice['language_codes'],
                'natural_sample_rate_hertz': voice['natural_sample_rate_hertz'],
                'ssml_gender': voice['ssml_gender'],
                
                # Classification tags
                'tags': {
                    'language': classification['language'],
                    'region': classification['region'],
                    'gender': classification['gender'],
                    'quality': classification['quality'],
                    'use_case': classification['use_case'],
                    'character_theme': classification['character_theme'],
                    'tone': classification['tone'],
                    'age': classification['age']
                },
                
                # Avatar URL
                'avatar_url': classification.get('avatar_url', ''),
                
                # Searchable text for filtering
                'search_text': f"{voice['name']} {classification['language']} {classification['region']} {classification['gender']} {classification['character_theme']} {classification['use_case']}".lower()
            }
            
            tagged_voices.append(tagged_voice)
        
        return tagged_voices
    
    @staticmethod
    def filter_voices(tagged_voices, filters=None):
        """Filter voices by tags"""
        if not filters:
            return tagged_voices
        
        filtered = tagged_voices
        
        for key, value in filters.items():
            if value and key in ['language', 'region', 'gender', 'quality', 'use_case', 'character_theme', 'tone', 'age']:
                filtered = [v for v in filtered if v['tags'].get(key) == value]
            elif key == 'search' and value:
                search_term = value.lower()
                filtered = [v for v in filtered if search_term in v['search_text']]
        
        return filtered
    
    @staticmethod
    def get_filter_options(tagged_voices):
        """Get all available filter options"""
        options = {
            'languages': set(),
            'regions': set(),
            'genders': set(),
            'qualities': set(),
            'use_cases': set(),
            'character_themes': set(),
            'tones': set(),
            'ages': set()
        }
        
        for voice in tagged_voices:
            tags = voice['tags']
            options['languages'].add(tags['language'])
            options['regions'].add(tags['region'])
            options['genders'].add(tags['gender'])
            options['qualities'].add(tags['quality'])
            options['use_cases'].add(tags['use_case'])
            options['character_themes'].add(tags['character_theme'])
            options['tones'].add(tags['tone'])
            options['ages'].add(tags['age'])
        
        # Convert sets to sorted lists
        return {k: sorted(list(v)) for k, v in options.items()}