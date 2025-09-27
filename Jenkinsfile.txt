pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "wine-app"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Build') {
            steps {
                echo " Building Docker image..."
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }

        stage('Test') {
            steps {
                echo " Running unit tests..."
                sh "pytest test_app.py"
            }
        }

        stage('Code Quality') {
            steps {
                echo " Checking code quality with pylint..."
                sh "pylint app.py || true"
            }
        }

        stage('Security') {
            steps {
                echo " Running security scan with Bandit..."
                sh "bandit -r . || true"
            }
        }

        stage('Deploy') {
            steps {
                echo " Deploying application using Docker Compose..."
                sh "docker-compose up -d"
            }
        }

        stage('Release') {
            steps {
                script {
                    echo " Creating release tag v1.0..."
                    sh 'git tag -a v1.0 -m "Release v1.0" || true'
                    sh "git push origin v1.0 || true"
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo "📈 Monitoring setup:"
                echo "Prometheus → http://localhost:9090"
                echo "Grafana → http://localhost:3000"
            }
        }
    }

    post {
        always {
            echo " Pipeline finished. Check logs for details."
        }
        success {
            echo " Pipeline completed successfully!"
        }
        failure {
            echo " Pipeline failed. Please check the logs."
        }
    }
}
