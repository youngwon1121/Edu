pipeline {
    agent any
    stages {
        stage('Git clone') {
            steps {
                git 'https://github.com/youngwon1121/post-crawler.git';
            }
        }

        stage('Docker build') {
            steps{
                script {
                    newImage = docker.build("peter9932/post-crawler:${env.BUILD_ID}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    newImage.inside() {
                        sh './manage.py test'
                    }
                }
            }
        }

        stage('Docker push') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'peter9932') {
                        newImage.push()
                    }
                }
            }
        }

    }
}
