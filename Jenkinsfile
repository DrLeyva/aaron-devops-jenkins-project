pipeline {
    agent any

    environment {
        APP_IMAGE = "aaron-devops-app"
        APP_TAG = "${BUILD_NUMBER}"
        APP_CONTAINER = "aaron-devops-app"
        APP_NETWORK = "aaronproject_default"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Repository loaded from GitHub'
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    rm -rf .venv-ci
                    python3 -m venv .venv-ci
                    . .venv-ci/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh '''
                    . .venv-ci/bin/activate
                    python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t ${APP_IMAGE}:${APP_TAG} \
                        -t ${APP_IMAGE}:latest \
                        .
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f ${APP_CONTAINER} || true

                    docker run -d \
                        --name ${APP_CONTAINER} \
                        --restart unless-stopped \
                        --network ${APP_NETWORK} \
                        -p 5000:5000 \
                        ${APP_IMAGE}:${APP_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    python3 - <<'PY'
import json
import time
import urllib.request

url = "http://aaron-devops-app:5000/health"

for attempt in range(1, 11):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = json.loads(response.read().decode())

            if response.status == 200 and body.get("status") == "healthy":
                print("Application health check passed")
                print(body)
                raise SystemExit(0)

    except Exception as error:
        print(f"Health check attempt {attempt} failed: {error}")

    time.sleep(2)

print("Application failed its health check")
raise SystemExit(1)
PY
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    docker ps --filter name=${APP_CONTAINER}
                    docker inspect ${APP_CONTAINER}
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully"
            echo "Deployed ${APP_IMAGE}:${APP_TAG}"
        }

        failure {
            echo 'Pipeline failed. Review the failed stage and console output.'
        }

        always {
            sh 'rm -rf .venv-ci'
        }
    }
}