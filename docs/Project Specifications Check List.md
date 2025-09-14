# **1.0 Overview**

This document outlines the features and user flow for the AI Audiobook Generator, an application designed to transform text-based scripts into high-definition, multi-character audiobooks. The application leverages a vast library of AI-generated voices to provide a rich, immersive listening experience. This specification details critical enhancements focused on user control, editing, and previewing capabilities.

## **2.0 Core User Flow**

The user journey is designed to be intuitive, guiding the user from script upload to final audiobook generation with clear, actionable steps.

1. **State: AwaitingUpload**  
   * A primary call-to-action instructs the user to upload their script (.md or .txt file) via a drag-and-drop zone or a file selector.  
2. **State: ProcessingScript**  
   * Upon upload, the application backend parses the script.  
   * **Action:** The system automatically detects unique character names (e.g., by identifying lines formatted as CHARACTER: followed by dialogue).  
   * The UI displays a loading indicator while processing.  
3. **State: VoiceAssignment**  
   * The UI presents a list of all auto-detected characters.  
   * For each character, the user is prompted to assign a voice from the library.  
   * The voice library UI should be a modal or drawer containing:  
     * Over 1600+ voices across 20+ languages.  
     * **Search Functionality:** Filter voices by name, language, gender, accent, or style (e.g., "deep," "youthful").

# The user assigns a voice to each character and confirms their selections.  **Project Specification:**

# 

# \#\# 1.0 Overview

# 

# This document outlines the features and user flow for the AI Audiobook Generator, an application designed to transform text-based scripts into high-definition, multi-character audiobooks. The application leverages a vast library of AI-generated voices to provide a rich, immersive listening experience. This specification details critical enhancements focused on user control, editing, and previewing capabilities.

# 

# \#\# 2.0 Core User Flow

# 

# The user journey is designed to be intuitive, guiding the user from script upload to final audiobook generation with clear, actionable steps.

# 

# 1\.  \*\*State: AwaitingUpload\*\*

#     \- \[x\] A primary call-to-action instructs the user to upload their script (.md or .txt file) via a drag-and-drop zone or a file selector.

# 2\.  \*\*State: ProcessingScript\*\*

#     \- \[ \] Upon upload, the application backend parses the script. *(Access to Google’s DOC AI API)*

#     \- \[ \] \*\*Action:\*\* The system automatically detects unique character names (e.g., by identifying lines formatted as CHARACTER: followed by dialogue).

#     \- \[ \] The UI displays a loading indicator while processing.

# 3\.  \*\*State: VoiceAssignment\*\*

#     \- \[x\] The UI presents a list of all auto-detected characters.

#     \- \[x\] For each character, the user is prompted to assign a voice from the library.

#     \- \[x\] The voice library UI should be a modal or drawer containing:

#         \- \[x\] Over 1600+ voices across 20+ languages.

#         \- \[ \] \*\*Search Functionality:\*\* Filter voices by name, language, gender, accent, or style (e.g., "deep," "youthful").

#     \- \[x\] The user assigns a voice to each character and confirms their selections.

# 4\.  \*\*State: DocumentPreview (NEW FEATURE)\*\*

#     \- \[ \] After assigning voices, the user is taken to a new preview and editing screen.

#     \- \[ \] This state is critical for verification and fine-tuning before generation. (See section 3.2 for details).

# 5\.  \*\*State: Generation (NEW FEATURE)\*\*

#     \- \[ \] The user chooses their preferred audio generation method:

#         \- \[ \] \*\*Batch Mode:\*\* Convert the entire script at once.

#         \- \[ \] \*\*Interactive Mode:\*\* Generate and review audio line-by-line.

#     \- \[  The UI transitions to reflect the chosen generation process.

# 6\.  \*\*State: Completed\*\*

#     \- \[ \] The application presents the final generated HD audio file(s).

#     \- \[ \] The user can play the audio within the app and download the final product.

# 

# \#\# 3.0 Feature Enhancements & Specifications

# 

# These features are designed to give the user granular control over the final output.

# 

# \#\#\# 3.1 Character & Dialogue Detection Logic

# 

# \- \[ \] \*\*Input:\*\* A string containing the full script content.

