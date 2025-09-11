#!/bin/bash
# Quick commands for EtoAudioBook development

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_help() {
    echo -e "${BLUE}EtoAudioBook Quick Commands:${NC}"
    echo ""
    echo "Setup:"
    echo "  ./quick-commands.sh setup     - Complete project setup"
    echo "  ./quick-commands.sh env       - Check environment variables"
    echo ""
    echo "Development:"
    echo "  ./quick-commands.sh backend   - Start backend server"
    echo "  ./quick-commands.sh frontend  - Start frontend server"
    echo "  ./quick-commands.sh both      - Start both servers"
    echo ""
    echo "Code Quality:"
    echo "  ./quick-commands.sh lint      - Run all linters"
    echo "  ./quick-commands.sh format    - Format all code"
    echo "  ./quick-commands.sh test      - Run all tests"
    echo ""
    echo "Utilities:"
    echo "  ./quick-commands.sh clean     - Clean build artifacts"
    echo "  ./quick-commands.sh install   - Install dependencies"
    echo "  ./quick-commands.sh path      - Fix PATH issues"
}

fix_path() {
    echo -e "${BLUE}Fixing PATH for local Python packages...${NC}"
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo -e "${GREEN}PATH updated. Run: source ~/.bashrc${NC}"
}

setup_project() {
    echo -e "${BLUE}Setting up EtoAudioBook project...${NC}"
    
    # Fix PATH first
    export PATH="$HOME/.local/bin:$PATH"
    
    # Create .env if it doesn't exist
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${YELLOW}Created .env from template - please add your API keys!${NC}"
        fi
    fi
    
    # Backend setup
    echo "Setting up Backend..."
    cd Backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install --upgrade pip
    [ -f "requirements.txt" ] && pip install -r requirements.txt
    [ -f "requirements-dev.txt" ] && pip install -r requirements-dev.txt
    cd ..
    
    # Frontend setup
    echo "Setting up Frontend..."
    cd Frontend
    [ -f "package.json" ] && npm install
    cd ..
    
    echo -e "${GREEN}Setup complete!${NC}"
}

run_backend() {
    echo -e "${BLUE}Starting Flask backend server...${NC}"
    cd Backend
    source venv/bin/activate
    python app.py
}

run_frontend() {
    echo -e "${BLUE}Starting React frontend server...${NC}"
    cd Frontend
    npm start
}

run_both() {
    echo -e "${BLUE}Starting both servers...${NC}"
    echo "Backend: http://localhost:5000"
    echo "Frontend: http://localhost:3000"
    
    # Start backend in background
    cd Backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    cd ..
    
    sleep 3
    
    # Start frontend
    cd Frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    # Cleanup function
    cleanup() {
        echo "Stopping servers..."
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
        exit
    }
    trap cleanup INT
    
    wait $BACKEND_PID $FRONTEND_PID
}

run_lint() {
    echo -e "${BLUE}Running linters...${NC}"
    
    # Backend linting
    echo "Linting Backend..."
    cd Backend
    source venv/bin/activate
    flake8 . || true
    cd ..
    
    # Frontend linting
    echo "Linting Frontend..."
    cd Frontend
    npm run lint || true
    cd ..
}

run_format() {
    echo -e "${BLUE}Formatting code...${NC}"
    
    # Backend formatting
    echo "Formatting Backend..."
    cd Backend
    source venv/bin/activate
    black . || true
    isort . || true
    cd ..
    
    # Frontend formatting
    echo "Formatting Frontend..."
    cd Frontend
    npm run format || true
    cd ..
}

run_tests() {
    echo -e "${BLUE}Running tests...${NC}"
    
    # Backend tests
    echo "Running Backend tests..."
    cd Backend
    source venv/bin/activate
    pytest || true
    cd ..
    
    # Frontend tests
    echo "Running Frontend tests..."
    cd Frontend
    npm test -- --coverage --watchAll=false || true
    cd ..
}

clean_project() {
    echo -e "${BLUE}Cleaning build artifacts...${NC}"
    rm -rf Frontend/build/
    rm -rf Backend/__pycache__/
    rm -rf Backend/.pytest_cache/
    rm -rf Backend/htmlcov/
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    echo -e "${GREEN}Cleanup complete!${NC}"
}

install_deps() {
    echo -e "${BLUE}Installing dependencies...${NC}"
    
    # Backend
    cd Backend
    source venv/bin/activate
    pip install -r requirements.txt
    [ -f "requirements-dev.txt" ] && pip install -r requirements-dev.txt
    cd ..
    
    # Frontend
    cd Frontend
    npm install
    cd ..
    
    echo -e "${GREEN}Dependencies installed!${NC}"
}

check_env() {
    echo -e "${BLUE}Checking environment variables...${NC}"
    
    if [ -f ".env" ]; then
        echo -e "${GREEN}.env file exists${NC}"
        
        # Check for required variables
        if grep -q "GEMINI_API_KEY=" .env; then
            if grep -q "GEMINI_API_KEY=your-" .env; then
                echo -e "${YELLOW}GEMINI_API_KEY: Template value (needs updating)${NC}"
            else
                echo -e "${GREEN}GEMINI_API_KEY: Set${NC}"
            fi
        else
            echo -e "${YELLOW}GEMINI_API_KEY: Missing${NC}"
        fi
        
        if grep -q "OPENAI_API_KEY=" .env; then
            if grep -q "OPENAI_API_KEY=your-" .env; then
                echo -e "${YELLOW}OPENAI_API_KEY: Template value (needs updating)${NC}"
            else
                echo -e "${GREEN}OPENAI_API_KEY: Set${NC}"
            fi
        else
            echo -e "${YELLOW}OPENAI_API_KEY: Missing${NC}"
        fi
        
    else
        echo -e "${YELLOW}.env file missing - run './quick-commands.sh setup'${NC}"
    fi
}

# Main command dispatcher
case "$1" in
    "setup")
        setup_project
        ;;
    "backend")
        run_backend
        ;;
    "frontend")
        run_frontend
        ;;
    "both")
        run_both
        ;;
    "lint")
        run_lint
        ;;
    "format")
        run_format
        ;;
    "test")
        run_tests
        ;;
    "clean")
        clean_project
        ;;
    "install")
        install_deps
        ;;
    "env")
        check_env
        ;;
    "path")
        fix_path
        ;;
    *)
        print_help
        ;;
esac