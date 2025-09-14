class VoiceAvatarGenerator:
    @staticmethod
    def generate_avatar_url(voice_name, gender, character_theme, language):
        """Generate avatar URL based on voice characteristics"""
        
        # Use voice name as seed for consistency
        seed = voice_name.lower().replace('-', '').replace(' ', '')
        
        # Select avatar style based on character theme
        style_map = {
            'dark': 'bottts',  # Robot/mechanical for villains
            'playful': 'fun-emoji',  # Colorful emoji for cartoon characters
            'mythological': 'personas',  # Epic personas for fantasy
            'neutral': 'avataaars'  # Professional human avatars
        }
        
        style = style_map.get(character_theme, 'avataaars')
        
        # Theme-specific parameters
        theme_params = VoiceAvatarGenerator._get_theme_params(style, gender, character_theme)
        
        # Generate URL
        base_url = f"https://api.dicebear.com/7.x/{style}/svg"
        return f"{base_url}?seed={seed}{theme_params}&backgroundColor=transparent&size=128"
    
    @staticmethod
    def _get_theme_params(style, gender, theme):
        """Get theme-specific parameters for avatar generation"""
        params = ''
        
        if style == 'avataaars':  # Professional human avatars
            if gender == 'FEMALE':
                params = '&hair=longHairStraight,longHairCurly&clothingColor=3c4f5c,262e33&skinColor=ae5d29,f8d25c'
            else:
                params = '&hair=shortHairShortFlat,shortHairDreads01&clothingColor=262e33,3c4f5c&skinColor=ae5d29,f8d25c'
                
        elif style == 'bottts':  # Dark/villain characters
            if theme == 'dark':
                params = '&colors=2d1b69,1a1a2e,16213e&primaryColorLevel=600&secondaryColorLevel=700'
            else:
                params = '&colors=4a90e2,7b68ee,9b59b6'
                
        elif style == 'fun-emoji':  # Playful characters
            params = '&colors=ff6b6b,4ecdc4,45b7d1,96ceb4,feca57'
            
        elif style == 'personas':  # Mythological characters
            params = '&colors=4ecdc4,45b7d1,96ceb4,a8e6cf,dcedc1'
            
        return params
    
    @staticmethod
    def get_fallback_avatar(gender):
        """Fallback avatar if generation fails"""
        style = 'initials'
        seed = 'voice' + gender.lower()
        return f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}&backgroundColor=6366f1&color=ffffff&size=128"