# \- \[ \] \*\*Process:\*\* The backend should implement a robust parser to identify character dialogue. A primary strategy is to detect lines matching patterns like:

#     \- \[ \] CHARACTER NAME:

#     \- \[ \] Character Name:

#     \- \[ \] (Character Name)

# \- \[ \] \*\*Output:\*\* A JSON object representing the structured script, including a list of unique character names.

# 

# \`\`\`json

# {

#   "characters": \["NARRATOR", "ARTHUR", "ZAPHOD"\],

#   "script\_lines": \[

#     { "line": 1, "character": "NARRATOR", "dialogue": "The story so far..." },

#     { "line": 2, "character": "ARTHUR", "dialogue": "What's that?" }

#   \]

# }

# 3.2 Document Preview & Editing Pane

# 

# This is a new, crucial screen in the user flow.

* **User Story:** "As a writer, I need to review my script and my voice assignments together, so I can catch errors and confirm my choices before committing to the final audio generation."  
* **UI Components:**  
  * **Editable Text Area:** Displays the full script. The user can make final textual edits here (fix typos, alter words).  
  * **Voice Assignment Display:** For each line of dialogue, display the assigned character's name.  
  * **Inline Voice Previewer:**  
    * Next to each dialogue line, place a "play" or "speaker" icon.  
    * When clicked, this icon triggers a **generic, pre-recorded demo** of the assigned voice (e.g., the voice actor saying, "This is the voice you've selected"). This confirms the *voice itself* and its correct assignment.  
    * This action **does not** generate the actual script line; it only plays a demo sample to prevent unnecessary API calls.

3.3 Dual Generation Modes

# 

# The user must be able to choose how they want to proceed after the preview stage.3.3.1 Batch Generation

* **User Story:** "When I'm confident in my script and voice choices, I want to generate the entire audiobook in one go and be notified when it's done."  
* **UI:** A primary button labeled **"Generate Full Audiobook"**.  
* **Process:**  
  * The application sends the full script content and the final voice assignment map to the backend.  
  * The UI shows a non-blocking progress bar or status update (e.g., "Generating... 25% complete").

3.3.2 Interactive (Line-by-Line) Generation

* **User Story:** "As a director, I want to approve each line's audio individually, with the ability to tweak the script or change a voice actor on the fly, and also adjust the pitch, tone, and speed of the voice actor's audio anytime to get the perfect performance."  
* **UI:** A secondary button labeled **"Review Line-by-Line"**.  
* **Process:**  
  * The interface highlights the first line of dialogue in the script.  
  * The UI displays a contextual control panel for the highlighted line with the following options:  
    * **Generate Audio**: Calls the TTS API for *only the highlighted line*.  
    * **Play/Pause**: Controls playback of the newly generated audio.  
    * **Accept & Next**: Approves the audio and automatically highlights the next dialogue line.  
    * **Change Voice**: Opens the voice library modal to re-assign a voice actor for this character.  
    * **Edit Script**: Allows the user to modify the text of the current line before generation.  
  * A global button, **"Generate Remaining Script"**, must be visible at all times during this mode, allowing the user to seamlessly switch to Batch Mode from their current position.

4.0 API & Data Model Considerations

# 

# The frontend and backend will communicate using a clear data structure.

* **Voice Assignment Payload:**

# {

#   "script\_id": "unique\_script\_identifier",

#   "assignments": \[

#     { "character": "NARRATOR", "voice\_id": "en-us-voice-123" },

#     { "character": "ARTHUR", "voice\_id": "en-gb-voice-456" },

#     { "character": "ZAPHOD", "voice\_id": "en-us-voice-789" }

#   \]

}

* **Line Generation Request (Interactive Mode):**

# {

#   "line\_id": 1,

#   "character": "ARTHUR",

#   "dialogue": "What's that?",

#   "voice\_id": "en-gb-voice-456"

}

# 

*   
4. **State: DocumentPreview (NEW FEATURE)**  
   * After assigning voices, the user is taken to a new preview and editing screen.  
   * This state is critical for verification and fine-tuning before generation. (See section 3.2 for details).  
