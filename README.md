# Cellomage

A Flask-based web application for cell image analysis using Cellpose deep learning models. Upload cell images and get automated cell counting, confluency analysis, and visualization results.

## Features

- **Single & Batch Image Processing**: Upload one or multiple cell images for analysis
- **Cell Counting**: Automated cell detection and counting using Cellpose AI models
- **Confluency Analysis**: Calculate cell confluency percentages
- **Multiple View Modes**: 
  - Dots view: Visualize detected cells as dots
  - Mask view: Display segmentation masks
- **Audit Logging**: Track all analysis activities with MongoDB
- **Responsive Web Interface**: Modern, user-friendly UI

## Requirements

### Python Version
- Python 3.10 or higher

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | Latest | Web framework |
| Flask-PyMongo | Latest | MongoDB integration for Flask |
| PyMongo | Latest | MongoDB driver |
| Gunicorn | Latest | Production WSGI server |
| NumPy | 1.26.4 | Numerical computing |
| OpenCV (headless) | 4.11.0.86 | Image processing (headless) |
| OpenCV | 4.11.0.86 | Image processing |
| scikit-image | Latest | Image processing utilities |
| Cellpose | 3.0.11 | Deep learning cell segmentation |
| PyTorch | Latest | Deep learning framework (required by Cellpose) |
| tqdm | Latest | Progress bars |
| Matplotlib | Latest | Plotting and visualization |
| Pillow | Latest | Image manipulation |

### System Requirements

- **MongoDB**: Version 4.0 or higher
  - Running on `localhost:27017` (default)
  - Database name: `cellomage`

- **Storage**: 
  - Space for uploaded images
  - Space for processed results
  - Model files (Cellpose models)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aviseka00/cellomage.git
cd cellomage
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installing PyTorch and Cellpose may take several minutes as these are large packages.

### 4. Set Up MongoDB

#### Option A: Local MongoDB Installation
1. Download and install MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   ```bash
   # Windows (if installed as service, it starts automatically)
   # Linux/Mac
   sudo systemctl start mongod
   ```

#### Option B: Docker
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

### 5. Configure the Application

Edit `config.py` if needed (defaults should work for local development):

```python
SECRET_KEY = "cellomage_secret_key"  # Change for production
MONGO_URI = "mongodb://localhost:27017/cellomage"
MODEL_PATH = "models/my_cells_v2"
UPLOAD_FOLDER = "uploads/originals"
RESULT_FOLDER = "results"
```

### 6. Ensure Model Files Exist

Make sure the Cellpose model is available at `models/my_cells_v2`. The model will be downloaded automatically on first use if not present.

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Production Mode (using Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Project Structure

```
cellomage/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
│
├── database/
│   └── mongo.py          # MongoDB connection setup
│
├── models/
│   └── my_cells_v2/      # Cellpose model files
│
├── services/
│   ├── cellpose_service.py  # Cell analysis service
│   ├── image_utils.py       # Image processing utilities
│   └── audit_service.py     # Audit logging service
│
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   ├── manifest.json     # PWA manifest
│   └── service-worker.js # PWA service worker
│
├── templates/
│   ├── base.html         # Base template
│   ├── upload.html       # Upload page
│   ├── result.html       # Single result page
│   ├── batch_result.html # Batch results page
│   └── audit.html        # Audit logs page
│
├── uploads/
│   └── originals/          # Uploaded images (gitignored)
│
└── results/
    ├── dots/              # Dots view results (gitignored)
    └── masks/              # Mask view results (gitignored)
```

## API Endpoints

- `GET /` - Upload page (dashboard)
- `POST /upload` - Upload and analyze images
  - Supports single or batch uploads
  - Form data: `images` (file(s)), `view` (dots/mask)
- `GET /uploads/<filename>` - Serve uploaded images
- `GET /results/<filename>` - Serve result images
- `GET /audit` - View audit logs

## Usage

1. **Access the Application**: Navigate to `http://localhost:5000`
2. **Upload Images**: Select one or multiple cell images
3. **Choose View Mode**: Select "dots" or "mask" visualization
4. **View Results**: 
   - Single image: See detailed analysis with cell count and confluency
   - Batch upload: See summary with total cells and average confluency
5. **Check Audit Logs**: Visit `/audit` to see analysis history

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: MongoDB (for audit logging)
- **AI/ML**: Cellpose 3.0.11 (cell segmentation)
- **Deep Learning**: PyTorch (neural network backend)
- **Image Processing**: OpenCV, scikit-image, Pillow
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn (WSGI server)

## Notes

- The application automatically creates required directories (`uploads/`, `results/`) on first run
- Cellpose models are downloaded automatically on first use
- Large files (uploads, results, cache) are excluded from git via `.gitignore`
- Virtual environments should not be committed to the repository

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongosh` or check service status
- Verify connection string in `config.py`
- Check firewall settings if MongoDB is on a remote server

### Model Loading Errors
- Ensure internet connection for first-time model download
- Check `models/` directory permissions
- Verify sufficient disk space

### Port Already in Use
- Change port in `app.py` (line 170): `app.run(host="0.0.0.0", port=5001)`

## License

[Add your license here]

## Author

[Add author information here]

## Contributing

[Add contribution guidelines if applicable]

