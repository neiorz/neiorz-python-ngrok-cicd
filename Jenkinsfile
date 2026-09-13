pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nourz1/python-auto-pipeline'
        CREDENTIALS_ID = 'docker'
        KUBECONFIG = '/home/nourz/.kube/config'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: "${CREDENTIALS_ID}",
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl config current-context
                    kubectl get nodes
                    kubectl apply -f deployment.yaml
                '''
            }
        }
    }
}