5. **State: Generation (NEW FEATURE)**  
   * The user chooses their preferred audio generation method:  
     * **Batch Mode:** Convert the entire script at once.  
     * **Interactive Mode:** Generate and review audio line-by-line.  
   * The UI transitions to reflect the chosen generation process.  
6. **State: Completed**  
   * The application presents the final generated HD audio file(s).  
   * The user can play the audio within the app and download the final product.

## **3.0 Feature Enhancements & Specifications**

These features are designed to give the user granular control over the final output.

### **3.1 Character & Dialogue Detection Logic**

* **Input:** A string containing the full script content.  
* **Process:** The backend should implement a robust parser to identify character dialogue. A primary strategy is to detect lines matching patterns like:  
  * CHARACTER NAME:  
  * Character Name:  
  * (Character Name)  
* **Output:** A JSON object representing the structured script, including a list of unique character names.  
  {  
    "characters": \["NARRATOR", "ARTHUR", "ZAPHOD"\],  
    "script\_lines": \[  
      { "line": 1, "character": "NARRATOR", "dialogue": "The story so far..." },  
      { "line": 2, "character": "ARTHUR", "dialogue": "What's that?" }  
    \]  
  }

### **3.2 Document Preview & Editing Pane**

This is a new, crucial screen in the user flow.

* **User Story:** "As a writer, I need to review my script and my voice assignments together, so I can catch errors and confirm my choices before committing to the final audio generation."  
* **UI Components:**  
  1. **Editable Text Area:** Displays the full script. The user can make final textual edits here (fix typos, alter words).  
  2. **Voice Assignment Display:** For each line of dialogue, display the assigned character's name.  
  3. **Inline Voice Previewer:**  
     * Next to each dialogue line, place a "play" or "speaker" icon.  
     * When clicked, this icon triggers a **generic, pre-recorded demo** of the assigned voice (e.g., the voice actor saying, "This is the voice you've selected"). This confirms the *voice itself* and its correct assignment.  
     * This action **does not** generate the actual script line; it only plays a demo sample to prevent unnecessary API calls.

### **3.3 Dual Generation Modes**

The user must be able to choose how they want to proceed after the preview stage.

#### **3.3.1 Batch Generation**

* **User Story:** "When I'm confident in my script and voice choices, I want to generate the entire audiobook in one go and be notified when it's done."  
* **UI:** A primary button labeled **"Generate Full Audiobook"**.  
* **Process:**  
  1. The application sends the full script content and the final voice assignment map to the backend.  
  2. The UI shows a non-blocking progress bar or status update (e.g., "Generating... 25% complete").

#### **3.3.2 Interactive (Line-by-Line) Generation**

* **User Story:** "As a director, I want to approve each line's audio individually, with the ability to tweak the script or change a voice actor on the fly to get the perfect performance."  
* **UI:** A secondary button labeled **"Review Line-by-Line"**.  
* **Process:**  
  1. The interface highlights the first line of dialogue in the script.  
  2. The UI displays a contextual control panel for the highlighted line with the following options:  
     * **Generate Audio**: Calls the TTS API for *only the highlighted line*.  
     * **Play/Pause**: Controls playback of the newly generated audio.  
     * **Accept & Next**: Approves the audio and automatically highlights the next dialogue line.  
     * **Change Voice**: Opens the voice library modal to re-assign a voice actor for this character.  
     * **Edit Script**: Allows the user to modify the text of the current line before generation.  
  3. A global button, **"Generate Remaining Script"**, must be visible at all times during this mode, allowing the user to seamlessly switch to Batch Mode from their current position.

## **4.0 API & Data Model Considerations**

The frontend and backend will communicate using a clear data structure.

* **Voice Assignment Payload:**  
  {  
    "script\_id": "unique\_script\_identifier",  
    "assignments": \[  
      { "character": "NARRATOR", "voice\_id": "en-us-voice-123" },  
      { "character": "ARTHUR", "voice\_id": "en-gb-voice-456" },  
      { "character": "ZAPHOD", "voice\_id": "en-us-voice-789" }  
    \]  
  }

* **Line Generation Request (Interactive Mode):**  
  {  
    "line\_id": 1,  
    "character": "ARTHUR",  
    "dialogue": "What's that?",  
    "voice\_id": "en-gb-voice-456"  
  }

