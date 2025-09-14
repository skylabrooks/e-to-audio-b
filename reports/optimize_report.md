# Optimization Agent Report (Dry-Run)

## Baseline timings
- frontend_build: exit=127 time=0.01s
- backend_pytest: exit=4 time=6.19s
- backend_mypy: exit=1 time=0.15s

## Frontend bundle sizes
- Total raw: 203.8 KB
- Total gzip: 63.8 KB
- Largest files:
  - build\static\js\main.dcb90688.js raw=199.5 KB gzip=62.1 KB
  - build\static\js\206.ed2f3d44.chunk.js raw=4.3 KB gzip=1.7 KB

## Frontend orphans (not reachable from entry)
- components\VoiceGallery\CharacterAvatar.jsx
- components\VoiceGallery\DemoButton.jsx
- components\VoiceGallery\FilterControls.jsx
- components\VoiceGallery\FilterDropdown.jsx
- components\VoiceGallery\PaginationControls.jsx
- components\VoiceGallery\SearchInput.jsx
- components\VoiceGallery\VoiceCard.jsx
- components\VoiceGallery\VoiceGallery.jsx
- components\VoiceGallery\VoiceGalleryHeader.jsx
- components\VoiceGallery\VoiceGrid.jsx
- components\VoiceGallery\VoiceStats.jsx
- components\VoiceGallery\VoiceTags.jsx
- components\__tests__\AudioPlayer.test.js
- components\__tests__\FileUploader.test.js
- components\icons\ClearIcon.jsx
- components\icons\FilterIcon.jsx
- components\icons\PauseIcon.jsx
- components\icons\PlayIcon.jsx
- components\icons\SearchIcon.jsx
- components\icons\StarIcon.jsx
- components\icons\UserIcon.jsx
- components\icons\VolumeIcon.jsx
- components\logo\LogoShowcase.jsx
- data\voiceGalleryMockData.js
- hooks\useCache.js
- hooks\useDebounce.js
- pages\App.VoiceGallery.jsx
- pages\App.test.js

## Backend unused imports (flake8 F401)
- None detected or flake8 unavailable

## Frontend linter unused hints
- None detected or ESLint clean

## Largest source files (potential split/optimize)
### Frontend/src
- components\TestVoices.js (14.3 KB)
- pages\App.js (11.8 KB)
- components\logo\LogoShowcase.jsx (7.0 KB)
- data\voiceGalleryMockData.js (6.1 KB)
- components\VoiceGallery\FilterControls.jsx (4.7 KB)
- components\VoiceGallery\VoiceGallery.jsx (4.6 KB)
- components\FileUploader.js (4.4 KB)
- pages\App.test.js (3.8 KB)
- components\logo\FlowIcon.jsx (3.7 KB)
- components\RoleAssignment.js (3.6 KB)
### Backend
- venv\Lib\site-packages\win32\lib\winerror.py (283.3 KB)
- venv\Lib\site-packages\idna\uts46data.py (233.7 KB)
- venv\Lib\site-packages\pip\_vendor\idna\uts46data.py (233.7 KB)
- venv\Lib\site-packages\redis\commands\core.py (218.3 KB)
- venv\Lib\site-packages\google\protobuf\descriptor_pb2.py (170.3 KB)
- venv\Lib\site-packages\openai\resources\chat\completions\completions.py (156.9 KB)
- venv\Lib\site-packages\typing_extensions.py (156.7 KB)
- venv\Lib\site-packages\openai\resources\responses\responses.py (155.7 KB)
- venv\Lib\site-packages\pygments\lexers\lisp.py (154.0 KB)
- venv\Lib\site-packages\openai\resources\beta\threads\runs\runs.py (151.7 KB)

## Suggested next actions (no changes applied)
- Remove unused imports flagged above (safe, local diffs)
- Consider deleting or moving orphan frontend files if truly unused
- Split or lazy-load largest frontend modules; review bundle report
- If you approve, the agent can auto-apply low-risk fixes in a PR-sized diff