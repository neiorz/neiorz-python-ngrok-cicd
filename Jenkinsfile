pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nourz1/python-auto-pipeline'
        CREDENTIALS_ID = 'docker'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build \
                -t ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                -t ${DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo $DOCKER_PASS | docker login \
                    -u $DOCKER_USER \
                    --password-stdin
                    '''

                    sh """
                    docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                export KUBECONFIG=/home/nourz/.kube/config

                kubectl config current-context
                kubectl cluster-info

                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                kubectl rollout status deployment/python-app
                '''
            }
        }
    }
}
