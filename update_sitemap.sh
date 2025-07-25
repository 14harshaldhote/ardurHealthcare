#!/bin/bash

# Ardur Healthcare Sitemap Update Script
# This script generates a fresh static sitemap.xml file and optionally deploys it

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🗺️  Ardur Healthcare Sitemap Generator${NC}"
echo "=================================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
    exit 1
fi

# Check if the generator script exists
if [ ! -f "generate_sitemap_file.py" ]; then
    echo -e "${RED}❌ generate_sitemap_file.py not found${NC}"
    exit 1
fi

# Parse command line arguments
BACKUP=true
DEPLOY=false
OUTPUT_FILE="sitemap.xml"
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-backup)
            BACKUP=false
            shift
            ;;
        --deploy)
            DEPLOY=true
            shift
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --quiet|-q)
            QUIET=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --no-backup    Don't create backup of existing sitemap"
            echo "  --deploy       Copy sitemap to static directory"
            echo "  --output FILE  Specify output filename (default: sitemap.xml)"
            echo "  --quiet, -q    Suppress output messages"
            echo "  --help, -h     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                                    # Generate sitemap.xml"
            echo "  $0 --deploy                          # Generate and deploy to static/"
            echo "  $0 --output custom_sitemap.xml       # Generate with custom name"
            echo "  $0 --no-backup --deploy --quiet      # Deploy without backup, quietly"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to log messages
log() {
    if [ "$QUIET" = false ]; then
        echo -e "$1"
    fi
}

# Create backup if requested and file exists
if [ "$BACKUP" = true ] && [ -f "$OUTPUT_FILE" ]; then
    BACKUP_FILE="${OUTPUT_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    log "${YELLOW}📋 Creating backup: $BACKUP_FILE${NC}"
    cp "$OUTPUT_FILE" "$BACKUP_FILE"
fi

# Generate the sitemap
log "${BLUE}🔄 Generating sitemap...${NC}"

if [ "$QUIET" = true ]; then
    python generate_sitemap_file.py --output "$OUTPUT_FILE" --quiet
else
    python generate_sitemap_file.py --output "$OUTPUT_FILE"
fi

# Check if generation was successful
if [ ! -f "$OUTPUT_FILE" ]; then
    echo -e "${RED}❌ Sitemap generation failed${NC}"
    exit 1
fi

# Get file info
FILE_SIZE=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
URL_COUNT=$(grep -c "<loc>" "$OUTPUT_FILE" || echo "0")

log "${GREEN}✅ Sitemap generated successfully!${NC}"
log "📄 File: $OUTPUT_FILE"
log "🔗 URLs: $URL_COUNT"
log "📊 Size: $FILE_SIZE bytes"

# Deploy to static directory if requested
if [ "$DEPLOY" = true ]; then
    STATIC_DIR="static"

    if [ ! -d "$STATIC_DIR" ]; then
        log "${YELLOW}📁 Creating static directory...${NC}"
        mkdir -p "$STATIC_DIR"
    fi

    DEPLOY_PATH="$STATIC_DIR/sitemap.xml"

    # Create backup of existing deployed sitemap
    if [ -f "$DEPLOY_PATH" ]; then
        DEPLOY_BACKUP="${DEPLOY_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
        log "${YELLOW}📋 Backing up deployed sitemap: $DEPLOY_BACKUP${NC}"
        cp "$DEPLOY_PATH" "$DEPLOY_BACKUP"
    fi

    # Copy to static directory
    log "${BLUE}🚀 Deploying to $DEPLOY_PATH...${NC}"
    cp "$OUTPUT_FILE" "$DEPLOY_PATH"

    log "${GREEN}✅ Sitemap deployed successfully!${NC}"
    log "🌐 Available at: /static/sitemap.xml"
fi

# Validate XML structure
log "${BLUE}🔍 Validating XML structure...${NC}"

# Check for required XML elements
if grep -q '<?xml version="1.0" encoding="UTF-8"?>' "$OUTPUT_FILE" && \
   grep -q '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' "$OUTPUT_FILE" && \
   grep -q '</urlset>' "$OUTPUT_FILE"; then
    log "${GREEN}✅ XML structure is valid${NC}"
else
    echo -e "${RED}❌ XML structure validation failed${NC}"
    exit 1
fi

# Check for important URLs
log "${BLUE}🔍 Checking for important URLs...${NC}"

IMPORTANT_URLS=(
    "https://ardurhealthcare.com/"
    "https://ardurhealthcare.com/about-us"
    "https://ardurhealthcare.com/services"
    "https://ardurhealthcare.com/contact-us"
)

MISSING_URLS=()

for url in "${IMPORTANT_URLS[@]}"; do
    if grep -q "$url" "$OUTPUT_FILE"; then
        log "${GREEN}✅ Found: $url${NC}"
    else
        log "${RED}❌ Missing: $url${NC}"
        MISSING_URLS+=("$url")
    fi
done

if [ ${#MISSING_URLS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Warning: ${#MISSING_URLS[@]} important URLs are missing${NC}"
else
    log "${GREEN}✅ All important URLs are present${NC}"
fi

# Show summary
echo ""
echo -e "${GREEN}🎉 Sitemap update completed!${NC}"
echo "=================================================="
echo "📊 Statistics:"
echo "   • Total URLs: $URL_COUNT"
echo "   • File size: $FILE_SIZE bytes"
echo "   • Output file: $OUTPUT_FILE"

if [ "$DEPLOY" = true ]; then
    echo "   • Deployed to: $STATIC_DIR/sitemap.xml"
fi

echo ""
echo "🔗 Next steps:"
echo "   • Test the sitemap: https://ardurhealthcare.com/sitemap.xml"
echo "   • Submit to Google Search Console"
echo "   • Submit to Bing Webmaster Tools"
echo "   • Update robots.txt if needed"

# Check if robots.txt exists and suggest update
if [ -f "robots.txt" ]; then
    if grep -q "Sitemap:" "robots.txt"; then
        log "${GREEN}✅ robots.txt already contains Sitemap directive${NC}"
    else
        echo ""
        echo -e "${YELLOW}💡 Tip: Add this line to your robots.txt:${NC}"
        echo "Sitemap: https://ardurhealthcare.com/sitemap.xml"
    fi
fi

echo ""
log "${BLUE}Done! 🚀${NC}"