# **Project Specification: I am unable to create a downloadable Markdown file directly. However, you can copy the text below and paste it into a file on your computer with a** `.md` extension.

# \# Project Specification: AI Audiobook Generator

# 

# \#\# 1.0 Overview

# 

# This document outlines the features and user flow for the AI Audiobook Generator, an application designed to transform text-based scripts into high-definition, multi-character audiobooks. The application leverages a vast library of AI-generated voices to provide a rich, immersive listening experience. This specification details critical enhancements focused on user control, editing, and previewing capabilities.

# 

# \#\# 2.0 Core User Flow

# 

# The user journey is designed to be intuitive, guiding the user from script upload to final audiobook generation with clear, actionable steps.

# 

# 1\.  \*\*State: AwaitingUpload\*\*

#     \- \[x\] A primary call-to-action instructs the user to upload their script (.md or .txt file) via a drag-and-drop zone or a file selector.

# 2\.  \*\*State: ProcessingScript\*\*

#     \- \[ \] Upon upload, the application backend parses the script.

#     \- \[ \] \*\*Action:\*\* The system automatically detects unique character names (e.g., by identifying lines formatted as CHARACTER: followed by dialogue).

#     \- \[ \] The UI displays a loading indicator while processing.

# 3\.  \*\*State: VoiceAssignment\*\*

#     \- \[x\] The UI presents a list of all auto-detected characters.

#     \- \[x\] For each character, the user is prompted to assign a voice from the library.

#     \- \[x\] The voice library UI should be a modal or drawer containing:

#         \- \[x\] Over 1600+ voices across 20+ languages.

#         \- \[ \] \*\*Search Functionality:\*\* Filter voices by name, language, gender, accent, or style (e.g., "deep," "youthful").

#     \- \[x\] The user assigns a voice to each character and confirms their selections.

# 4\.  \*\*State: DocumentPreview (NEW FEATURE)\*\*

#     \- \[ \] After assigning voices, the user is taken to a new preview and editing screen.

#     \- \[ \] This state is critical for verification and fine-tuning before generation. (See section 3.2 for details).

# 5\.  \*\*State: Generation (NEW FEATURE)\*\*

#     \- \[ \] The user chooses their preferred audio generation method:

#         \- \[ \] \*\*Batch Mode:\*\* Convert the entire script at once.

#         \- \[ \] \*\*Interactive Mode:\*\* Generate and review audio line-by-line.

#     \- \[  The UI transitions to reflect the chosen generation process.

# 6\.  \*\*State: Completed\*\*

#     \- \[ \] The application presents the final generated HD audio file(s).

#     \- \[ \] The user can play the audio within the app and download the final product.

# 

# \#\# 3.0 Feature Enhancements & Specifications

# 

# These features are designed to give the user granular control over the final output.

# 

# \#\#\# 3.1 Character & Dialogue Detection Logic

# 

# \- \[ \] \*\*Input:\*\* A string containing the full script content.

# \- \[ \] \*\*Process:\*\* The backend should implement a robust parser to identify character dialogue. A primary strategy is to detect lines matching patterns like:

#     \- \[ \] CHARACTER NAME:

#     \- \[ \] Character Name:

#     \- \[ \] (Character Name)

# \- \[ \] \*\*Output:\*\* A JSON object representing the structured script, including a list of unique character names.

# 

# \`\`\`json

# {

#   "characters": \["NARRATOR", "ARTHUR", "ZAPHOD"\],

#   "script\_lines": \[

#     { "line": 1, "character": "NARRATOR", "dialogue": "The story so far..." },

#     { "line": 2, "character": "ARTHUR", "dialogue": "What's that?" }

#   \]

# }

# 3.2 Document Preview & Editing Pane

# 

# This is a new, crucial screen in the user flow.

* **User Story:** "As a writer, I need to review my script and my voice assignments together, so I can catch errors and confirm my choices before committing to the final audio generation."  
* **UI Components:**  
  * **Editable Text Area:** Displays the full script. The user can make final textual edits here (fix typos, alter words).  
  * **Voice Assignment Display:** For each line of dialogue, display the assigned character's name.  
  * **Inline Voice Previewer:**  
    * Next to each dialogue line, place a "play" or "speaker" icon.  
    * When clicked, this icon triggers a **generic, pre-recorded demo** of the assigned voice (e.g., the voice actor saying, "This is the voice you've selected"). This confirms the *voice itself* and its correct assignment.  
    * This action **does not** generate the actual script line; it only plays a demo sample to prevent unnecessary API calls.

