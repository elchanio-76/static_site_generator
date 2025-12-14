# Static Site Generator

A lightweight, zero-dependency static site generator written in Python that converts Markdown files to HTML while preserving your file and folder structure. Built specifically for GitHub Pages deployment.

## Features

- **Zero Dependencies**: Pure Python implementation using only the standard library
- **Markdown to HTML**: Full support for headings, paragraphs, lists, code blocks, quotes, and inline formatting
- **Inline Formatting**: Bold (`**text**`), italic (`_text_`), code (`` `code` ``), links (`[text](url)`), and images (`![alt](url)`)
- **Structure Preservation**: Maintains your content directory structure in the output
- **GitHub Pages Ready**: Built-in support for GitHub Pages deployment with configurable base paths
- **Template System**: Simple HTML template with title and content placeholders
- **Comprehensive Tests**: 999 lines of unit tests covering all functionality
- **Development Server**: Built-in local server for testing your site

## Project Structure

```
static_site_generator/
├── src/                    # Python source code
│   ├── main.py            # Build orchestration and entry point
│   ├── helper.py          # Markdown parsing and conversion
│   ├── htmlnode.py        # HTML node classes
│   ├── textnode.py        # Text node classes and types
│   └── test_*.py          # Comprehensive unit tests
├── content/               # Your Markdown content goes here
│   ├── index.md          # Homepage
│   ├── blog/             # Example blog structure
│   └── contact/          # Example contact page
├── public/                # Static assets (CSS, images)
│   └── index.css         # Stylesheet
├── docs/                  # Generated HTML output (for GitHub Pages)
├── template.html          # HTML template
├── build.sh              # Production build script
├── main.sh               # Development server script
└── test.sh               # Test runner script
```

## Requirements

- Python 3.7 or higher
- No external dependencies required!

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/static_site_generator.git
   cd static_site_generator
   ```

2. **Optional: Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Verify installation**:
   ```bash
   python3 src/main.py --help
   ```

## Quick Start

### 1. Add Your Content

Create Markdown files in the `content/` directory:

```bash
# Create a new page
echo "# My First Page" > content/my-page.md
echo "This is my content!" >> content/my-page.md

# Create a nested structure
mkdir -p content/blog/my-post
echo "# My Blog Post" > content/blog/my-post/index.md
```

### 2. Build Your Site

For local development:
```bash
./main.sh
# Site will be available at http://localhost:8888
```

For production (GitHub Pages):
```bash
./build.sh
```

Or run Python directly:
```bash
# Development build (base path = "/")
python3 src/main.py

# Production build (base path = "/your-repo-name/")
python3 src/main.py "/your-repo-name/"
```

### 3. View Your Site

Open your browser to `http://localhost:8888` when using the development server.

## Usage

### Writing Markdown Content

The generator supports standard Markdown syntax:

#### Headings
```markdown
# H1 Heading
## H2 Heading
### H3 Heading
```

#### Text Formatting
```markdown
**bold text**
_italic text_
`inline code`
```

#### Links and Images
```markdown
[Link text](https://example.com)
![Image alt text](/images/photo.jpg)
```

#### Lists
```markdown
- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2
```

#### Code Blocks
````markdown
```
code block content
```
````

#### Quotes
```markdown
> This is a quote
> spanning multiple lines
```

### Page Requirements

**Every Markdown file MUST include an H1 heading**. This is extracted as the page title:

```markdown
# My Page Title

Content goes here...
```

The H1 becomes the `<title>` tag in the generated HTML.

### Customizing the Template

Edit `template.html` to customize your site's layout:

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

**Available placeholders**:
- `{{ Title }}` - Replaced with the H1 heading from your Markdown
- `{{ Content }}` - Replaced with the generated HTML content

### Styling Your Site

Add your CSS to `public/index.css`. This file is automatically copied to the output directory.

You can also add other static assets (images, JavaScript, fonts) to the `public/` directory.

