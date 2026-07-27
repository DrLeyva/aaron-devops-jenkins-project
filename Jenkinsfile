pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Repository successfully loaded from GitHub'
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
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
    }

    post {
        success {
            echo 'Continuous integration tests completed successfully'
        }

        failure {
            echo 'Pipeline failed. Review the failed stage and console output.'
        }

        always {
            sh 'rm -rf .venv-ci'
        }
    }
}