3.3 Dual Generation Modes

# 

# The user must be able to choose how they want to proceed after the preview stage.3.3.1 Batch Generation

* **User Story:** "When I'm confident in my script and voice choices, I want to generate the entire audiobook in one go and be notified when it's done."  
* **UI:** A primary button labeled **"Generate Full Audiobook"**.  
* **Process:**  
  * The application sends the full script content and the final voice assignment map to the backend.  
  * The UI shows a non-blocking progress bar or status update (e.g., "Generating... 25% complete").

3.3.2 Interactive (Line-by-Line) Generation

* **User Story:** "As a director, I want to approve each line's audio individually, with the ability to tweak the script or change a voice actor on the fly, and also adjust the pitch, tone, and speed of the voice actor's audio anytime to get the perfect performance."  
* **UI:** A secondary button labeled **"Review Line-by-Line"**.  
* **Process:**  
  * The interface highlights the first line of dialogue in the script.  
  * The UI displays a contextual control panel for the highlighted line with the following options:  
    * **Generate Audio**: Calls the TTS API for *only the highlighted line*.  
    * **Play/Pause**: Controls playback of the newly generated audio.  
    * **Accept & Next**: Approves the audio and automatically highlights the next dialogue line.  
    * **Change Voice**: Opens the voice library modal to re-assign a voice actor for this character.  
    * **Edit Script**: Allows the user to modify the text of the current line before generation.  
  * A global button, **"Generate Remaining Script"**, must be visible at all times during this mode, allowing the user to seamlessly switch to Batch Mode from their current position.

4.0 API & Data Model Considerations

# 

# The frontend and backend will communicate using a clear data structure.

* **Voice Assignment Payload:**

# {

#   "script\_id": "unique\_script\_identifier",

#   "assignments": \[

#     { "character": "NARRATOR", "voice\_id": "en-us-voice-123" },

#     { "character": "ARTHUR", "voice\_id": "en-gb-voice-456" },

#     { "character": "ZAPHOD", "voice\_id": "en-us-voice-789" }

#   \]

}

* **Line Generation Request (Interactive Mode):**

# {

#   "line\_id": 1,

#   "character": "ARTHUR",

#   "dialogue": "What's that?",

#   "voice\_id": "en-gb-voice-456"

}

# 

# **1.0 Overview**

This document outlines the features and user flow for the AI Audiobook Generator, an application designed to transform text-based scripts into high-definition, multi-character audiobooks. The application leverages a vast library of AI-generated voices to provide a rich, immersive listening experience. This specification details critical enhancements focused on user control, editing, and previewing capabilities.

## **2.0 Core User Flow**

The user journey is designed to be intuitive, guiding the user from script upload to final audiobook generation with clear, actionable steps.

1. **State: AwaitingUpload**  
   * A primary call-to-action instructs the user to upload their script (.md or .txt file) via a drag-and-drop zone or a file selector.  
2. **State: ProcessingScript**  
   * Upon upload, the application backend parses the script.  
   * **Action:** The system automatically detects unique character names (e.g., by identifying lines formatted as CHARACTER: followed by dialogue).  
   * The UI displays a loading indicator while processing.  
3. **State: VoiceAssignment**  
   * The UI presents a list of all auto-detected characters.  
   * For each character, the user is prompted to assign a voice from the library.  
   * The voice library UI should be a modal or drawer containing:  
     * Over 1600+ voices across 20+ languages.  
     * **Search Functionality:** Filter voices by name, language, gender, accent, or style (e.g., "deep," "youthful").  
   * The user assigns a voice to each character and confirms their selections.  
4. **State: DocumentPreview (NEW FEATURE)**  
   * After assigning voices, the user is taken to a new preview and editing screen.  
   * This state is critical for verification and fine-tuning before generation. (See section 3.2 for details).  
