pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Repository successfully loaded from GitHub'
            }
        }

        stage('Verify Files') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Test Pipeline') {
            steps {
                echo 'Jenkins successfully executed the Jenkinsfile'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed. Review the console output.'
        }
    }
}