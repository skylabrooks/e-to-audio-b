# 🎭 EtoAudioBook - Multi-Voice Audiobook Generator

Transform your stories into immersive audiobooks with multiple AI voices! EtoAudioBook uses Google Cloud Text-to-Speech to create engaging audiobooks where different characters have different voices.

## ✨ Features

- 📖 **Multi-Format Support**: Upload `.md` or `.txt` files
- 🎭 **Character Detection**: Automatically detects speaker roles from your content
- 🗣️ **Voice Assignment**: Assign different Google Cloud TTS voices to each character
- 🎵 **Audio Generation**: Creates high-quality MP3 audiobook segments
- 🎧 **Interactive Player**: Play your generated audiobook with segment navigation
- 🌐 **Modern UI**: Clean, responsive React interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Cloud Project with Text-to-Speech API enabled

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd EtoAudioBook
```

### 2. Automated Setup (Windows)
```bash
deploy-local.bat
```

### 3. Manual Setup

#### Backend Setup
```bash
cd Backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd Frontend
npm install
```

### 4. Google Cloud Configuration

1. Create a Google Cloud Project
2. Enable the Text-to-Speech API
3. Create a Service Account with TTS permissions
4. Download the service account JSON key
5. Copy `Backend/credentials_template.py` to `Backend/credentials.py`
6. Add your credentials to `credentials.py`

### 5. Run the Application

#### Terminal 1 - Backend
```bash
cd Backend
venv\Scripts\activate
python app.py
```

#### Terminal 2 - Frontend  
```bash
cd Frontend
npm start
```

### 6. Open Your Browser
Navigate to `http://localhost:3000`

## 🎬 Demo Instructions

### Sample Content Format
Your story should use this markdown format:
~~~
**Narrator:** Once upon a time in a magical kingdom...

**Princess:** Help me, brave knight!

**Knight:** I shall save you, Princess!

**Dragon:** ROAAAAR! None shall pass!
~~~

### Demo Flow
1. **Upload** the provided `demo-story.md` file
2. **Assign Voices** to each detected character
3. **Generate** your multi-voice audiobook
4. **Play** and enjoy your creation!

## 🏗️ Architecture

```
EtoAudioBook/
├── Frontend/          # React.js application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.js        # Main application
│   │   └── App.css       # Styling
│   └── package.json
├── Backend/           # Flask API server
│   ├── app.py            # Main Flask application
│   ├── credentials.py    # Google Cloud credentials
│   └── requirements.txt
└── demo-story.md      # Sample story for testing
```

## 🔧 API Endpoints

- `GET /api/voices` - List available TTS voices
- `POST /api/detect-roles` - Extract character roles from uploaded file
- `POST /api/synthesize` - Generate audio for text segments

## 🎯 Key Components

### Frontend Components
- **FileUploader**: Handles file upload and validation
- **RoleAssignment**: Maps characters to TTS voices  
- **AudioPlayer**: Plays generated audiobook segments
- **TestVoices**: Displays available voices for testing

### Backend Features
- **Role Detection**: Extracts speaker roles using regex patterns
- **Content Parsing**: Segments content by character dialogue
- **Voice Synthesis**: Converts text to speech using Google Cloud TTS
- **Audio Encoding**: Returns base64-encoded MP3 audio

## 🚀 Deployment Options

### Local Development
Use the provided batch scripts for quick local setup.

### Cloud Deployment
- **Frontend**: Deploy to Netlify, Vercel, or GitHub Pages
- **Backend**: Deploy to Google Cloud Run, Heroku, or AWS
- **Environment**: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Docker Deployment
```dockerfile
# Example Dockerfile for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔍 Troubleshooting

### Common Issues

**Backend not starting?**
- Check Python version (3.8+ required)
- Verify Google Cloud credentials
- Ensure Text-to-Speech API is enabled

**Frontend not loading?**
- Check Node.js version (16+ required)
- Run `npm install` in Frontend directory
- Verify backend is running on port 5000

**Voice API errors?**
- Verify Google Cloud project setup
- Check service account permissions
- Ensure billing is enabled on your GCP project

**Audio not playing?**
- Check browser console for errors
- Verify MP3 support in your browser
- Check network connectivity to backend

## 📊 Performance Tips

- **Caching**: Voice lists are cached to reduce API calls
- **Compression**: Audio files are base64 encoded for web delivery
- **Error Handling**: Graceful fallbacks for network issues
- **Loading States**: User feedback during processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Cloud Text-to-Speech API
- React.js community
- Flask framework
- All contributors and testers

---

**Ready to create your first multi-voice audiobook? Upload `demo-story.md` and start experimenting!** 🎭🎵