## Deployment

### GitHub Pages

1. **Configure your repository**:
   - Go to Settings → Pages
   - Set "Source" to "Deploy from a branch"
   - Select the `main` branch and `/docs` folder
   - Click "Save"

2. **Update the build script**:

   Edit `build.sh` and replace `/static_site_generator/` with your repository name:
   ```bash
   #!/bin/bash

   source .venv/bin/activate
   python3 src/main.py "/your-repo-name/"
   deactivate
   ```

3. **Build and deploy**:
   ```bash
   ./build.sh
   git add docs/
   git commit -m "Build site"
   git push origin main
   ```

4. **Access your site**:
   Your site will be available at `https://yourusername.github.io/your-repo-name/`

### Other Hosting Providers

The generated HTML in `docs/` is standard static content. You can deploy it to:

- **Netlify**: Drag and drop the `docs/` folder
- **Vercel**: Connect your repo and set build command to `python3 src/main.py`
- **AWS S3**: Upload the `docs/` contents to an S3 bucket
- **Any static host**: Upload the `docs/` directory

For non-GitHub Pages hosting, use the default base path:
```bash
python3 src/main.py "/"
```

## Development

### Running Tests

Run the comprehensive test suite:

```bash
./test.sh
# or
python -m unittest discover -s src
```

All tests should pass:
```
.............................
----------------------------------------------------------------------
Ran X tests in 0.XXXs

OK
```

### Development Workflow

1. **Make changes** to your content in `content/`
2. **Rebuild** by running `python3 src/main.py`
3. **Test locally** with the development server (`./main.sh`)
4. **Run tests** to ensure nothing broke (`./test.sh`)
5. **Commit and push** your changes

### Project Scripts

- **`build.sh`**: Production build with GitHub Pages base path
- **`main.sh`**: Development build + local server on port 8888
- **`test.sh`**: Run all unit tests

## Architecture

The generator follows a multi-stage conversion pipeline:

```
Markdown File
    ↓
Blocks (paragraphs, headings, lists)
    ↓
TextNodes (intermediate representation)
    ↓
HTMLNodes (tree structure)
    ↓
HTML String
    ↓
Template Injection
    ↓
Final HTML File
```

For detailed architecture information, see [Architecture.md](./Architecture.md).

### Key Components

- **`main.py`**: Entry point, orchestrates the build process
- **`helper.py`**: Markdown parsing, block processing, HTML generation
- **`textnode.py`**: Text node types (TEXT, BOLD, ITALIC, CODE, LINK, IMAGE)
- **`htmlnode.py`**: HTML node classes (HTMLNode, LeafNode, ParentNode)

## Troubleshooting

### Build fails with "No title found"

Every Markdown file must have an H1 heading:
```markdown
# Page Title

Your content here...
```

### CSS not loading

Make sure your CSS is in `public/index.css`. The build script copies this to `docs/index.css`.

### Images not displaying

- Use absolute paths from root: `/images/photo.jpg`
- Place images in `public/images/` directory
- They'll be copied to `docs/images/` during build

### Links not working on GitHub Pages

Make sure you're using the correct base path in `build.sh`:
```bash
python3 src/main.py "/your-exact-repo-name/"
```

### "Source directory is not within project workspace" error

This is a security feature. Only directories within the project can be used as source/target.

## Limitations

Current limitations (potential future improvements):

- No frontmatter support (YAML metadata)
- No table support
- No syntax highlighting for code blocks
- No automatic sitemap/RSS generation
- No incremental builds (rebuilds everything)
- Single template for all pages
- No plugin system

## Contributing

This is an educational project. Feel free to fork and extend it with your own features!

## License

MIT License - See [LICENSE](./LICENSE) for details

## Acknowledgments

Built as a learning project to understand static site generation from first principles.

---

**Need help?** Open an issue on GitHub or check the [Architecture.md](./Architecture.md) for implementation details.
