# PVT Mail Stock Monitor

A high-performance asynchronous Python tool for monitoring and purchasing mail stock from the Hotmail007 API. This tool continuously checks stock availability and automatically purchases mails when available using multiple concurrent workers.

## Features

- **Asynchronous Processing**: Uses aiohttp for efficient concurrent API calls
- **Multiple Workers**: Configurable number of concurrent stock checks
- **Real-time Monitoring**: Continuous stock checking with adjustable intervals
- **Automatic Purchasing**: Instant purchase when stock becomes available
- **Comprehensive Logging**: Color-coded logging with detailed error handling
- **Docker Support**: Containerized deployment for easy scaling
- **Environment Configuration**: Secure credential management via environment variables

## Prerequisites

- Python 3.12 or higher
- Docker (optional, for containerized deployment)
- Valid CLIENT_KEY from Hotmail007 API

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd pvt
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
CLIENT_KEY=your_hotmail007_client_key_here
```

**Security Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

### Configuration Parameters

You can modify the following parameters in `main.py`:

- `BASE_URL`: The base API URL (default: "https://gapi.hotmail007.com")
- `QUANTITY`: Number of mails to purchase per transaction (default: 1)
- `NUM_WORKERS`: Number of concurrent stock checking workers (default: 5)
- `CHECK_INTERVAL`: Time between stock checks in seconds (default: 0.2)

## Usage

### Running Locally

1. Ensure your `.env` file contains the CLIENT_KEY
2. Run the application:
```bash
uv run main.py
```

Or with Python directly:
```bash
python main.py
```

### Running with Docker

1. Build the Docker image:
```bash
docker build -t pvt-mail-monitor .
```

2. Run the container with your CLIENT_KEY:
```bash
docker run -e CLIENT_KEY=your_actual_client_key_here pvt-mail-monitor
```

For persistent logging, you can mount a volume:
```bash
docker run -e CLIENT_KEY=your_actual_client_key_here -v $(pwd)/logs:/app/logs pvt-mail-monitor
```

## How It Works

1. **Stock Monitoring**: Multiple worker threads continuously check the stock API endpoint
2. **Stock Detection**: When stock becomes available (> 0), workers attempt to purchase
3. **Purchase Execution**: Uses the configured CLIENT_KEY to make authenticated purchase requests
4. **Logging**: All activities are logged with timestamps and worker IDs for monitoring

## API Endpoints Used

- **Stock Check**: `https://gapi.hotmail007.com/api/mail/getStock?mailType=outlook/hotmail/hotmail%20Trusted/outlook%20Trusted`
- **Purchase**: `https://gapi.hotmail007.com/api/mail/getMail?clientKey={CLIENT_KEY}&mailType=outlook/hotmail/hotmail%20Trusted/outlook%20Trusted&quantity={quantity}`

## Logging

Logs are stored in the `logs/` directory with color-coded console output:
- **INFO**: Successful stock checks and purchases
- **ERROR**: API failures and exceptions

## Troubleshooting

### Common Issues

1. **Missing CLIENT_KEY**: Ensure your `.env` file exists and contains a valid key
2. **API Rate Limiting**: Adjust `CHECK_INTERVAL` if experiencing rate limits
3. **Network Issues**: The tool includes timeout handling and retry logic

### Performance Tuning

- Increase `NUM_WORKERS` for more concurrent checks (monitor API limits)
- Adjust `CHECK_INTERVAL` based on your monitoring frequency needs
- Modify `QUANTITY` based on your purchase requirements

## Development

### Project Structure

```
pvt/
├── main.py              # Main application logic
├── pyproject.toml       # Project configuration and dependencies
├── uv.lock             # Dependency lock file
├── utils/
│   └── logger.py       # Logging configuration
├── logs/               # Application logs
├── Dockerfile          # Docker container configuration
├── .dockerignore       # Docker build exclusions
└── .gitignore         # Git exclusions
```

### Adding Dependencies

To add new dependencies:

1. Update `pyproject.toml` dependencies section
2. Run `uv sync` to update the lock file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

[Add contribution guidelines here]