5. **State: Generation (NEW FEATURE)**  
   * The user chooses their preferred audio generation method:  
     * **Batch Mode:** Convert the entire script at once.  
     * **Interactive Mode:** Generate and review audio line-by-line.  
   * The UI transitions to reflect the chosen generation process.  
6. **State: Completed**  
   * The application presents the final generated HD audio file(s).  
   * The user can play the audio within the app and download the final product.

## **3.0 Feature Enhancements & Specifications**

These features are designed to give the user granular control over the final output.

### **3.1 Character & Dialogue Detection Logic**

* **Input:** A string containing the full script content.  
* **Process:** The backend should implement a robust parser to identify character dialogue. A primary strategy is to detect lines matching patterns like:  
  * CHARACTER NAME:  
  * Character Name:  
  * (Character Name)  
* **Output:** A JSON object representing the structured script, including a list of unique character names.  
  {  
    "characters": \["NARRATOR", "ARTHUR", "ZAPHOD"\],  
    "script\_lines": \[  
      { "line": 1, "character": "NARRATOR", "dialogue": "The story so far..." },  
      { "line": 2, "character": "ARTHUR", "dialogue": "What's that?" }  
    \]  
  }

### **3.2 Document Preview & Editing Pane**

This is a new, crucial screen in the user flow.

* **User Story:** "As a writer, I need to review my script and my voice assignments together, so I can catch errors and confirm my choices before committing to the final audio generation."  
* **UI Components:**  
  1. **Editable Text Area:** Displays the full script. The user can make final textual edits here (fix typos, alter words).  
  2. **Voice Assignment Display:** For each line of dialogue, display the assigned character's name.  
  3. **Inline Voice Previewer:**  
     * Next to each dialogue line, place a "play" or "speaker" icon.  
     * When clicked, this icon triggers a **generic, pre-recorded demo** of the assigned voice (e.g., the voice actor saying, "This is the voice you've selected"). This confirms the *voice itself* and its correct assignment.  
     * This action **does not** generate the actual script line; it only plays a demo sample to prevent unnecessary API calls.

### **3.3 Dual Generation Modes**

The user must be able to choose how they want to proceed after the preview stage.

#### **3.3.1 Batch Generation**

* **User Story:** "When I'm confident in my script and voice choices, I want to generate the entire audiobook in one go and be notified when it's done."  
* **UI:** A primary button labeled **"Generate Full Audiobook"**.  
* **Process:**  
  1. The application sends the full script content and the final voice assignment map to the backend.  
  2. The UI shows a non-blocking progress bar or status update (e.g., "Generating... 25% complete").

#### **3.3.2 Interactive (Line-by-Line) Generation**

* **User Story:** "As a director, I want to approve each line's audio individually, with the ability to tweak the script or change a voice actor on the fly to get the perfect performance."  
* **UI:** A secondary button labeled **"Review Line-by-Line"**.  
* **Process:**  
  1. The interface highlights the first line of dialogue in the script.  
  2. The UI displays a contextual control panel for the highlighted line with the following options:  
     * **Generate Audio**: Calls the TTS API for *only the highlighted line*.  
     * **Play/Pause**: Controls playback of the newly generated audio.  
     * **Accept & Next**: Approves the audio and automatically highlights the next dialogue line.  
     * **Change Voice**: Opens the voice library modal to re-assign a voice actor for this character.  
     * **Edit Script**: Allows the user to modify the text of the current line before generation.  
  3. A global button, **"Generate Remaining Script"**, must be visible at all times during this mode, allowing the user to seamlessly switch to Batch Mode from their current position.

## **4.0 API & Data Model Considerations**

The frontend and backend will communicate using a clear data structure.

* **Voice Assignment Payload:**  
  {  
    "script\_id": "unique\_script\_identifier",  
    "assignments": \[  
      { "character": "NARRATOR", "voice\_id": "en-us-voice-123" },  
      { "character": "ARTHUR", "voice\_id": "en-gb-voice-456" },  
      { "character": "ZAPHOD", "voice\_id": "en-us-voice-789" }  
    \]  
  }

* **Line Generation Request (Interactive Mode):**  
  {  
    "line\_id": 1,  
    "character": "ARTHUR",  
    "dialogue": "What's that?",  
    "voice\_id": "en-gb-voice-456"  
  }

