# EtoAudioBook Setup Instructions

## 🚨 Quick Fix for Current Issues

You're experiencing PATH issues and missing files. Here's how to fix them:

### 1. Fix PATH Issue (Immediate)
```bash
# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Now pre-commit should work
pre-commit --version
```

### 2. Save Working Set Files
The rule files are in the working set but not yet saved to your repository. You need to:
1. **Save all files** from the working set to your repository
2. The files should appear in your actual project directory

### 3. Use Quick Commands (Alternative to Makefile)
Since the Makefile isn't available yet, use these scripts:

```bash
# Make scripts executable
chmod +x setup.sh quick-commands.sh

# Complete setup
./setup.sh

# Or use quick commands
./quick-commands.sh setup
```

## 📋 Available Commands

### Setup Commands
```bash
./quick-commands.sh setup     # Complete project setup
./quick-commands.sh env       # Check environment variables
./quick-commands.sh path      # Fix PATH issues
```

### Development Commands
```bash
./quick-commands.sh backend   # Start Flask backend
./quick-commands.sh frontend  # Start React frontend  
./quick-commands.sh both      # Start both servers
```

### Code Quality Commands
```bash
./quick-commands.sh lint      # Run all linters
./quick-commands.sh format    # Format all code
./quick-commands.sh test      # Run all tests
```

### Utility Commands
```bash
./quick-commands.sh clean     # Clean build artifacts
./quick-commands.sh install   # Install dependencies
```

## 🔧 Manual Setup Steps

If scripts don't work, here's the manual process:

### 1. Backend Setup
```bash
cd Backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if available

cd ..
```

### 2. Frontend Setup
```bash
cd Frontend

# Install Node.js dependencies
npm install

cd ..
```

### 3. Environment Configuration
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 4. Pre-commit Setup
```bash
# Install pre-commit (with fixed PATH)
export PATH="$HOME/.local/bin:$PATH"
pip install pre-commit
pre-commit install
```

## 🚀 Running the Application

### Start Backend Only
```bash
cd Backend
source venv/bin/activate
python app.py
```

### Start Frontend Only
```bash
cd Frontend
npm start
```

### Start Both (Manual)
```bash
# Terminal 1 - Backend
cd Backend && source venv/bin/activate && python app.py

# Terminal 2 - Frontend  
cd Frontend && npm start
```

## 🐛 Troubleshooting

### PATH Issues
```bash
# Check if tools are installed
which pre-commit
which black
which flake8

# If not found, add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Missing Files
If you see "No rule to make target" errors:
1. Save all working set files to repository
2. Check files exist: `ls -la Makefile`
3. Use quick-commands.sh as alternative

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf Backend/venv
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node.js Issues
```bash
# Clear npm cache
cd Frontend
rm -rf node_modules package-lock.json
npm install
```

## 📁 Expected File Structure

After setup, you should have:
```
EtoAudioBook/
├── .env                    # Your API keys
├── .env.example           # Template
├── Makefile              # Build commands
├── setup.sh              # Setup script
├── quick-commands.sh     # Alternative commands
├── Backend/
│   ├── venv/             # Python virtual environment
│   ├── requirements.txt  # Python dependencies
│   └── app.py           # Flask application
├── Frontend/
│   ├── node_modules/     # Node.js dependencies
│   ├── package.json      # Node.js configuration
│   └── src/             # React source code
└── [rule files...]       # All the configuration files
```

## ✅ Verification Steps

1. **Check PATH**: `echo $PATH` should include `$HOME/.local/bin`
2. **Check tools**: `pre-commit --version`, `black --version`
3. **Check files**: `ls -la Makefile setup.sh quick-commands.sh`
4. **Check .env**: `cat .env` should show your API keys
5. **Test backend**: `cd Backend && source venv/bin/activate && python -c "import flask; print('OK')"`
6. **Test frontend**: `cd Frontend && npm list react`

## 🆘 Need Help?

If you're still having issues:
1. **Save working set files first** - this is the most important step
2. Run `./quick-commands.sh setup` for automated setup
3. Check each step manually if automation fails
4. Verify all files are in the correct locations

The rule files setup is comprehensive and will work great once the files are saved to your repository! 🚀