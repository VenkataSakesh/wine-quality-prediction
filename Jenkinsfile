pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "wine-app"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker image..."
                bat "docker build --no-cache -t %DOCKER_IMAGE% ."
            }
        }

        stage('Test') {
            steps {
                echo "Running unit tests inside Docker..."
                bat "docker run --rm %DOCKER_IMAGE% pytest test_app.py"
            }
        }

        stage('Code Quality') {
            steps {
                echo "Checking code quality with pylint..."
                bat "pylint app.py || exit 0"
            }
        }

        stage('Security') {
            steps {
                echo "Running security scan with Bandit..."
                bat "bandit -r . || exit 0"
                echo "If vulnerabilities are found, explain severity and how you addressed them in your report."
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying application using Docker Compose..."
                bat "docker-compose up -d"
            }
        }

        stage('Release') {
            environment {
                GITHUB_TOKEN = credentials('github-creds') // Use the Jenkins secret ID
            }
            steps {
                script {
                    echo "Creating release tag v1.0..."
                    // Configure git user
                    bat 'git config user.name "Jenkins CI"'
                    bat 'git config user.email "jenkins@example.com"'
                    // Create tag
                    bat 'git tag -a v1.0 -m "Release v1.0" || exit 0'
                    // Push tag using PAT
                    bat "git push https://$GITHUB_TOKEN@github.com/VenkataSakesh/wine-quality-prediction.git v1.0 || exit 0"
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo "📈 Monitoring setup:"
                echo "Prometheus → http://localhost:9090"
                echo "Grafana → http://localhost:3000"
                echo "Configure monitoring and alerting to detect production issues."
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Check logs for details."
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}
