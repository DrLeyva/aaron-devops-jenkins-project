pipeline {
    agent any

    environment {
        APP_IMAGE = "aaron-devops-app"
        APP_TAG = "${BUILD_NUMBER}"
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

        stage('Verify Docker Image') {
            steps {
                sh '''
                    docker image inspect ${APP_IMAGE}:${APP_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully"
            echo "Created Docker image ${APP_IMAGE}:${APP_TAG}"
        }

        failure {
            echo 'Pipeline failed. Review the failed stage and console output.'
        }

        always {
            sh 'rm -rf .venv-ci'
        }
    }
}