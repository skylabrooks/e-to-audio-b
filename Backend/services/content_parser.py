import re
import logging

logger = logging.getLogger(__name__)

class ContentParser:
    @staticmethod
    def sanitize_text_input(text):
        if not isinstance(text, str):
            return ""
        
        sanitized = re.sub(r'[<>"\'\\]', "", text)
        return sanitized[:10000]
    
    @staticmethod
    def parse_content_and_roles(content):
        segments = []
        roles = set()
        lines = content.split("\n")
        current_role = None
        current_text = []

        for line in lines:
            role_match = re.match(r"^\s*\*\*(.*?)\*\*", line)
            if role_match:
                if current_role and current_text:
                    segment = {
                        "role": current_role,
                        "text": " ".join(current_text).strip(),
                    }
                    segments.append(segment)

                current_role = role_match.group(1).strip()
                roles.add(current_role)
                text_after_role = line[role_match.end():].strip()
                current_text = [text_after_role] if text_after_role else []
            elif line.strip() and current_role:
                current_text.append(line.strip())

        if current_role and current_text:
            final_segment = {
                "role": current_role,
                "text": " ".join(current_text).strip(),
            }
            segments.append(final_segment)

        return segments, list(roles)