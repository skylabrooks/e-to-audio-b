#!/bin/bash
# EtoAudioBook Setup Script

set -e  # Exit on any error

echo "🚀 Setting up EtoAudioBook project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "Backend" ] || [ ! -d "Frontend" ]; then
    print_error "Please run this script from the EtoAudioBook project root directory"
    exit 1
fi

# Fix PATH issue for local bin
print_status "Fixing PATH for local Python packages..."
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Check if .env exists, if not create from template
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file and add your API keys!"
    else
        print_status "Creating basic .env file..."
        cat > .env << EOF
# LLM API Keys - Add your actual keys here
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
BRAVE_API_KEY=your-brave-api-key-here

# Google Cloud Credentials (for TTS)
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=true
REACT_APP_API_URL=http://localhost:5000
EOF
        print_warning "Created .env file - please add your actual API keys!"
    fi
else
    print_success ".env file already exists"
fi

# Backend setup
print_status "Setting up Python backend..."
cd Backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

if [ -f "requirements-dev.txt" ]; then
    print_status "Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

cd ..

# Frontend setup
print_status "Setting up React frontend..."
cd Frontend

# Install Node.js dependencies
if [ -f "package.json" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
else
    print_warning "No package.json found in Frontend directory"
fi

cd ..

# Install pre-commit hooks if available
if command -v pre-commit >/dev/null 2>&1; then
    print_status "Installing pre-commit hooks..."
    pre-commit install
else
    print_warning "pre-commit not found in PATH, skipping hooks installation"
    print_status "You can install it later with: pip install pre-commit && pre-commit install"
fi

# Create basic run scripts
print_status "Creating run scripts..."

# Backend run script
cat > run-backend.sh << 'EOF'
#!/bin/bash
echo "Starting Flask backend server..."
cd Backend
source venv/bin/activate
python app.py
EOF
chmod +x run-backend.sh

# Frontend run script
cat > run-frontend.sh << 'EOF'
#!/bin/bash
echo "Starting React frontend server..."
cd Frontend
npm start
EOF
chmod +x run-frontend.sh

# Combined run script
cat > run-all.sh << 'EOF'
#!/bin/bash
echo "Starting both backend and frontend servers..."
echo "Backend will run on http://localhost:5000"
echo "Frontend will run on http://localhost:3000"
echo "Press Ctrl+C to stop both servers"

# Function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}
trap cleanup INT

# Start backend in background
cd Backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
cd Frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
EOF
chmod +x run-all.sh

print_success "Setup complete!"
print_status "Available commands:"
echo "  ./run-backend.sh  - Start Flask backend server"
echo "  ./run-frontend.sh - Start React frontend server"
echo "  ./run-all.sh      - Start both servers"
echo ""
print_warning "Don't forget to:"
echo "  1. Edit .env file with your actual API keys"
echo "  2. Source your bashrc: source ~/.bashrc"
echo "  3. Test the setup: ./run-backend.sh"
echo ""
print_success "🎉 EtoAudioBook setup is ready!"