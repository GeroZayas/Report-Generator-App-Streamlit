# 📑 Report Generator App

- The Report Generator App is a powerful tool that allows you to create custom reports based on your data.
- It uses **Streamlit**

## Using Docker

If you prefer using Docker, you can build and run the application with the provided Dockerfile. First, ensure you have Docker installed on your system.

**Build the Docker image:**

```bash
docker build -t report-generator-app .
```

**Run the Docker container:**

```bash
docker run -d -p 8501:8501 --name report_generator report_generator_app
```

The application will be available at http://localhost:8501/.
